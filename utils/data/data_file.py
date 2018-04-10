
import os
import traceback
from django.utils import timezone

from avi.log import logger

from avi.warehouse import wh_global_config as wh
from avi.models import results_model
from .file_manager import file_manager

# TODO: add timestamp in the file name?
class data_file:

    task_name = "TODO"
    res = None
    log = None
    def __init__(self, id):
        self.log = logger().get_log('data_file')
        try:
            self.log.info("getting results")
            self.res = results_model.objects.get(job_id=id)
        except results_model.DoesNotExist:
            self.log.info("Creating results")
            self.res = results_model(job_id=id)
            self.res.save()

    def file(self, file_name, type=None):
        fm = file_manager()
        path = wh().get().RESULTS_PATH
        full_name = os.path.join(path, file_name)
        ret = None
        if type == "b":
            ret = open(full_name, "wb")
        else:
            ret = open(full_name, "w")
        model = fm.save_file_info(full_name, self.res.job_id, 
                                  self.task_name, timezone.now())
        self.res.resources.add(model)
        return ret

    def add_plot(self, plot):
        self.res.plots.add(plot)
                          
    def save_fits(self, fname, data):
        fm = file_manager()
        path = wh().get().RESULTS_PATH
        full_name = os.path.join(path, fname)
        
        model = fm.save_file_info(full_name, self.res.job_id,
                                  self.task_name, timezone.now())

        self.res.resources.add(model)
        data.writeto(full_name)
    
    def save_vot(self, fname, data):
        fm = file_manager()
        path = wh().get().RESULTS_PATH
        full_name = os.path.join(path, fname)
        
        model = fm.save_file_info(full_name, self.res.job_id,
                                  self.task_name, timezone.now())

        self.res.resources.add(model)
        data.to_xml(full_name)
