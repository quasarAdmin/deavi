
from .job import job as parent

from avi.log import logger

class get_algorithm(parent):
    def start(self, data):
        log = logger().get_log('views')
        log.info(data)
        from avi.core.algorithm.algorithm_manager import algorithm_manager
        res = algorithm_manager().get_algorithm(data)
        self.job_data.data = {}
        self.job_data.ok = True
        return self.job_data
