
from .job import job as parent

from avi.models import plot_model
from avi.log import logger

class get_plot(parent):
    def start(self, data):
        ms = plot_model.objects.filter(pk=data)
        if not ms:
            self.job_data.ok = False
            self.job_data.data = None
            return self.job_data
        
        ret = {}
        ret['html'] = ms[0].html
        ret['sc'] = ms[0].script
        self.job_data.ok = True
        self.job_data.data = ret
        return self.job_data
