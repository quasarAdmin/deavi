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

@package avi.core.pipeline.job_get_queries_status

--------------------------------------------------------------------------------

This module provides the get_queries_status job.
"""
from .job import job as parent

from django.core.paginator import Paginator
from itertools import chain
from operator import attrgetter

from avi.models import gaia_query_model, herschel_query_model, sim_query_model

from avi.warehouse import wh_common
from avi.warehouse import wh_frontend_config

from avi.log import logger

from .job_get_query_info import get_query_info

class get_queries_status(parent):
    """@class get_pipeline_status
    The get_queries_status class retrieves the status of the queries.

    It implementes the job interface and inherits the job_data attribute.

    @see job @link avi.core.pipeline.job
    @see job_data @link avi.core.pipeline.job_data
    """
    def start(self, data):
        """This method runs the get_queries_status job.

        This method will retrieve the gaia_query_models and the 
        herschel_query_models and it will sort them by the current sorting 
        method provided by the wh_frontend_config warehouse.

        Then it will paginate the results with current page retrieved from 
        the wh_frontend_config warehouse.

        Args:
        self: The object pointer.
        data: A dictorianry containing the input data for the job.

        Returns:
        The job_data attribute. The ok attribute provides the pages information.

        @see gaia_query_model @link avi.models.gaia_query_model
        @see herschel_query_model @link avi.models.herschel_query_model
        @see wh_frontend_config @link avi.warehouse.wh_frontend_config
        """
        log = logger().get_log("get_queries_status")

        current_started = wh_common().get().queries_started
        count_started = 0

        wh = wh_frontend_config().get()
        sorting_wh = wh.SORTING_QUERY_BY
        order_by = 'request__pipeline_state__started_time'
        order_lambda = lambda query: (query.request.pipeline_state.started_time, query)
        if sorting_wh == 'name':
            order_by = 'name'
            order_lambda = lambda query: ("%s %s %s"%(query.archive, query.name, query.pk), query)
        elif sorting_wh == '-name':
            order_by = '-name'
            order_lambda = lambda query: ("%s %s %s"%(query.archive, query.name, query.pk), query)
        elif sorting_wh == '-date':
            order_by = '-request__pipeline_state__started_time'
            order_lambda = lambda  query: (query.request.pipeline_state.started_time, query)
        elif sorting_wh == 'status':
            order_by = 'request__pipeline_state__state'
            order_lambda = lambda query: (query.request.pipeline_state.state, query)
        elif sorting_wh == '-status':
            order_by = '-request__pipeline_state__state'
            order_lambda = lambda query: (query.request.pipeline_state.state, query)

        all_gaia = gaia_query_model.objects.all().order_by(order_by,'pk')
        all_hsa = herschel_query_model.objects.all().order_by(order_by,'pk')
        all_sim = sim_query_model.objects.all().order_by(order_by, 'pk')

        len_all = len(str(len(all_gaia) + len(all_hsa) + len(all_sim)))
        order_lambda = lambda query: (query.request.pipeline_state.started_time, query)
        if sorting_wh == 'name':
            order_lambda = lambda query: ("%s %s %s"%(query.archive, query.name, str(query.pk).zfill(len_all)), query)
        elif sorting_wh == '-name':
            order_lambda = lambda query: ("%s %s %s"%(query.archive, query.name, str(query.pk).zfill(len_all)), query)

        log.info("models retrieved")

        self.job_data.data = dict([(0, False), (1, {})])
        self.job_data.ok = False

        #pgg = Paginator(all_gaia, wh.MAX_QUERY_PER_PAGE)
        #pgh = Paginator(all_hsa, wh.MAX_QUERY_PER_PAGE)
        
        #page_gaia = wh.CURRENT_QUERY_PAGE
        #if page_gaia < 1:
        #    wh.CURRENT_QUERY_PAGE = 1
        #elif page_gaia > pgg.num_pages:
        #    wh.CURRENT_QUERY_PAGE = pgg.num_pages

        #ms_gaia = pgg.page(wh.CURRENT_QUERY_PAGE)
        
        #if wh.CURRENT_QUERY_PAGE > pgh.num_pages:
        #    wh.CURRENT_QUERY_PAGE = pgh.num_pages

        #ms_hsa = pgh.page(wh.CURRENT_QUERY_PAGE)

        reverse = False
        if order_by[0] == '-':
            reverse = True
            order_by.replace('-','',1)
        call = chain(all_gaia, all_hsa, all_sim)
        #for call_ in call:
        #    call_.name = "query %s"%(call_.name)
        #    if isinstance(call_, gaia_query_model):
        #        call_.name = "Gaia %s"%(call_.name)
        #    elif isinstance(call_, herschel_query_model):
        #        call_.name = "HSA %s"%(call_.name)
        #    elif isinstance(call_, sim_query_model):
        #        call_.name = "SIM %s"%(call_.name)
        #try:
        all_ms = sorted(call , 
                        #key=attrgetter("name"), 
                        key = order_lambda,
                        reverse=reverse)
        #for am in all_ms:
        #    log.info("%s %s %s", am.name, am.request.pipeline_state.started_time, am.request.pipeline_state.state)
        #except TypeError:
        #    log.info("whaaat")
        #    all_ms = sorted(call , 
                            #key=attrgetter("name"), 
        #                    key = lambda query: (query.name is None, query),
        #                    reverse=True)

        log.info("models chained and sorted")

        pg = Paginator(all_ms, wh.MAX_QUERY_PER_PAGE)
        page = wh.CURRENT_QUERY_PAGE
        #log.info(page)
        #------------------
        #---all data queries
        allqueries = {}
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
            name = "query %s"%(h.name)
            if isinstance(h, gaia_query_model):
                name = "Gaia %s"%(h.name)
            elif isinstance(h, herschel_query_model):
                name = "HSA %s"%(h.name)
            elif isinstance(h, sim_query_model):
                name = "SIM %s"%(h.name)
            allqueries[k] = (name, status, date, h.pk, h.archive)
            k += 1
        #------------------
        log.info("paginator done")
        if page < 1:
            wh.CURRENT_QUERY_PAGE = 1
        elif page > pg.num_pages:
            wh.CURRENT_QUERY_PAGE = pg.num_pages


        all_ms = pg.page(wh.CURRENT_QUERY_PAGE)

        if not all_ms:
            return self.job_data

        data = {}


        #------query info -----
        #query_id_mission = {}
        #query_info = {}
        #------query info -----


        i = 0
        for q in all_ms:
            try:
                status = q.request.pipe_state.state
                date = q.request.pipe_state.started_time
            except AttributeError:
                status = q.request.pipeline_state.state
                date = q.request.pipeline_state.started_time
                error = q.request.pipeline_state.exception
                pos = error.rfind("Exception: ")
                error = error[pos+11:]


                #------query info -----
                #query_id_mission['mission'] = q.archive
                #query_id_mission['id'] = q.pk
                #query_info = get_query_info.start(self,query_id_mission)
                #log.info("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                #log.info(query_info.data)
                #log.info("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
                #------query info -----


            if not error or error == "":
                error = "OK"
            if q.is_aborted:
                error = "Aborted"

            log.info("status: %s", status)
            if status == "STARTED":
                count_started += 1
            #data[q.pk] = (q.name, status)
            

            #------query info -----
            #data[i] = ("query %s"%(q.name), status, date, error, q.pk, q.archive, query_info.data)
            #------query info -----

            name = "query %s"%(q.name)
            if isinstance(q, gaia_query_model):
                name = "Gaia %s"%(q.name)
            elif isinstance(q, herschel_query_model):
                name = "HSA %s"%(q.name)
            elif isinstance(q, sim_query_model):
                name = "SIM %s"%(q.name)
            data[i] = (name, status, date, error, q.pk, q.archive)
            log.info("loop")
            
            i+=1

        log.info("looping through the paginator")

        wh_common().get().queries_started = count_started
        #if current_started != 0:
        log.info("asdasd")
        log.info(self.job_data.data)
        self.job_data.data[0] = count_started < current_started
        #self.job_data.data.append(count_started < current_started)
        self.job_data.ok = [pg.num_pages, wh.CURRENT_QUERY_PAGE, \
                            wh.CURRENT_QUERY_PAGE + 1, wh.CURRENT_QUERY_PAGE - 1, allqueries, wh.SORTING_QUERY_BY]
        try:
            log.info(self.job_data.data)
            #log.info(self.job_data.data[1])
            log.info(data)
            aux = data
            log.info(type(aux))
            if isinstance(self.job_data.data, dict):
            #log.info(type(self.job_data.data[1]))
                self.job_data.data[1] = aux#{0:('sim','success'),1:('sim20','success')}
            else:
                self.job_data.data.append(data)
            #self.job_data.data.append(data)
        except Exception as e:
            log.info(e)
        log.info("job_get_queries_status end")
        return self.job_data
        # OLD

        ms = gaia_query_model.objects.all()

        data = {}
        i = 0
        for q in ms:
            log.info("query %s", q.name)
            try:
                status = q.request.pipe_state.state
                date = q.request.pipe_state.started_time
            except AttributeError:
                status = q.request.pipeline_state.state
                date = q.request.pipeline_state.started_time
                error = q.request.pipeline_state.exception
                pos = error.rfind("Exception: ")
                error = error[pos+11:]

            if not error or error == "":
                error = "OK"
            if q.is_aborted:
                error = "Aborted"

            log.info("status: %s", status)
            if status == "STARTED":
                count_started += 1
            #data[q.pk] = (q.name, status)
            data[i] = ("Gaia %s"%(q.name), status, date, error, q.pk, "gaia")
            i+=1
            #data.append((q.name, status))

        ms = herschel_query_model.objects.all()
        
        for q in ms:
            log.info("query %s", q.name)
            try:
                status = q.request.pipe_state.state
                date = q.request.pipe_state.started_time
            except AttributeError:
                status = q.request.pipeline_state.state
                date = q.request.pipeline_state.started_time
                error = q.request.pipeline_state.exception
                pos = error.rfind("Exception: ")
                error = error[pos+11:]

            if not error or error == "":
                error = "OK"
            if q.is_aborted:
                error = "Aborted"
            log.info("status: %s", status)
            if status == "STARTED":
                count_started += 1
            data[i] = ("HSA %s"%(q.name), status, date, error, q.pk, "hsa")
            i+=1

        sorted_index = sorted(data, key=lambda x: data[x][1], reverse=True)

        res = {}
        i = 0
        for ind in sorted_index:
            res[i] = data[ind]
            i += 1
        self.job_data.data = {}
        self.job_data.data[1] = res
        wh_common().get().queries_started = count_started
        #if current_started != 0:
        self.job_data.data[0] = count_started < current_started
        #else:
        #    self.job_data.data[0] = False

        self.job_data.ok = ms is not None
        return self.job_data

        self.job_data.data = {}
        i = 0
        for ind in sorted_index:
            self.job_data.data[i] = data[ind]
            i += 1
        
        self.job_data.ok = ms is not None
        return self.job_data
