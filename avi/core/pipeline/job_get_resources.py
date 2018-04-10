
from .job import job as parent

from avi.models import resource_model
from avi.warehouse import wh_global_config as wh
from avi.log import logger

class get_resources(parent):
    def start(self, data):
        ms = resource_model.objects.all()
        data = {}
        gaia = {}
        hsa = {}
        data['gaia'] = gaia
        data['hsa'] = hsa
        for q in ms:
            if q.file_type == 'gaia':
                gaia[q.name] = q.name
            elif q.file_type == 'hsa':
                hsa[q.name] = q.name
        self.job_data.ok = True
        self.job_data.data = data
        return self.job_data
