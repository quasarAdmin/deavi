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

@package avi.core.pipeline.job_get_algorithms

--------------------------------------------------------------------------------

This module provides the get_algorithms job.
"""
from .job import job as parent

from django.core.paginator import Paginator

from avi.warehouse import wh_global_config as wh
from avi.warehouse import wh_frontend_config
from avi.log import logger

class get_algorithms(parent):
    """@class get_algorithms
    The get_algorithms class provides the algorithms names.

    It implementes the job interface and inherits the job_data attribute.

    @see job @link avi.core.pipeline.job
    @see job_data @link avi.core.pipeline.job_data
    """
    def start(self, data):
        """This method runs the get_algorithms job.

        If the algorithms are not loaded it will load them. Then it will 
        retrieve the all algorithm_info_models and return the data from them.

        Args:
        self: The object pointer.
        data: A dictionary containing the input data for the job.
        
        Returns:
        The job_data attribute. The ok attribute will be True if there are 
        algorithms retrieved, False otherwise.

        @see algorithm_info_model @link avi.models.algorithm_info_model
        """
        log = logger().get_log('algorithm_manager')

        wh_f = wh_frontend_config().get()

        if not wh().get().ALGORITHMS_LOADED:
            from avi.core.algorithm.algorithm_manager import algorithm_manager
            algorithm_manager().init()
            wh().get().ALGORITHMS_LOADED = True

        from avi.models import algorithm_info_model, algorithm_group_model
        all_ms = algorithm_info_model.objects.all().order_by('name_view',
                                                          'name','pk')
        
        #sall_ms = sorted(all_ms, key = lambda x:(x.name_view is None, x))

        self.job_data.data = {}
        self.job_data.ok = all_ms is not None
        if not all_ms:
            return self.job_data

        pg = Paginator(all_ms, wh_f.MAX_ALG_PER_PAGE)
        page = wh_f.CURRENT_ALG_PAGE
        if page < 1:
            wh_f.CURRENT_ALG_PAGE = 1
        elif page > pg.num_pages:
            wh_f.CURRENT_ALG_PAGE = pg.num_pages

        ms = pg.page(wh_f.CURRENT_ALG_PAGE)

        all_ms_g = algorithm_group_model.objects.all().order_by('name_view','name','pk')
        pg_g = Paginator(all_ms_g, wh_f.MAX_ALG_PER_PAGE)
        page = wh_f.CURRENT_ALG_PAGE
        if page < 1:
            wh_f.CURRENT_ALG_PAGE = 1
        elif page > pg.num_pages:
            wh_f.CURRENT_ALG_PAGE = pg.num_pages
        ms_g = pg_g.page(wh_f.CURRENT_ALG_PAGE)

        data = []
        for g in ms_g:
            data.append({"group":g, 
                        "algorithms":[]})
        data.sort(key=lambda x: x["group"].position, reverse=False)
        
        for j in ms:
            for g in data:
                if j.algorithm_group == g["group"].name:
                    g["algorithms"].append((j.pk,
                                            j.name,
                                            j.name_view,
                                            j.algorithm_type,
                                            j.algorithm_group,
                                            j.position))
        for g in data:
            g["algorithms"].sort(key=lambda x: x[4], reverse=False)
        
        for g in data:
            log.info(g["group"].name)
            log.info(g["group"].position)
            for a in g["algorithms"]:
                log.info(a[4])
                log.info(a[1])


        # OLD
        # data = {}
        # i = 0
        # for j in ms:
        #     data[i] = (j.pk,
        #                j.name,
        #                j.name_view,
        #                j.algorithm_type)
        #     i += 1
            
        res = {}
        res["algorithms"] = data
        res["max_pages"] = pg.num_pages
        res["current_page"] = wh_f.CURRENT_ALG_PAGE
        res["next_page"] = wh_f.CURRENT_ALG_PAGE + 1
        res["prev_page"] = wh_f.CURRENT_ALG_PAGE - 1
        self.job_data.data = res
        return self.job_data
