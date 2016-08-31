from .worker import Worker
from .taskProcessors import TaskProcessor, ThreadedTaskProcessor, ProcessTaskProcessor
def import(name):
    execfile(name+'py')
