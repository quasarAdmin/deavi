
from .job import job as parent

from avi.models import algorithm_model
from avi.models import gaia_query_model
from avi.models import herschel_query_model
from avi.models import plot_model
from avi.models import results_model

from avi.log import logger

class delete(parent):
    def start(self, data):
        log = logger().get_log("views")
        log.info("inside delete job")
        dtype = data['type']
        pk = data['pk']
        if dtype == 'algorithm':
            m = algorithm_model.objects.get(pk=pk)
            
        if dtype == 'gaia':
            m = gaia_query_model.objects.get(pk=pk)
        
        if dtype == 'hsa':
            m = herschel_query_model.objects.get(pk=pk)
        
        self.job_data.data = {}
        self.job_data.ok = m is not None
        if not m:
            return self.job_data
            
        log.info("deleting_job")
        log.info(m.request.pipeline_state.state)
        if m.request.pipeline_state.state == 'SUCCESS' or \
           m.request.pipeline_state.state == 'FAILURE' or \
           m.is_aborted:
            log.info("deleting job...")
            
            if dtype == 'algorithm':
                plots = plot_model.objects.filter(job_id=pk)
                for p in plots:
                    p.delete()
                results = results_model.objects.filter(job_id=pk)
                for r in results:
                    r.delete()
            m.request.pipeline_state.delete()
            m.request.delete()
            m.delete()
                

            return self.job_data
            
        return self.job_data
