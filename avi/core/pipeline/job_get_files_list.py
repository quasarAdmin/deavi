"""
Copyright (C) 2016-2020 Quasar Science Resources, S.L.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.

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
