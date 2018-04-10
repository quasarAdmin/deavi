
from .job import job as parent

from avi.models import algorithm_model
from avi.models import gaia_query_model
from avi.models import herschel_query_model

from avi.log import logger

class abort(parent):
    def start(self, data):
        log = logger().get_log("views")
        log.info("inside the job")
        if data['type'] == 'algorithm':
            m = algorithm_model.objects.get(pk=data['pk'])
            
        if data['type'] == 'gaia':
            m = gaia_query_model.objects.get(pk=data['pk'])
        
        if data['type'] == 'hsa':
            m = herschel_query_model.objects.get(pk=data['pk'])
        
        self.job_data.data = {}
        self.job_data.ok = m is not None
        if not m:
            return self.job_data
            
        log.info("abandon_job")
        log.info(m.request.pipeline_state.state)
        if m.request.pipeline_state.state == 'SUCCESS' or \
           m.request.pipeline_state.state == 'FAILURE' or \
           m.is_aborted:
            return self.job_data
            
        log.info("aborting job...")
            
        m.request.abandon_job('User request')    
        m.is_aborted = True
        m.request.delete_job_task()
        log.info(m.request.pipeline_state.state)
        m.request.pipeline_state.save()
        m.request.save()
        m.save()
        return self.job_data
