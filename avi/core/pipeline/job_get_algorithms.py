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

        from avi.models import algorithm_info_model
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
        data = {}
        i = 0
        for j in ms:
            data[i] = (j.pk,
                       j.name,
                       j.name_view,
                       j.algorithm_type)
            i += 1
            
        res = {}
        res["algorithms"] = data
        res["max_pages"] = pg.num_pages
        res["current_page"] = wh_f.CURRENT_ALG_PAGE
        res["next_page"] = wh_f.CURRENT_ALG_PAGE + 1
        res["prev_page"] = wh_f.CURRENT_ALG_PAGE - 1
        self.job_data.data = res
        return self.job_data
