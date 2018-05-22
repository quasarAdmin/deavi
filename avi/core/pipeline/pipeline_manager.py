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
