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

@package avi.core.pipeline.job_delete_file

--------------------------------------------------------------------------------

This module provides the delete file job.
"""
from .job import job as parent

import os
from avi.models import resource_model

from avi.log import logger

class delete_file(parent):
    """@class delete
    The delete_file class provides the delete file feature.
    
    It implementes the job interface and inherits the job_data attribute.

    @see job @link avi.core.pipeline.job
    @see job_data @link avi.core.pipeline.job_data
    """
    def start(self, data):
        """This method runs the delete file job.

        This method will delete file provided in the data 
        parameter.

        The data parameter must have the key 'pk' containing the primary key of 
        the resource to be deleted.

        It will first check if the resource of the given pk 
        exists and if so, it will delete it.

        It will also delete the file from disk.

        Args:
        self: The object pointer.
        data: A dictorianry containing the input data for the job.

        Returns:
        The job_data attribute. The ok attribute will be True if the resource has 
        been deleted, False otherwise.
        """
        log = logger().get_log("views")
        log.info("inside delete file job")
        pk = data['pk']
        
        m = resource_model.objects.get(pk=pk)

        self.job_data.data = {}
        self.job_data.ok = m is not None
        if not m:
            return self.job_data
            
        path = m.path
        name = m.name

        m.delete()

        full_path = os.path.join(path, name)
        os.remove(full_path)
            
        return self.job_data
