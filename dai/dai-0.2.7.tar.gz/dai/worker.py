import time
import sys
import logging
import collections
import threading
import traceback
import os
import platform
import argparse

from MeteorClient import MeteorClient
try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x
from subprocess import Popen, PIPE, STDOUT
from utils import NonBlockingStreamReader, Resource

class Task(object):

    def __init__(self, taskDoc, worker, meteorClient):
        self.taskDoc = taskDoc
        self.worker = worker
        self.meteorClient = meteorClient
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

    def __setitem__(self, key, value):
        if key == "visible2worker" and value == False:
            vdict = {key: value, "status.running": False}
        elif self.processor and self['status.running'] != self.processor.running:
            vdict = {key: value, "status.running": self.processor.running}
        else:
            vdict = {key: value}
        self.meteorClient.call('tasks.update.worker', [
                               self.id, self.worker.id, self.worker.token, {'$set': vdict}])


    def __getattr__(self, attr):
        if attr in ['taskDoc', 'id', 'processor', 'worker', 'subtasks', 'meteorClient', 'has_key']:
            return super(Task, self).__getattribute__(attr)
        if self.taskDoc.has_key(attr):
            return self.taskDoc[attr]
        else:
            return None

    def __setattr__(self, key, value):
        if key in ['taskDoc', 'id', 'processor', 'worker', 'subtasks', 'meteorClient', 'has_key']:
            super(Task, self).__setattr__(key, value)
        else:
            self.__setitem__(key, value)

    def __delattr__(self, item):
        self.__delitem__(item)

    def push(self, key, value):
        self.meteorClient.call('tasks.update.worker', [
                               self.id, self.worker.id, self.worker.token, {'$push': {key: value}}])

    def pull(self, key, value):
        self.meteorClient.call('tasks.update.worker', [
                               self.id, self.worker.id, self.worker.token, {'$pull': {key: value}}])


