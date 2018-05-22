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

@package avi.core.pipeline.job_get_files_list

--------------------------------------------------------------------------------

This module provides the get_files_list job.
"""
from .job import job as parent

from avi.core.algorithm.algorithm_manager import algorithm_manager
from avi.models import algorithm_info_model
from avi.models import resource_model


from avi.log import logger

class get_files_list(parent):
    """@class get_files_list
    The get_files_list class provides the names of all the files in the system
    
    It implementes the job interface and inherits the job_data attribute.

    @see job @link avi.core.pipeline.job
    @see job_data @link avi.core.pipeline.job_data
    """
    def start(self, data):
        """This method runs the get_files_list job.

        This method retrieves all the resource_models.

        Args:
        self: The object pointer.
        data: A dictorianry containing the input data for the job.

        Returns:
        The job_data attribute. The ok attribute will be True if there are 
        files retrieved, False otherwise.

        @see resource_model @link avi.models.resource_model
        """
        log = logger().get_log('algorithm_manager')
        
        ms = resource_model.objects.all()
        
        self.job_data.ok = ms is not None
        if not ms:
            self.job_data.data = None
            return self.job_data

        return self.job_data
