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

@package avi.core.pipeline.job_abort

--------------------------------------------------------------------------------

This module provides the abort job.
"""
from .job import job as parent

from avi.models import algorithm_model
from avi.models import gaia_query_model
from avi.models import herschel_query_model

from avi.log import logger

class abort(parent):
    """@class abort
    The abort class provides the abort asynchronous job feature.
    
    It implementes the job interface and inherits the job_data attribute.

    @see job @link avi.core.pipeline.job
    @see job_data @link avi.core.pipeline.job_data
    """
    def start(self, data):
        """This method runs the abort job.

        This method will abort the asynchronous job provided in the data 
        parameter.

        The data parameter must have the key 'pk' containing the primary key of 
        the job to be aborted and the key 'type' containing the type of 
        asynchronous job to be aborted.

        It will first check if the job of the given type and with the given pk 
        exists and if so, it will abort it unless it is already or its state is 
        'SUCCESS' or 'FAILURE'.

        Args:
        self: The object pointer.
        data: A dictorianry containing the input data for the job.

        Returns:
        The job_data attribute. The ok attribute will be True if the job has 
        been aborted, False otherwise.
        """
        log = logger().get_log("views")
        log.info("inside the job")
        if data['type'] == 'algorithm':
            m = algorithm_model.objects.get(pk=data['pk'])
            
        if data['type'] == 'gaia':
            m = gaia_query_model.objects.get(pk=data['pk'])
        
        if data['type'] == 'hsa':
            m = herschel_query_model.objects.get(pk=data['pk'])
        
        self.job_data.data = {}
        self.job_data.ok = m is not None
        if not m:
            return self.job_data
            
        log.info("abandon_job")
        log.info(m.request.pipeline_state.state)
        if m.request.pipeline_state.state == 'SUCCESS' or \
           m.request.pipeline_state.state == 'FAILURE' or \
           m.is_aborted:
            return self.job_data
            
        log.info("aborting job...")
            
        m.request.abandon_job('User request')    
        m.is_aborted = True
        m.request.delete_job_task()
        log.info(m.request.pipeline_state.state)
        m.request.pipeline_state.save()
        m.request.save()
        m.save()
        return self.job_data
