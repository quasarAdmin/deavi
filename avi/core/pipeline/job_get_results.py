
from .job import job as parent

from avi.models import results_model
from avi.log import logger

class get_results(parent):
    def start(self, data):
        log = logger().get_log("views")
        log.info("%s",str(data))
        ms = results_model.objects.filter(job_id=data)
        if not ms:
            log.info("no results")
            self.job_data.ok = False
            self.job_data.data = None
            return self.job_data
        log.info("results %s",data)
        model = ms[0]
        ret = {}
        plots = {}
        resources = {}
        ret['plots'] = plots
        ret['resources'] = resources
        for p in model.plots.all():
            log.info("%s",str(p.job_id))
            plots[p.pk] = p.pk #(p.script, p.html)
        for r in model.resources.all():
            log.info("%s",str(r.name))
            resources[r.pk] = r.name
        self.job_data.ok = True
        self.job_data.data = ret
        return self.job_data