class Widget(object):

    def __init__(self, widgetDoc, meteorClient):
        self.widgetDoc = widgetDoc
        self.meteorClient = meteorClient
        self.has_key = self.widgetDoc.has_key
        if self.widgetDoc.has_key('_id'):
            self.id = self.widgetDoc['_id']
        else:
            self.id = None

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

    def __getattr__(self, attr):
        if attr in ['widgetDoc', 'id', 'has_key', 'meteorClient']:
            return super(Widget, self).__getattribute__(attr)
        if self.widgetDoc.has_key(attr):
            return self.widgetDoc[attr]
        else:
            return None

    def __setattr__(self, key, value):
        if key in ['widgetDoc', 'id', 'has_key', 'meteorClient']:
            super(Widget, self).__setattr__(key, value)
        else:
            self.__setitem__(key, value)

    def __delattr__(self, item):
        self.__delitem__(item)

    def exec_widget_task_processor(self, task, widget, worker):
        import time
        id = widget._id
        widget_task_processor = self.default_task_processor
        ns = {'TASK': task, 'WIDGET': widget,
              'WORKER': worker, '__name__': '__worker__', 'time': time}
        exec(widget['code_snippets']['__init___py']['content'], ns)
        if ns.has_key('TASK_PROCESSOR'):
            return ns['TASK_PROCESSOR']
        else:
            return None

    def default_task_processor(self, task, widget, worker):
        print('default_task_processor: ' + task._id)

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

        self.workdir = os.path.abspath(os.path.join(workdir, worker_id))
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
        self['version'] = self.workerVersion
        self['sysInfo'] = features
        self['name'] = self.resources[
            'platform'].features['node'] + '-' + self.id
        self['status'] = 'ready'
        while True:
            self.get_gpu_resources()
            resources = ''
            for k in self.resources:
                resources += self.resources[k].id + ':\n'
                for s in self.resources[k].status.values():
                    resources += str(s) + '\n'
            self['resources'] = resources
            time.sleep(2.0)

    def register_widget(self, widget):
        id = widget._id
        print('register widget: ' + id)
        if widget.mode == 'development':
            widgetWorkdir = os.path.join(self.workdir, id)
            if not os.path.exists(widgetWorkdir):
                os.makedirs(widgetWorkdir)
            self.devWidgets[id] = widget
            if self.productionWidgets.has_key(id):
                del self.productionWidgets[id]

        if widget['mode'] == 'production':
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

    def __setitem__(self, key, value):
        self.meteorClient.call('workers.update', [self.id, self.token, {
                               '$set': {key: value}}], self.default_update_callback)

    def push(self, key, value):
        self.meteorClient.call('workers.update', [self.id, self.token, {
                               '$push': {key: value}}], self.default_update_callback)

    def pull(self, key, value):
        self.meteorClient.call('workers.update', [self.id, self.token, {
                               '$pull': {key: value}}], self.default_update_callback)

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
        taskId = task._id
        if task and task.widgetId and self.is_widget_registered(task.widgetId):
            widget = self.get_registered_widget(task.widgetId)
            task_processor = widget.get_task_processor()
            if task_processor:
                try:
                    #task['status'] = {"stage":'-', "running": False, "error":'', "progress":-1}
                    if not 'autoRestart' in task['tags'] and task['status.running'] == True:
                        task['cmd'] = ''
                        task['status.stage'] = 'interrupted'
                        task['status.running'] = False
                        task['status.error'] = 'worker restarted unexpectedly.'
                    if 'ing' in task['status.stage']:
                        task['status.stage'] = '-'
                    tp = task_processor(task, widget, self)
                except Exception as e:
                    traceback.print_exc()
                    task['status'] = task['status'] or {}
                    task['status.running'] = False
                    task['status.error'] = traceback.format_exc()
                    task['cmd'] = ''
                    task['visible2worker'] = False
                else:
                    if tp:
                        if not self.workTasks.has_key(taskId):
                            print('add task {} to {}'.format(taskId, self.id))
                            if not task.parent:
                                self.workTasks[taskId] = task
                                for t in self.workTasks.values():
                                    if t.parent == task._id:
                                        task.subtasks.add(t)
                                        if t.processor and t.processor.running:
                                            if not task.cmd or task.cmd == '':
                                                task.cmd = 'run'
                            elif self.workTasks.has_key(task.parent):
                                self.workTasks[taskId] = task
                                self.workTasks[task.parent].subtasks.add(task)
                            else:
                                task['status.stage'] = 'ignored'
                                task[
                                    'status.error'] = 'parent task is not in the available to worker'
                                task['visible2worker'] = False
                                print(
                                    'ignore task {}/{}, disable it from worker'.format(task.name, task._id))
                    else:
                        task['status.error'] = 'no task processor defined.'
                        return None
                if self.workTasks.has_key(taskId):
                    self.workTasks[taskId].processor.on_update(
                        'cmd', self.execute_task_cmd)
                    self.workTasks[taskId].processor.on_update(
                        'worker', self.task_worker_changed)
                    self.workTasks[taskId].processor.on_remove(
                        self.remove_task)
                    self.execute_task_cmd(
                        self.workTasks[taskId], 'cmd', task.cmd)
                    # if task['cmd'] == 'run':
                    #    self.run_task(self.workTasks[taskId])
                    return self.workTasks[taskId]
            else:
                print('widget task processor is not available.')
        else:
            if task:
                task['visible2worker'] = False
            print("widget is not registered: taskid=" + taskId)

    def remove_task(self, task):
        if isinstance(task, str):
            return
        if self.workTasks.has_key(task.id):
            task = self.workTasks[task.id]
            if task.processor.running:
                task.processor.stop()
            # remove this task from parent task
            if task.parent and self.workTasks.has_key(task.parent):
                if task in self.workTasks[task.parent].subtasks:
                    self.workTasks[task.parent].subtasks.remove(task)

            del self.workTasks[task.id]
            print('remove task {} from widget {}'.format(task.id, self.id))

    def execute_task_cmd(self, task, key, cmd):
        self['cmd'] = ''
        if cmd == 'run':
            print('---run task---')
            self.run_task(task)
        elif cmd == 'stop':
            print('---stop task---')
            self.stop_task(task)

    def execute_worker_cmd(self, cmd):
        self['cmd'] = ''
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
                task['status.stage'] = 'queued'
                print('task Qsize:' + str(self.taskQueue.qsize()))

    def stop_task(self, task):
        id = task.id
        if self.workTasks.has_key(id):
            if self.workTasks[id].processor.running:
                self.workTasks[id].processor.stop()

    def work_on_task(self, abortEvent):
        import time
        print('working thread for tasks of widget {} started'.format(self.id))
        while True:
            if abortEvent.is_set():
                break
            try:
                taskId = self.taskQueue.get()
                if self['status'] != 'running':
                    self['status'] = 'running'
                if self.workTasks.has_key(taskId):
                    task = self.workTasks[taskId]
                    if task.processor:
                        if not task.parent:
                            task.processor.start()
                        elif task.parent and self.workTasks.has_key(task.parent):
                            ptask = self.workTasks[task.parent]
                            if ptask.processor and not ptask.processor.running:
                                task['status.stage'] = 'waiting'
                                ptask.processor.start()
                            task.processor.start()
                        else:
                            task['status.stage'] = 'ignored'
                            task[
                                'status.error'] = 'parent task is not in the available to worker'
                            task['visible2worker'] = False
                            print(
                                'ignore task {}/{}, disable it from worker'.format(task.name, task._id))
                            # task.processor.start()
                self.taskQueue.task_done()

            except Empty:
                self['status'] = 'ready'
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
        self['status'] = 'stopped'
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
                    if task._id:
                        self.worker.add_task(task)

        elif collection == 'users':
            self.userName = fields['username']
        elif collection == 'widgets':
            # widget = fields#self.client.find_one('widgets', selector={'name':
            widget_ = Widget(self.client.find_one(
                'widgets', selector={'_id': id}), self.client)
            if widget_._id:
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
                                task['status.error'] = traceback.format_exc()

                for key, value in cleared.items():
                    if task.processor.updateCallbackDict.has_key(key):
                        for updateCallback in task.processor.updateCallbackDict[key]:
                            try:
                                updateCallback(task, key, value)
                            except Exception as e:
                                traceback.print_exc()
                                task['status.error'] = traceback.format_exc()

            else:
                if fields.has_key('worker') and fields['worker'] == self.worker.id:
                    self.worker.add_task(id)

                #print('task is not in worktask list: ' + id)
        if collection == 'widgets':
            widget_ = Widget(self.client.find_one(
                'widgets', selector={'_id': id}), self.client)
            if widget_._id:
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
