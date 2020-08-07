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

@package avi.core.pipeline.job_get_results

--------------------------------------------------------------------------------

This module provides the get_query_status job.
"""
from .job import job as parent

from avi.models import gaia_query_model
from avi.models import herschel_query_model
from avi.models import resource_model

from avi.log import logger

class get_query_status(parent):
    """@class get_query_info
    The get_query_status class retrieves the status of a specific query execution.

    It implementes the job interface and inherits the job_data attribute.

    @see job @link avi.core.pipeline.job
    @see job_data @link avi.core.pipeline.job_data
    """
    def start(self, data):
        """This method runs the get_query_status job.

        The data parameter must be a tupla of the primary key of the query 
        execution and an identifier of the mission.

        The method will retrieve the status of the given query.

        Args:
        self: The object pointer.
        data: A dictionary containing the input data for the job.

        Returns:
        The job_data attribute. The ok attribute will be True if the 
        information was retrieved correctly, False otherwise.

        @see results_model @link avi.models.results_model
        """
        log = logger().get_log("views")
        if data.get('mission') == 'gaia':
            #m = gaia_query_model.objects.all.filter(pk=data['id'])
            #m = gaia_query_model.objects.all
            m = gaia_query_model.objects.get(pk=data['id'])
            if m == None:
                self.job_data.ok = False
                return self.job_data
            self.job_data.ok = True
            self.job_data.data = m.request.pipeline_state.state
            return self.job_data
            
        if  data.get('mission') == 'hsa':
            m = herschel_query_model.objects.get(pk=data['id'])
            if m == None:
                self.job_data.ok = False
                return self.job_data
            self.job_data.ok = True
            self.job_data.data = m.request.pipeline_state.state
            return self.job_data