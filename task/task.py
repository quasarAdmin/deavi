
from abc import ABCMeta, abstractmethod

class task_exception(Exception):
    def __init__(self, msg):
        self.message = msg

class task_data:
    data = None

class task(object):
    __metaclass__=ABCMeta

    task_data = task_data()
    task_id = None
    
    @abstractmethod
    def output(self):
        pass

    @abstractmethod
    def run(self):
        pass
