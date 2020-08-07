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

@package avi.core.pipeline.pipeline_manager

--------------------------------------------------------------------------------

This module provides the pipeline_manager.
"""
from avi.log import logger

from avi.warehouse import wh_global_config

from .job_factory import job_factory
from .job import job

class pipeline_manager:
    """@class pipeline_manager
    The pipeline_manager class provides a manager for the pipeline.

    It basically starts job using the job_factory and provides error control.
    """
    ## Log header
    str_log_header = 'pipeline_manager'
    
    ## Log
    log = None
    
    def __init__(self):
        """The pipeline_manager constructor
        
        The constructor basically starts the log.
        
        Args:
        self: The object pointer.
        """
        self.log = logger().get_log(self.str_log_header)

    def start_job(self, name, data):
        """This method starts a new job.

        This method starts a new job using the job_factory.

        Args:
        self: The object pointer.
        name: The name of the job to be stared.
        data: The data to be pass as parameter to the job.

        Returns:
        None if the job could not be started, otherwise it will return the 
        result of the start of the job.
        """
        new_job = None
        if wh_global_config().get().CONTAINER_NAME == 'deavi':
            self.log.info('Starting deavi job')
            new_job = job_factory().get_deavi(name)
        elif wh_global_config().get().CONTAINER_NAME == 'gavip':
            self.log.info('Starting avi job')
            new_job = job_factory().get_avi(name)

        if not new_job:
            self.log.error('Error while initializing the job.')
            return None
        return new_job.start(data = data)
