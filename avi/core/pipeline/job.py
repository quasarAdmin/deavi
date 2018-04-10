
from abc import ABCMeta, abstractmethod

class job_data:
    data = None
    ok = False

class job(object):
    __metaclass__=ABCMeta

    job_data = job_data()
    
    @abstractmethod
    def start(self, data):
        pass
