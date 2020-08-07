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
