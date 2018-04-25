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
along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
"""
from .job import job as parent

from django.core.paginator import Paginator
from itertools import chain
from operator import attrgetter

from avi.models import gaia_query_model, herschel_query_model

from avi.warehouse import wh_common
from avi.warehouse import wh_frontend_config

from avi.log import logger

class get_queries_status(parent):
    def start(self, data):
        log = logger().get_log("get_queries_status")

        current_started = wh_common().get().queries_started
        count_started = 0

        wh = wh_frontend_config().get()
        sorting_wh = wh.SORTING_QUERY_BY
        order_by = 'request__pipeline_state__started_time'
        order_lambda = lambda query: query.request.pipeline_state.started_time
        if sorting_wh == 'name':
            order_by = 'name'
            order_lambda = lambda query: query.name
        elif sorting_wh == '-name':
            order_by = '-name'
            order_lambda = lambda query: query.name
        elif sorting_wh == '-date':
            order_by = '-request__pipeline_state__started_time'
        elif sorting_wh == 'status':
            order_by = 'request__pipeline_state__state'
            order_lambda = lambda query: query.request.pipeline_state.state
        elif sorting_wh == '-status':
            order_by = '-request__pipeline_state__state'
            order_lambda = lambda query: query.request.pipeline_state.state

        all_gaia = gaia_query_model.objects.all().order_by(order_by,'pk')
        all_hsa = herschel_query_model.objects.all().order_by(order_by,'pk')

        self.job_data.data = {}
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
        call = chain(all_gaia, all_hsa)
        all_ms = sorted(call , 
                        #key=attrgetter("name"), 
                        key = order_lambda,
                        reverse=reverse)

        pg = Paginator(all_ms, wh.MAX_QUERY_PER_PAGE)
        page = wh.CURRENT_QUERY_PAGE
        #log.info(page)
        if page < 1:
            wh.CURRENT_QUERY_PAGE = 1
        elif page > pg.num_pages:
            wh.CURRENT_QUERY_PAGE = pg.num_pages

        #log.info(wh.CURRENT_QUERY_PAGE)

        all_ms = pg.page(wh.CURRENT_QUERY_PAGE)

        if not all_ms:
            return self.job_data

        data = {}
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

            if not error or error == "":
                error = "OK"
            if q.is_aborted:
                error = "Aborted"

            log.info("status: %s", status)
            if status == "STARTED":
                count_started += 1
            #data[q.pk] = (q.name, status)
            data[i] = ("query %s"%(q.name), status, date, error, q.pk, q.archive)
            i+=1

        self.job_data.data[1] = data

        wh_common().get().queries_started = count_started
        #if current_started != 0:
        self.job_data.data[0] = count_started < current_started
        self.job_data.ok = [pg.num_pages, wh.CURRENT_QUERY_PAGE, \
                            wh.CURRENT_QUERY_PAGE + 1, wh.CURRENT_QUERY_PAGE - 1]

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
