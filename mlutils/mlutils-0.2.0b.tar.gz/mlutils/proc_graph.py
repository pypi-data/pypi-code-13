#!/usr/bin/python
""" Implementation of processing graph on base of generic directed basic_graph.   
    Link from Node A to Node B represent dependency of Node A from Node B 
        and Node A will be waiting for data from Node B 
    Processing could be run given number of iterations : ProcGraph.run(N)
    or until some tasl return 'None' as a request to finish processing 
"""
from mlutils import basic_graph as bg
import copy as cp
import Queue as que
import thread as thr
import time

print_lock = thr.allocate_lock()

def sync_print(message, *args):
    print_lock.acquire()
    print message%args
    print_lock.release()              
   
class ProcNode(bg.BasicNode):
    """ Processing node, represent processing task 
    Task object should have methods:
        init()
        process(**kwargs), should return not 'None' to proceed to next iteration.
        finish()
    init() and finish() are optional, process(**kwargs) is requared.
    process(**kwargs) should return not 'None' to proceed on next iteration. 
    If it return 'None' execution of this task and all dependent tasks will be stopped,
    but tasks which do not depend on this task will continue running
    Alternatively you can inherit from ProcNode and overwrite these methods 
    """
    def __init__(self, task_object):
        super(ProcNode, self).__init__()
        self._task = task_object
        
    def __str__(self):
        return "%s, task : %s " % (type(self), str(self.task)) 
    
    def task(self):
        return self._task
    
    def init(self):
        if callable(getattr(self._task, "init", None)):
            self._task.init()        
    
    def process(self, **kwargs):
        return self._task.process(**kwargs)        
    
    def finish(self):
        if callable(getattr(self._task, "finish", None)):
            self._task.finish()    
    
class ProcGraph(bg.BasicGraph):
    """ Processing network 
    """ 
    DefQueueSize = 10
    DefQueueTimeout = 10
    class Link(bg.BasicGraph.Link):
        """ Dependency link, data queue container
        """        
        def __init__(self, graph):
            bg.BasicGraph.Link.__init__(self, graph)
            self.queue = que.Queue(self._graph._queue_size)
            
        def put(self, data):
            try:
                self.queue.put(data, True, self._graph._queue_timeout)
            except que.Full:
                linked = self._graph.get_linked_labels(self)
                self._graph.stop("Error: queue '%s'=>'%s' is full", linked[1], linked[0])
                                     
        def get(self):
            try:
                return self.queue.get(True, self._graph._queue_timeout)
            except que.Empty:
                linked = self._graph.get_linked_labels(self)
                self._graph.stop("Error: data '%s'<='%s' timeout", linked[0], linked[1])                

    def __init__(self, name, queue_size = None, queue_timeout = None):
        """ Init ProcGraph object
        params:
            queue_size - depth of the data queue between nodes
            queue_timeout - wait time for get/put data in queue before through error
        """
        super(ProcGraph, self).__init__(name)
        self._join_queue = que.Queue()
        self._stop_graph = False
        if queue_size is None:
            self._queue_size = ProcGraph.DefQueueSize
        else:
            self._queue_size = queue_size
        if queue_timeout is None:
            self._que_timeout = ProcGraph.DefQueueTimeout
        else:
            self._queue_timeout = queue_timeout
                    
    def run(self, iteration_num = None):
        """ Launch every node in separate thread. 
        params: 
            iteration_num - number of iteration for each node. 
            If 'None' run infinitely until receive or return 'None'
        """
        idents = {}
        sync_print("ProcGraph: start...")
        for label in self.get_labels():
            try:
                ident = thr.start_new_thread(self.node_proc_thread,(label, iteration_num))
                idents[ident] = label
            except:
                sync_print("Failed to start threadfor node %s.", label)
        # wait to join all threads
        while len(idents) > 0:
            ident = self._join_queue.get() 
            sync_print("Node %s stop.", idents[ident])  
            del idents[ident]
        # clean-up
        sync_print("ProcGraph: finish.")
        
        
    def stop(self, message, *args):
        """ Stop graph, print error message
        """
        self._stop_graph = True
        sync_print(message, *args)
              
    def node_proc_thread(self, label, iteration_num):
        """ Thread function for execution node task. 
        It invokes task.init() if exist
        then execute task.process(**kwargs) given number of iteration or
            until it recieve 'None' as an argumwent or return 'None'
        then invoke task.finish() if exist
        """
        node = self.get_node(label)
        # init task
        node.init()
        # process 
        finish = False
        while not self._stop_graph and iteration_num != 0 and not finish:
            kwargs = {} 
            # get data
            for target in self.get_targets(label):
                data = self.get_link(label, target).get()
                if data is not None:
                    kwargs[target] = data
                else:
                    finish = True
                    break
            # process 
            if not finish:
                ret = node.process(**kwargs)
                # push forward    
                for source in self.get_sources(label):
                    self.get_link(source, label).put(cp.deepcopy(ret))
                finish = ret is None 
            # next
            if iteration_num > 0: 
                iteration_num -= 1

        # finish task
        node.finish()
        # join
        self._join_queue.put(thr.get_ident(), False)
        
                
def test():
    class T1:
        def init(self):
            self.cntr = 0
        def process(self):
            time.sleep(1)
            if self.cntr < 10:
                self.cntr += 1
                return self.cntr        
                    
    class T2:
        def process(self, T1):
            time.sleep(1)
            sync_print("T2: %s", T1**2)
            return T1**2

    class T3:
        def process(self, T2, T1):
            time.sleep(1)
            sync_print("T3: %s + %s = %s", T2, T1, T2 + T1)
            return 0

    gr = ProcGraph("Pipenet", 10, 10)
    gr.add_node(ProcNode(T1()), "T1") 
    gr.add_node(ProcNode(T2()), "T2")
    gr.add_node(ProcNode(T3()), "T3")
    gr.link("T2","T1")  
    gr.link("T3","T1")
    gr.link("T3","T2")    
    #gr.display()
    gr.run(5)
       

if __name__ == '__main__':
    test()