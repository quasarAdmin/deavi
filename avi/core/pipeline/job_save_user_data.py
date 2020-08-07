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

@package avi.core.pipeline.job_save_user_data

--------------------------------------------------------------------------------

This module provides the save_user_data job.
"""
from .job import job as parent

import time
import os
from django.utils import timezone
from urllib.parse import unquote

from avi.utils.data.file_manager import file_manager
from avi.warehouse import wh_global_config as wh

from avi.log import logger

class save_user_data(parent):
    """@class save_user_data
    The save_user_data class saves a received user file from the client

    It implementes the job interface and inherits the job_data attribute.

    @see job @link avi.core.pipeline.job
    @see job_data @link avi.core.pipeline.job_data
    """
    def start(self, data):
        """This method runs the save_user_data job.

        It will received the user file and it will store it in the user space 
        using the file_manager.

        Args:
        self: The object pointer.
        data: A dictionary containing the user file to be saved.
        
        Returns:
        The job_data attribute. The ok attribure will be True if everything 
        went correctly, False otherwise.
        
        @see file_manager @link avi.utils.data.file_manager.file_manager
        """
        from django.core.files.storage import FileSystemStorage
        fs = FileSystemStorage()
        f = data['file']
        file_name = wh().get().USER_FMT%{"user":"user",
                                         "date":str(round(time.time())),
                                         "name":f.name}
        full_name = os.path.join(wh().get().USER_PATH, file_name)
        filename = fs.save(full_name, f)
        fm = file_manager()
        fm.save_file_info(f.name, full_name, -1, "user", timezone.now())
        self.job_data.ok = True
        self.job_data.data = {}
        self.job_data.data['status'] = 'success'
        return self.job_data
