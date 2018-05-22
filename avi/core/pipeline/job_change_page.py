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

@package avi.core.pipeline.job_change_page

--------------------------------------------------------------------------------

This module provides the change page job.
"""
from .job import job as parent

from avi.log import logger
from avi.warehouse import wh_frontend_config

class change_page(parent):
    """@class change_page
    The change_page class changes the current page to the given page.
    
    It implementes the job interface and inherits the job_data attribute.

    @see job @link avi.core.pipeline.job
    @see job_data @link avi.core.pipeline.job_data
    """
    def start(self, data):
        """This method runs the change page job.

        This methods changes the current page storaged in the 
        wh_frontend_config warehouse.

        The data parameter must have the key 'page' containing the name of 
        the web page whose page number will change. It must have also the 
        key 'number' with the number of the page.

        Here we just change the current page in the warehouse, without checking 
        if it is valid or not. Those error controls will be made in other jobs.

        Args:
        self: The object pointer.
        data: A dictorianry containing the input data for the job.

        Returns:
        The job_data attribute. The ok attribute will be True always.

        @see wh_frontend_config @link avi.warehouse.wh_frontend_config
        """
        #log = logger().get_log('get_queries_status')
        wh = wh_frontend_config().get()
        if data['page'] == "pipeline_status":
            wh.CURRENT_EXEC_PAGE = int(data['number'])
            
        if data['page'] == "query_status":
            wh.CURRENT_QUERY_PAGE = int(data['number'])

        if data['page'] == "algorithm":
            wh.CURRENT_ALG_PAGE = int(data['number'])

        if data['page'] == "resources":
            wh.CURRENT_RESOURCES_PAGE = int(data['number'])

        if data['page'] == "results":
            wh.CURRENT_RESULTS_PAGE = int(data['number'])

        self.job_data.data = {}
        self.job_data.ok = True
        return self.job_data
