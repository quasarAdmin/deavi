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

@package avi.core.pipeline.job_get_pipeline_status

--------------------------------------------------------------------------------

This module provides the get_pipeline_status job.
"""
from .job import job as parent

from django.core.paginator import Paginator

from avi.models import algorithm_model
from avi.warehouse import wh_frontend_config

from avi.log import logger

class get_pipeline_status(parent):
    """@class get_pipeline_status
    The get_pipeline_status class retrieves the status of the pipeline.

    It implementes the job interface and inherits the job_data attribute.

    @see job @link avi.core.pipeline.job
    @see job_data @link avi.core.pipeline.job_data
    """
    def start(self, data):
        """This method runs the get_pipeline_status job.

        This method will retrieve the algorithm_models and it will sort them 
        by the current sorting method provided by the wh_frontend_config 
        warehouse.

        Then it will paginate the results with current page retrieved from 
        the wh_frontend_config warehouse.

        Args:
        self: The object pointer.
        data: A dictorianry containing the input data for the job.

        Returns:
        The job_data attribute. The ok attribute provides the pages information.

        @see algorithm_model @link avi.models.algorithm_model
        @see wh_frontend_config @link avi.warehouse.wh_frontend_config
        """
        log = logger().get_log("get_pipeline_status")
        wh = wh_frontend_config().get()
        sorting_wh = wh.SORTING_EXEC_BY
        order_by = 'request__pipeline_state__started_time'
        if sorting_wh == 'name':
            order_by = 'alg_name'
        elif sorting_wh == '-name':
            order_by = '-alg_name'
        elif sorting_wh == '-date':
            order_by = '-request__pipeline_state__started_time'
        elif sorting_wh == 'status':
            order_by = 'request__pipeline_state__state'
        elif sorting_wh == '-status':
            order_by = '-request__pipeline_state__state'
            
        all_ms = algorithm_model.objects.all().order_by(order_by,'pk')
        
        self.job_data.data = {}
        self.job_data.ok = all_ms is not None
        if not all_ms:
            self.job_data.ok = False
            return self.job_data

        pg = Paginator(all_ms, wh.MAX_EXEC_PER_PAGE)
        page = wh.CURRENT_EXEC_PAGE
        if page < 1:
            wh.CURRENT_EXEC_PAGE = 1
        elif page > pg.num_pages:
            wh.CURRENT_EXEC_PAGE = pg.num_pages

        ms = pg.page(wh.CURRENT_EXEC_PAGE)

        self.job_data.data = {}
        self.job_data.ok = ms is not None
        if not ms:
            self.job_data.ok = False
            return self.job_data

        data = {}
        i = 0
        for j in ms:
            name = j.alg_name
            try:
                status = j.request.pipe_state.state
                date = j.request.pipe_state.started_time
            except AttributeError:
                status = j.request.pipeline_state.state
                date = j.request.pipeline_state.started_time
                error = j.request.pipeline_state.exception
                pos = error.rfind("Exception: ")
                error = error[pos+11:]
                params = j.params
                #log.info(error)
            if not error or error == "":
                error = "OK"
            if j.is_aborted:
                error = "Aborted"
            data[i] = (name, status, date, error, j.pk, params)
            i += 1
        
        self.job_data.ok = (pg.num_pages, wh.CURRENT_EXEC_PAGE, \
                            wh.CURRENT_EXEC_PAGE + 1, wh.CURRENT_EXEC_PAGE - 1)
        self.job_data.data = data
        return self.job_data
        
        # OLD
        sorted_index = sorted(data, key=lambda x: data[x][1], reverse=True)

        i = 0
        for ind in sorted_index:
            self.job_data.data[i] = data[ind]
            i += 1

        return self.job_data
