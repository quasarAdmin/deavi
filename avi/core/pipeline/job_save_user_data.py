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
        fm.save_file_info(full_name, -1, "user", timezone.now())
        self.job_data.ok = True
        self.job_data.data = {}
        self.job_data.data['status'] = 'success'
        return self.job_data
