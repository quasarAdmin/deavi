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

@package avi.core.pipeline.job_get_pipeline_status

--------------------------------------------------------------------------------

This module provides the get_pipeline_status job.
"""
from .job import job as parent

from ast import literal_eval
from django.core.paginator import Paginator

from avi.models import algorithm_model, algorithm_info_model
from avi.core.algorithm.algorithm_manager import algorithm_manager
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
        #------------------
        #----all data algorithms
        alldata = {}
        k = 0
        for h in pg.object_list:
            try:
                status = h.request.pipe_state.state
                date = h.request.pipe_state.started_time
            except AttributeError:
                status = h.request.pipeline_state.state
                date = h.request.pipeline_state.started_time
            #status = h.request.pipeline_state.state
            #date = h.request.pipeline_state.started_time
            params = {}
            params['algorithm'] = {'name': h.alg_name, 'params':{}}
            ainfo_ms = algorithm_info_model.objects.filter(name=h.alg_name)[0]
            if ainfo_ms:
                qparams = literal_eval(h.params)
                mng = algorithm_manager()
                ainfo = mng.get_info(ainfo_ms.definition_file, 'input')
                for l in ainfo:
                    if 'view_name' in ainfo[l]:
                        params['algorithm']['params'][ainfo[l]['view_name']] = qparams['algorithm']['params'][ainfo[l]['name']]
                    else:
                        params['algorithm']['params'][ainfo[l]['name']] = qparams['algorithm']['params'][ainfo[l]['name']]
                params = str(params)
                    
            else:
                params = h.params
            alldata[k] = (h.alg_name, h.pk, params, date, status)
            log.info(params)
            k += 1
        #------------------
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
            params = {}
            params['algorithm'] = {'name': j.alg_name, 'params':{}}
            try:
                status = j.request.pipe_state.state
                date = j.request.pipe_state.started_time
            except AttributeError:
                status = j.request.pipeline_state.state
                date = j.request.pipeline_state.started_time
                error = j.request.pipeline_state.exception
                pos = error.rfind("Exception: ")
                error = error[pos+11:]
                ainfo_ms = algorithm_info_model.objects.filter(name=j.alg_name)[0]
                if ainfo_ms:
                    qparams = literal_eval(j.params)
                    mng = algorithm_manager()
                    ainfo = mng.get_info(ainfo_ms.definition_file, 'input')
                    for k in ainfo:
                        if 'view_name' in ainfo[k]:
                            params['algorithm']['params'][ainfo[k]['view_name']] = str(qparams['algorithm']['params'][ainfo[k]['name']])
                        else:
                            params['algorithm']['params'][ainfo[k]['name']] = str(qparams['algorithm']['params'][ainfo[k]['name']])
                    params = str(params)
                        
                else:
                    params = j.params
                #log.info(error)
            if not error or error == "":
                error = "OK"
            if j.is_aborted:
                error = "Aborted"
            data[i] = (name, status, date, error, j.pk, params)
            i += 1
        
        self.job_data.ok = (pg.num_pages, wh.CURRENT_EXEC_PAGE, \
                            wh.CURRENT_EXEC_PAGE + 1, wh.CURRENT_EXEC_PAGE - 1, alldata, wh.SORTING_EXEC_BY)
        self.job_data.data = data
        return self.job_data
        
        # OLD
        sorted_index = sorted(data, key=lambda x: data[x][1], reverse=True)

        i = 0
        for ind in sorted_index:
            self.job_data.data[i] = data[ind]
            i += 1

        return self.job_data
