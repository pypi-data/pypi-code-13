import time
import sys
import logging
import collections
import threading
import traceback
import os
import platform
import argparse
import requests

from MeteorClient import MeteorClient
try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x
from subprocess import Popen, PIPE, STDOUT
from utils import NonBlockingStreamReader, Resource
from utils import rate_limited
from MeteorFiles import Uploader

RATE_LIMIT = 5

TASK_INNER_PROPERTIES = ['taskDoc', 'id', 'processor', 'worker', 'subtasks', 'meteorClient', 'has_key', 'abort']
class Task(object):

    def __init__(self, taskDoc, worker, meteorClient):
        self.taskDoc = taskDoc
        self.worker = worker
        self.meteorClient = meteorClient
        self.abort = threading.Event()
        self.has_key = self.taskDoc.has_key
        if self.taskDoc.has_key('_id'):
            self.id = self.taskDoc['_id']
        else:
            self.id = None
        self.processor = None
        self.subtasks = set()

    def __getitem__(self, key):
        if not self.taskDoc:
            return None
        if '.' in key:
            ks = key.split('.')
            d = self.taskDoc
            for k in ks:
                if isinstance(d, dict) and d.has_key(k):
                    d = d[k]
                else:
                    return None
            return d
        elif self.taskDoc.has_key(key):
            return self.taskDoc[key]
        else:
            return None
    def __set__(self, key, value=None):
        assert (type(key) is str and not value is None)or (type(key) is dict and value is None)
        if key == 'running':
            if self.processor:
                self.processor.running = value
            return
        if not type(key) is dict and self.get(key) == value:
            return

        if type(key) is dict:
            vdict = key
            try:
                self.meteorClient.call('tasks.update.worker', [
                                       self.id, self.worker.id, self.worker.token, {'$set': vdict}])
            except Exception as e:
                print('error ocurred during setting ' + str(vdict))
            finally:
                return

        if key == "visible2worker" and value == False:
            vdict = {key: value, "status.running": False}
        elif self.processor and self.get('status.running') != self.processor.running:
            vdict = {key: value, "status.running": self.processor.running}
        else:
            vdict = {key: value}
        try:
            self.meteorClient.call('tasks.update.worker', [
                                   self.id, self.worker.id, self.worker.token, {'$set': vdict}])
        except Exception as e:
            print('error ocurred during setting ' + str(vdict))

    def __setitem__(self, key, value):
        return self.__set__(key,value)

    def __getattr__(self, attr):
        if attr in TASK_INNER_PROPERTIES:
            return super(Task, self).__getattribute__(attr)
        elif attr == 'running':
            if self.processor:
                return self.processor.running
            else:
                return False
        if self.taskDoc.has_key(attr):
            return self.taskDoc[attr]
        else:
            return None

    @rate_limited(RATE_LIMIT)
    def __setattr__(self, key, value):
        if key in TASK_INNER_PROPERTIES:
            super(Task, self).__setattr__(key, value)
        else:
            self.__set__(key,value)

    def __delattr__(self, item):
        self.__delitem__(item)

    def get(self, key):
        return self.__getitem__(key)

    @rate_limited(RATE_LIMIT, important=True)
    def set(self, key, value=None):
        self.__set__(key, value)

    @rate_limited(RATE_LIMIT, important=False)
    def update(self, key, value=None):
        self.__set__(key, value)

    @rate_limited(RATE_LIMIT, important=True)
    def push(self, key, value=None):
        try:
            vdict = key if type(key) is dict and value is None else {key: value}
            self.meteorClient.call('tasks.update.worker', [
                                   self.id, self.worker.id, self.worker.token, {'$push': vdict}])
        except Exception as e:
            print('error ocurred during setting ' + key)

    @rate_limited(RATE_LIMIT, important=True)
    def pull(self, key, value=None):
        try:
            vdict = key if type(key) is dict and value is None else {key: value}
            self.meteorClient.call('tasks.update.worker', [
                                   self.id, self.worker.id, self.worker.token, {'$pull': vdict}])
        except Exception as e:
            print('error ocurred during setting ' + key)

    def upload(self, filePath):
        uploader = Uploader(self.meteorClient, 'files', transport='http', verbose=True)
        meta = {"taskId":self.id, "widgetId":self.get('widgetId'), "workerId":self.worker.id, 'workerToken': self.worker.token}
        uploader.upload(filePath, meta=meta)

    def files(self, selector={}):
        selector['meta.taskId'] = self.id
        return self.find('files', selector)

    def file(self, selector={}):
        selector['meta.taskId'] = self.id
        return self.find_one('files', selector)

    def download(self, file):
        if isinstance(file, (str, unicode)):
            fileObj = self.meteorClient.find_one('files', {'_id': file})
        else:
            fileObj = file
        if fileObj:
            baseurl = self.meteorClient.ddp_client.url
            assert baseurl.startswith('ws://') and baseurl.endswith('/websocket')
            if not fileObj.has_key('version'):
                fileObj['version'] = 'original'
            if fileObj.has_key('extension') and len(fileObj['extension'])>0:
                ext = '.' + fileObj['extension']
            else:
                ext = ''
            fileObj['ext'] = ext
            downloadUrl = 'http' + baseurl[2:-10] + "{_downloadRoute}/{_collectionName}/{_id}/{version}/#{_id}#{ext}".format(**fileObj)
            if not os.path.exists(self.processor.workdir):
                os.makedirs(self.processor.workdir)
            save_path = os.path.join(self.processor.workdir, fileObj['name'])
            r = requests.get(downloadUrl, stream=True)
            with open(save_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
            return save_path

    def find(self, collection, selector={}):
        '''
        support multi-level selector
        '''
        results = []
        for _id, doc in self.meteorClient.collection_data.data.get(collection, {}).items():
            doc.update({'_id': _id})
            if selector == {}:
                results.append(doc)
            for key, value in selector.items():
                if '.' in key:
                    keys = key.split('.')
                    v = doc
                    for k in keys:
                        if k in v:
                            v = v[k]
                        else:
                            break
                    if v == value:
                        results.append(doc)
                else:
                    if key in doc and doc[key] == value:
                        results.append(doc)
        return results

    def find_one(self, collection, selector={}):
        for _id, doc in self.meteorClient.collection_data.data.get(collection, {}).items():
            doc.update({'_id': _id})
            if selector == {}:
                return doc
            for key, value in selector.items():
                if '.' in key:
                    keys = key.split('.')
                    v = doc
                    for k in keys:
                        if k in v:
                            v = v[k]
                        else:
                            break
                    if v == value:
                        return doc
                else:
                    if key in doc and doc[key] == value:
                        return doc
    def save(self, filename=None):
        import ejson
        workdir = self.processor.workdir
        if not os.path.exists(workdir):
            os.makedirs(workdir)
        if filename is None:
            filename = 'task.ejson'
        with open(os.path.join(workdir, filename), 'w') as f:
            f.write(ejson.dumps())

class Widget(object):

    def __init__(self, widgetDoc, worker, meteorClient):
        self.widgetDoc = widgetDoc
        self.meteorClient = meteorClient
        self.worker = worker
        self.has_key = self.widgetDoc.has_key
        if self.widgetDoc.has_key('_id'):
            self.id = self.widgetDoc['_id']
        else:
            raise Exception('invalid widgetDoc')
        self.workdir = os.path.join(self.worker.workdir, 'widget-'+self.id)
        if not os.path.exists(self.workdir):
            os.makedirs(self.workdir)

    def __getitem__(self, key):
        if not self.widgetDoc:
            return None
        if '.' in key:
            ks = key.split('.')
            d = self.widgetDoc
            for k in ks:
                if isinstance(d, dict) and d.has_key(k):
                    d = d[k]
                else:
                    return None
            return d
        elif self.widgetDoc.has_key(key):
            return self.widgetDoc[key]
        else:
            return None

    def __setitem__(self, key, value):
        # TODO: remove this after login
        raise Exception('widgets is readonly for worker.')

    def get(self, key):
        return self.__getitem__(key)

    @rate_limited(RATE_LIMIT, important=True)
    def set(self, key, value):
        self.__setitem__(key, value)

    @rate_limited(RATE_LIMIT, important=False)
    def update(self, key, value):
        self.__setitem__(key, value)

    def exec_widget_task_processor(self, task, widget, worker):
        import time
        id = widget.id
        widget_task_processor = self.default_task_processor
        ns = {'TASK': task, 'WIDGET': widget,
              'WORKER': worker, '__name__': '__worker__', 'time': time}
        exec(widget.get('code_snippets')['__init___py']['content'], ns)
        if ns.has_key('TASK_PROCESSOR'):
            return ns['TASK_PROCESSOR']
        else:
            return None

    def default_task_processor(self, task, widget, worker):
        print('default_task_processor: ' + task.id)

    def get_task_processor(self):
        return self.exec_widget_task_processor


class Worker(object):

    def __init__(self, worker_id=None, worker_token=None,
                 server_url='ws://localhost:3000/websocket', workdir='./', dev_mode=True, thread_num=10):
        self.serverUrl = server_url
        self.id = worker_id
        assert not worker_id is None, 'Please set a valid worker id and token.'
        self.token = worker_token
        self.devWidgets = {}
        self.productionWidgets = {}
        self.workerDoc = None
        self.userName = None
        self.userId = None
        self.workTasks = collections.OrderedDict()
        self.taskQueue = Queue()
        self.thread_num = thread_num
        self.maxTaskNum = 50
        self.taskWorkerThreads = []
        self.taskWorkerAbortEvents = []
        self.resources = {}
        self.cpuThreadCount = 50
        self.workerVersion = "0.0"
        self.logger = logging.getLogger('worker')

        self.workdir = os.path.abspath(os.path.join(workdir, 'worker-'+worker_id))
        if not os.path.exists(self.workdir):
            os.makedirs(self.workdir)
        self.init()
        self.prepare_resources()

        self.connectionManager = ConnectionManager(
            server_url=server_url, worker=self)
        self.meteorClient = self.connectionManager.client

    def start(self):
        self.start_monitor_thread()
        self.start_task_threads()
        self.connectionManager.connect()
        self.connectionManager.run()

    def init(self):
        pass

    def prepare_resources(self):
        self.get_cpu_thread_pool()
        self.get_platform_info()
        try:
            self.get_gpu_resources()
        except Exception as e:
            print('error occured during getting gpu resources.')

    def get_cpu_thread_pool(self):
        self.resources['cpu_thread'] = Resource(
            'cpu_thread', 'cpu_thread#main', self.cpuThreadCount)

    def get_platform_info(self):
        self.resources['platform'] = Resource('platform', 'platform#', 1)
        self.resources['platform'].features[
            'uname'] = ', '.join(platform.uname())
        self.resources['platform'].features['machine'] = platform.machine()
        self.resources['platform'].features['system'] = platform.system()
        self.resources['platform'].features['processor'] = platform.processor()
        self.resources['platform'].features['node'] = platform.node()

    def get_gpu_resources(self):
        from device_query import get_devices, get_nvml_info
        devices = get_devices()
        for i, device in enumerate(devices):
            gpuResource = Resource('gpu', 'gpu#' + str(i))
            self.resources['gpu#' + str(i)] = gpuResource
            for name, t in device._fields_:
                if name not in [
                        'name', 'totalGlobalMem', 'clockRate', 'major', 'minor', ]:
                    continue
                if 'c_int_Array' in t.__name__:
                    val = ','.join(str(v) for v in getattr(device, name))
                else:
                    val = getattr(device, name)
                gpuResource.features[name] = Metrics(name, val)

            info = get_nvml_info(i)
            if info is not None:
                if 'memory' in info:
                    gpuResource.status['Total memory'] = Metrics('Total memory',
                                                                 info['memory']['total'] / 2**20, 'MB')
                    gpuResource.status['Used memory'] = Metrics('Used memory',
                                                                info['memory']['used'] / 2**20, 'MB')
                if 'utilization' in info:
                    gpuResource.status['Memory utilization'] = Metrics(
                        'Memory utilization', info['utilization']['memory'], '%')
                    gpuResource.status['GPU utilization'] = Metrics(
                        'GPU utilization', info['utilization']['gpu'], '%')
                if 'temperature' in info:
                    gpuResource.status[
                        'temperature'] = Metrics('temperature', info['temperature'], 'C')

    def worker_monitor(self):
        while not self.connectionManager.ready:
            time.sleep(0.2)
        print('worker monitor thread started.')
        self.get_gpu_resources()
        features = ''
        for k in self.resources:
            features += self.resources[k].id + ':\n'
            for f in self.resources[k].features.values():
                features += str(f) + '\n'
        self.set('version', self.workerVersion)
        self.set('sysInfo', features)
        self.set('name', self.resources['platform'].features['node'] + '-' + self.id)
        self.set('status', 'ready')
        while True:
            self.get_gpu_resources()
            resources = ''
            for k in self.resources:
                resources += self.resources[k].id + ':\n'
                for s in self.resources[k].status.values():
                    resources += str(s) + '\n'
            self.set('resources', resources)
            time.sleep(2.0)

    def register_widget(self, widget):
        id = widget.id
        print('register widget: ' + id)
        if widget.get('mode') == 'development':
            self.devWidgets[id] = widget
            if self.productionWidgets.has_key(id):
                del self.productionWidgets[id]
            if widget.get('code_snippets'):
                for k in widget.get('code_snippets').keys():
                    k = k.replace('.', '_')
                    code = widget.get('code_snippets')[k]
                    with open(os.path.join(widget.workdir, code['name']), 'w') as f:
                        f.write(code['content'])

        if widget.get('mode') == 'production':
            self.productionWidgets[id] = widget
            if self.devWidgets.has_key(id):
                del self.devWidgets[id]

    def unregister_widget(self, widgetId):
        if self.devWidgets.has_key(widgetId):
            del self.devWidgets[widgetId]
        if self.productionWidgets.has_key(widgetId):
            del self.productionWidgets[widgetId]

    def is_widget_registered(self, widgetId):
        if self.devWidgets.has_key(widgetId):
            return True
        if self.productionWidgets.has_key(widgetId):
            return True
        return False

    def get_registered_widget(self, widgetId):
        if self.devWidgets.has_key(widgetId):
            return self.devWidgets[widgetId]
        if self.productionWidgets.has_key(widgetId):
            return self.productionWidgets[widgetId]
        return None

    def __getitem__(self, key):
        if not self.workerDoc:
            return None
        if '.' in key:
            ks = key.split('.')
            d = self.workerDoc
            for k in ks:
                if d.has_key(k):
                    d = d[k]
                else:
                    return None
            return d
        elif self.workerDoc.has_key(key):
            return self.workerDoc[key]
        else:
            return None

    def __set__(self, key, value=None):
        assert (type(key) is str and not value is None)or (type(key) is dict and value is None)
        if not type(key) is dict and self.get(key) == value:
            return
        try:
            vdict = key if type(key) is dict and value is None else {key: value}
            self.meteorClient.call('workers.update', [self.id, self.token, {
                                   '$set': vdict}], self.default_update_callback)
        except Exception as e:
            print('error ocurred during setting ' + key)
    def __setitem__(self, key, value):
        self.__set__(key, value)

    def get(self, key):
        return self.__getitem__(key)

    @rate_limited(RATE_LIMIT)
    def set(self, key, value=None):
        self.__set__(key, value)

    @rate_limited(RATE_LIMIT, important=False)
    def update(self, key, value=None):
        self.__set__(key, value)

    @rate_limited(RATE_LIMIT)
    def push(self, key, value):
        try:
            self.meteorClient.call('workers.update', [self.id, self.token, {
                                   '$push': {key: value}}], self.default_update_callback)
        except Exception as e:
            print('error ocurred during setting ' + key)

    @rate_limited(RATE_LIMIT)
    def pull(self, key, value):
        try:
            self.meteorClient.call('workers.update', [self.id, self.token, {
                                   '$pull': {key: value}}], self.default_update_callback)
        except Exception as e:
            print('error ocurred during setting ' + key)

    def default_update_callback(self, error, result):
        if error:
            print(error)
            return

    def start_monitor_thread(self):
        mThread = threading.Thread(target=self.worker_monitor)
        # daemon lets the program end once the tasks are done
        mThread.daemon = True
        mThread.start()
        self.monitorThread = mThread

    def start_task_threads(self):
        for i in range(self.thread_num):
            abortEvent = threading.Event()
            # Create 1 threads to run our jobs
            aThread = threading.Thread(
                target=self.work_on_task, args=[abortEvent])
            # daemon lets the program end once the tasks are done
            aThread.daemon = True
            aThread.start()
            self.taskWorkerThreads.append(aThread)
            self.taskWorkerAbortEvents.append(abortEvent)
        print('{} task threads started'.format(self.thread_num))

    def stop_task_threads(self):
        for abortEvent in self.taskWorkerAbortEvents:
            abortEvent.set()
        print('stop worker')
        self.taskWorkerThreads = []
        self.taskWorkerAbortEvents = []

    def task_worker_changed(self, task, key, value):
        print('worker changed')
        if value != self.id:
            self.remove_task(task)

    def add_task(self, task):
        taskId = task.id
        if task and task.get('widgetId') and self.is_widget_registered(task.get('widgetId')):
            widget = self.get_registered_widget(task.get('widgetId'))
            task_processor = widget.get_task_processor()
            if task_processor:
                try:
                    #task.set('status', {"stage":'-', "running": False, "error":'', "progress":-1})
                    if not 'autoRestart' in task.get('tags') and task.get('status.running') == True:
                        task.set('cmd', '')
                        task.set('status.stage', 'interrupted')
                        task.set('status.running', False)
                        task.set('status.error', 'worker restarted unexpectedly.')
                    if 'ing' in task.get('status.stage'):
                        task.set('status.stage', '-')
                    tp = task_processor(task, widget, self)
                except Exception as e:
                    traceback.print_exc()
                    task.set('status', task.get('status') or {})
                    task.set('status.running', False)
                    task.set('status.error', traceback.format_exc())
                    task.set('cmd', '')
                    task.set('visible2worker', False)
                else:
                    if tp:
                        if not self.workTasks.has_key(taskId):
                            #print('add task {} to {}'.format(taskId, self.id))
                            if not task.get('parent'):
                                self.workTasks[taskId] = task
                                for t in self.workTasks.values():
                                    if t.parent == task.id:
                                        task.subtasks.add(t)
                                        if t.processor and t.processor.running:
                                            if not task.get('cmd') or task.get('cmd') == '':
                                                task.set('cmd','run')
                            elif self.workTasks.has_key(task.get('parent')):
                                self.workTasks[taskId] = task
                                self.workTasks[task.get('parent')].subtasks.add(task)
                            else:
                                task.set('status.stage', 'ignored')
                                task.set('status.error', 'parent task is not in the available to worker')
                                task.set('visible2worker', False)
                                print('ignore task {}/{}, disable it from worker'.format(task.get('name'), task.id))
                    else:
                        task.set('status.error', 'no task processor defined.')
                        return None
                if self.workTasks.has_key(taskId):
                    self.workTasks[taskId].processor.on_update(
                        'cmd', self.execute_task_cmd)
                    self.workTasks[taskId].processor.on_update(
                        'worker', self.task_worker_changed)
                    self.workTasks[taskId].processor.on_remove(
                        self.remove_task)
                    self.execute_task_cmd(
                        self.workTasks[taskId], 'cmd', task.get('cmd'))
                    # if task.get('cmd') == 'run':
                    #    self.run_task(self.workTasks[taskId])
                    return self.workTasks[taskId]
            else:
                print('widget task processor is not available.')
        else:
            if task:
                task.set('visible2worker', False)
            print("widget is not registered: taskid=" + taskId)

    def remove_task(self, task):
        if isinstance(task, str):
            return
        if self.workTasks.has_key(task.id):
            task = self.workTasks[task.id]
            if task.processor.running:
                task.processor.stop()
            # remove this task from parent task
            if task.get('parent') and self.workTasks.has_key(task.get('parent')):
                if task in self.workTasks[task.get('parent')].subtasks:
                    self.workTasks[task.get('parent')].subtasks.remove(task)

            del self.workTasks[task.id]
            print('remove task {} from widget {}'.format(task.id, self.id))

    def execute_task_cmd(self, task, key, cmd):
        self.set('cmd', '')
        if cmd == 'run':
            print('---run task---')
            self.run_task(task)
        elif cmd == 'stop':
            print('---stop task---')
            self.stop_task(task)

    def execute_worker_cmd(self, cmd):
        self.set('cmd', '')
        if cmd == 'run':
            self.start_task_threads()
        elif cmd == 'stop':
            self.stop_task_threads()

    def run_task(self, task):
        id = task.id
        if self.workTasks.has_key(id):
            if self.workTasks[id].processor:
                self.workTasks[id].processor.start()
            else:
                self.taskQueue.put(id)
                task.set('status.stage', 'queued')
                print('task Qsize:' + str(self.taskQueue.qsize()))

    def stop_task(self, task):
        id = task.id
        if self.workTasks.has_key(id):
            if self.workTasks[id].processor.running:
                self.workTasks[id].processor.stop()

    def work_on_task(self, abortEvent):
        import time
        # print('working thread for tasks of widget {} started'.format(self.id))
        while True:
            if abortEvent.is_set():
                break
            try:
                taskId = self.taskQueue.get()
                if self.get('status') != 'running':
                    self.set('status', 'running')
                if self.workTasks.has_key(taskId):
                    task = self.workTasks[taskId]
                    if task.processor:
                        if not task.get('parent'):
                            task.processor.start()
                        elif task.get('parent') and self.workTasks.has_key(task.get('parent')):
                            ptask = self.workTasks[task.get('parent')]
                            if ptask.processor and not ptask.processor.running:
                                task.set('status.stage', 'waiting')
                                ptask.processor.start()
                            task.processor.start()
                        else:
                            task.set('status.stage', 'ignored')
                            task.set('status.error', 'parent task is not in the available to worker')
                            task.set('visible2worker', False)
                            print('ignore task {}/{}, disable it from worker'.format(task.get('name'), task.id))
                            # task.processor.start()
                self.taskQueue.task_done()

            except Empty:
                self.set('status', 'ready')
                time.sleep(1)
            except:
                traceback.print_exc()
            time.sleep(0.5)

        print('working thread for {} stopped'.format(self.id))

    def stop(self):
        try:
            for task in self.workTasks:
                if task.processor.running:
                    task.processor.stop()
        except Exception as e:
            pass
        self.set('status', 'stopped')
        for subscription in self.meteorClient.subscriptions.copy():
            self.meteorClient.unsubscribe(subscription)


class Metrics():

    def __init__(self, type, value, unit=''):
        self.type = type
        self.value = value
        self.unit = unit
        self.__repr__ = self.__str__

    def __str__(self):
        return "{}: {}{}".format(self.type, self.value, self.unit)


class ConnectionManager():

    def __init__(self, server_url='ws://localhost:3000/websocket', worker=None):
        self.client = MeteorClient(server_url)
        self.client.on('subscribed', self.subscribed)
        self.client.on('unsubscribed', self.unsubscribed)
        self.client.on('added', self.added)
        self.client.on('changed', self.changed)
        self.client.on('removed', self.removed)
        self.client.on('connected', self.connected)
        self.client.on('logged_in', self.logged_in)
        self.client.on('logged_out', self.logged_out)
        self.worker = worker
        self.connected = False
        self.ready = False

    def connect(self):
        self.client.connect()

    def connected(self):
        self.connected = True
        print('* CONNECTED')
        #self.client.login('test', '*****')
        if not 'workers.worker' in self.client.subscriptions:
            self.client.subscribe(
                'workers.worker', [self.worker.id, self.worker.token])
        if not 'files.worker' in self.client.subscriptions:
            self.client.subscribe('files.worker', [self.worker.id, self.worker.token]);

    def logged_in(self, data):
        self.userId = data['id']
        print('* LOGGED IN {}'.format(data))

    def subscribed(self, subscription):
        print('* SUBSCRIBED {}'.format(subscription))
        self.ready = True
        if subscription == 'workers.worker':
            if self.client.find_one('workers', selector={'_id': self.worker.id}):
                print('-----Worker {} found-----'.format(self.worker.id))
                if not 'widgets.worker' in self.client.subscriptions:
                    self.client.subscribe(
                        'widgets.worker', [self.worker.id, self.worker.token])
            else:
                raise Exception('Failed to find the worker with id:{} token{}'.format(
                    self.worker.id, self.worker.token))
        if subscription == 'files.worker':
            print('files of this worker SUBSCRIBED-')

        if subscription == 'widgets.worker':
            print('widgets of this worker SUBSCRIBED-')

        elif subscription == 'tasks.worker':
            print('* tasks of this worker SUBSCRIBED-')

    def added(self, collection, id, fields):
        print('* ADDED {} {}'.format(collection, id))
        # for key, value in fields.items():
        #    print('  - FIELD {} {}'.format(key, value))
        if collection == 'tasks':
            if not self.worker.workTasks.has_key(id):
                if fields.has_key('worker') and fields['worker'] == self.worker.id:
                    task = Task(self.client.find_one('tasks', selector={
                                '_id': id}), self.worker, self.client)
                    if task.id:
                        self.worker.add_task(task)

        elif collection == 'users':
            self.userName = fields['username']
        elif collection == 'widgets':
            # widget = fields#self.client.find_one('widgets', selector={'name':
            widget_ = Widget(self.client.find_one(
                'widgets', selector={'_id': id}), self.worker, self.client)
            if widget_.id:
                self.worker.register_widget(widget_)
                if not 'tasks.worker' in self.client.subscriptions:
                    self.client.subscribe(
                        'tasks.worker', [self.worker.id, self.worker.token])

    def changed(self, collection, id, fields, cleared):
        #print('* CHANGED {} {}'.format(collection, id))
        # for key, value in fields.items():
        #    print('  - FIELD {} {}'.format(key, value))
        # for key, value in cleared.items():
        #    print('  - CLEARED {} {}'.format(key, value))
        if collection == 'tasks':
            if self.worker.workTasks.has_key(id):
                task = self.worker.workTasks[id]
                for key, value in fields.items():
                    if task.processor.updateCallbackDict.has_key(key):
                        for updateCallback in task.processor.updateCallbackDict[key]:
                            try:
                                updateCallback(task, key, value)
                            except Exception as e:
                                traceback.print_exc()
                                task.set('status.error', traceback.format_exc())

                for key, value in cleared.items():
                    if task.processor.updateCallbackDict.has_key(key):
                        for updateCallback in task.processor.updateCallbackDict[key]:
                            try:
                                updateCallback(task, key, value)
                            except Exception as e:
                                traceback.print_exc()
                                task.set('status.error', traceback.format_exc())

            else:
                if fields.has_key('worker') and fields['worker'] == self.worker.id:
                    self.worker.add_task(id)

                #print('task is not in worktask list: ' + id)
        if collection == 'widgets':
            widget_ = Widget(self.client.find_one(
                'widgets', selector={'_id': id}), self.worker, self.client)
            if widget_.id:
                self.worker.register_widget(widget_)

            if fields.has_key('workers'):
                if fields['workers'].has_key(self.worker.id):
                    #print('worker config changed')
                    worker = fields['workers'][self.worker.id]
                    if worker.has_key('cmd'):
                        self.worker.execute_worker_cmd(worker['cmd'])

    def removed(self, collection, id):
        #print('* REMOVED {} {}'.format(collection, id))
        if collection == 'tasks':
            if self.worker.workTasks.has_key(id):
                task = self.worker.workTasks[id]
                for cb in task.processor.removeCallbackList:
                    cb(task)

    def unsubscribed(self, subscription):
        print('* UNSUBSCRIBED {}'.format(subscription))

    def logged_out():
        self.userId = None
        print('* LOGGED OUT')

    def subscription_callback(self, error):
        if error:
            print(error)

    def run(self):
        # (sort of) hacky way to keep the client alive
        # ctrl + c to kill the script
        try:
            while True:
                time.sleep(1)
        except:
            traceback.print_exc()
        finally:
            self.stop()
            print('server exited')

    def stop(self):
        try:
            for task in self.worker.workTasks:
                if task.processor:
                    task.processor.stop()
        except Exception as e:
            pass
        self.worker['status'] = 'stopped'
        for subscription in self.client.subscriptions.copy():
            self.client.unsubscribe(subscription)


if __name__ == '__main__':
    '''
    python dsWorker.py --workdir ./workdir --dev --server-url ws://localhost:3000/websocket --worker-id Xkzx4atx6auuxXGfX --worker-token qjygopwdoqvqkzu
    '''
    parser = argparse.ArgumentParser(description='distributed worker')
    parser.add_argument('--worker-id', dest='worker_id',
                        type=str, default='', help='id of the worker')
    parser.add_argument('--thread-num', dest='thread_num',
                        type=int, default=10, help='number of thread for the worker')
    parser.add_argument('--worker-token', dest='worker_token',
                        type=str, default='', help='token of the worker')
    parser.add_argument('--server-url', dest='server_url', type=str,
                        default='ws://localhost:3000/websocket', help='server url')
    parser.add_argument('--workdir', dest='workdir', type=str,
                        default='./workdir', help='workdir')
    parser.add_argument('--dev-mode', dest='dev_mode',
                        action='store_true', help='enable development mode')
    parser.add_argument('--verbose', dest='verbose',
                        action='store_true', help='enable debug logging')
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    dw = Worker(worker_id=args.worker_id, worker_token=args.worker_token, server_url=args.server_url,
                workdir=args.workdir, dev_mode=args.dev_mode, thread_num=args.thread_num)
    dw.start()
