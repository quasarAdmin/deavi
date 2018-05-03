"""
Copyright (C) 2016-2018 Quasar Science Resources, S.L.

This file is part of DEAVI.

DEAVI is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

DEAVI is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with DEAVI.  If not, see <http://www.gnu.org/licenses/>.
"""
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
