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

@package avi.utils.data.data_file

--------------------------------------------------------------------------------

This module provides an interface to the file management
"""
import os
import time
import traceback
from django.utils import timezone

from avi.log import logger

from avi.warehouse import wh_global_config as wh
from avi.models import results_model
from .file_manager import file_manager

# TODO: add timestamp in the file name?
class data_file:
    """@class data_file
    This class provides an interface to the files management

    This interfaces is used by the algorithm scripts
    """
    ## The task name, NOT USED YET
    task_name = "result"
    ## An instance of the results_model
    res = None
    ## The log
    log = None
    def __init__(self, id):
        """Constructor
        
        Initializes the log and sets the 'res' attribute retrieving the 
        results_model associated with the given id.

        If the results_model does not exist then a new model it is created.

        Args:
        self: The object pointer
        id: The job_id associated with the results_model
        
        See:
        results_model: avi.models.results_model
        """
        self.log = logger().get_log('data_file')
        try:
            self.log.info("getting results")
            self.res = results_model.objects.get(job_id=id)
        except results_model.DoesNotExist:
            self.log.info("Creating results")
            self.res = results_model(job_id=id)
            self.res.save()

    def file(self, file_name, type=None):
        """Creates a new file

        Creates a new file with the given characteristics and saves the file 
        information in the 'res' attribute
        
        Args:
        self: The object pointer
        file_name: The name of the file
        type: The file's type

        Returns:
        A python file object
        
        See:
        results_model: avi.models.results_model
        """
        fm = file_manager()
        path = wh().get().RESULTS_PATH
        fname = wh().get().RESULTS_FMT%{"task":"res",
                                        "date":str(round(time.time())),
                                        "name": file_name}
        full_name = os.path.join(path, fname)
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
        """Adds the given plot to 'res'

        Adds the given plot to the results stored in 'res'

        Args:
        self: The object pointer
        plot: The plot to be saved

        See:
        results_model: avi.models.results_model
        """
        self.res.plots.add(plot)
                          
    def save_fits(self, fname, data):
        """Saves a FITS file
        
        Saves the given data in a FITS file and saves the file information in 
        the results_model stored in 'res'

        Args:
        self: The object pointer
        fname: The name of the file to be saved
        data: The data to be saved

        See:
        results_model: avi.models.results_model
        """
        fm = file_manager()
        path = wh().get().RESULTS_PATH
        full_name = os.path.join(path, fname)
        
        model = fm.save_file_info(full_name, self.res.job_id,
                                  self.task_name, timezone.now())

        self.res.resources.add(model)
        data.writeto(full_name)
    
    def save_vot(self, fname, data):
        """Saves a VOTable file
        
        Saves the given data in a VOTable file and saves the file information 
        in the results_model stored in 'res'

        Args:
        self: The object pointer
        fname: The name of the file to be saved
        data: The data to be saved

        See:
        results_model: avi.models.results_model
        """
        fm = file_manager()
        path = wh().get().RESULTS_PATH
        full_name = os.path.join(path, fname)
        
        model = fm.save_file_info(full_name, self.res.job_id,
                                  self.task_name, timezone.now())

        self.res.resources.add(model)
        data.to_xml(full_name)
