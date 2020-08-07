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

@package avi.core.pipeline.job_delete

--------------------------------------------------------------------------------

This module provides the delete job.
"""
from .job import job as parent

import os

from avi.models import algorithm_model
from avi.models import gaia_query_model
from avi.models import herschel_query_model
from avi.models import sim_query_model
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

        if dtype == 'sim':
            m = sim_query_model.objects.get(pk=pk)
        
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
                if del_data != False:
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
                    results = results_model.objects.filter(job_id=pk)
                    plots = plot_model.objects.filter(job_id=pk)
                    for r in results:
                        for p in plots:
                                r.plots.remove(p)
                    for p in plots: 
                        p.delete()
                    
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
