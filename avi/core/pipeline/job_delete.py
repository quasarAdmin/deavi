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

@package avi.core.pipeline.job_delete

--------------------------------------------------------------------------------

This module provides the delete job.
"""
from .job import job as parent

import os

from avi.models import algorithm_model
from avi.models import gaia_query_model
from avi.models import herschel_query_model
from avi.models import plot_model
from avi.models import results_model
from avi.models import resource_model

from avi.log import logger

class delete(parent):
    """@class delete
    The delete class provides the delete asynchronous job feature.
    
    It implementes the job interface and inherits the job_data attribute.

    @see job @link avi.core.pipeline.job
    @see job_data @link avi.core.pipeline.job_data
    """
    def start(self, data):
        """This method runs the delete job.

        This method will delete the asynchronous job provided in the data 
        parameter.

        The data parameter must have the key 'pk' containing the primary key of 
        the job to be aborted and the key 'type' containing the type of 
        asynchronous job to be aborted.

        It will first check if the job of the given type and with the given pk 
        exists and if so, it will delete it if the job is aborted or its state 
        is 'SUCCESS' or 'FAILURE'.

        If the type is 'algorithm' it will also delete all the results and 
        plots associated with it.

        Args:
        self: The object pointer.
        data: A dictorianry containing the input data for the job.

        Returns:
        The job_data attribute. The ok attribute will be True if the job has 
        been deleted, False otherwise.
        """
        log = logger().get_log("views")
        log.info("inside delete job")
        dtype = data['type']
        pk = data['pk']
        #data['delete-data'] = 'asd'
        if 'delete-data' in data:
            del_data = data['delete-data']
        else:
            del_data = False
        if dtype == 'algorithm':
            m = algorithm_model.objects.get(pk=pk)
            
        if dtype == 'gaia':
            m = gaia_query_model.objects.get(pk=pk)
        
        if dtype == 'hsa':
            m = herschel_query_model.objects.get(pk=pk)
        
        self.job_data.data = {}
        self.job_data.ok = m is not None
        if not m:
            return self.job_data
            
        log.info("deleting_job")
        log.info(m.request.pipeline_state.state)
        if m.request.pipeline_state.state == 'SUCCESS' or \
           m.request.pipeline_state.state == 'FAILURE' or \
           m.is_aborted:
            log.info("deleting job...")
            
            if dtype == 'algorithm':
                plots = plot_model.objects.filter(job_id=pk)
                for p in plots:
                    p.delete()
                results = results_model.objects.filter(job_id=pk)
                for r in results:
                    r.delete()
                rs = resource_model.objects.filter(job_id=pk)
                for r in rs:
                    full_path = os.path.join(r.path, r.name)
                    os.remove(full_path)
                    rs.delete()
            else:
                if del_data != False:
                    resources = resource_model.objects.filter(job_id=pk)
                    for r in resources:
                        full_path = os.path.join(r.path, r.name)
                        os.remove(full_path)
                        r.delete()
            m.request.pipeline_state.delete()
            m.request.delete()
            m.delete()
                

            return self.job_data
            
        return self.job_data
