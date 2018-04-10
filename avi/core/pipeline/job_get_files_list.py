
from .job import job as parent

from avi.core.algorithm.algorithm_manager import algorithm_manager
from avi.models import algorithm_info_model
from avi.models import resource_model


from avi.log import logger

class get_files_list(parent):
    def start(self, data):
        log = logger().get_log('algorithm_manager')
        
        ms = resource_model.objects.all()
        
        self.job_data.ok = ms is not None
        if not ms:
            self.job_data.data = None
            return self.job_data

        return self.job_data
