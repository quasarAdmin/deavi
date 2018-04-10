
from avi.log import logger

from avi.warehouse import wh_global_config

from .job_factory import job_factory
from .job import job

class pipeline_manager:

    str_log_header = 'pipeline_manager'
    
    log = None
    
    def __init__(self):
        self.log = logger().get_log(self.str_log_header)

    def start_job(self, name, data):
        new_job = None
        if wh_global_config().get().CONTAINER_NAME == 'deavi':
            self.log.info('Starting deavi job')
            new_job = job_factory().get_deavi(name)
        elif wh_global_config().get().CONTAINER_NAME == 'gavip':
            self.log.info('Starting avi job')
            new_job = job_factory().get_avi(name)

        if not new_job:
            self.log.error('Error while initializing the job.')
            return None

        return new_job.start(data = data)
