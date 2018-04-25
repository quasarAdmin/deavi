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

from avi.log import logger

from django.core.paginator import Paginator

from avi.warehouse import wh_frontend_config
from avi.utils.resources_manager import resources_manager

class get_files(parent):
    def start(self, data):
        log = logger().get_log("views")
        
        wh = wh_frontend_config().get()
        
        #dirs = data[0]
        #files = data[1]

        sorting_wh = wh.SORTING_RESOURCES_BY
        order_by = ''

        all_files = resources_manager().get_list(wh.CURRENT_PATH)
        
        all_files.sort()

        pg = Paginator(all_files, wh.MAX_RESOURCES_PER_PAGE)
        page = wh.CURRENT_RESOURCES_PAGE
        if page < 1:
            wh.CURRENT_RESOURCES_PAGE = 1
        elif page > pg.num_pages:
            wh.CURRENT_RESOURCES_PAGE = pg.num_pages

        files = pg.page(wh.CURRENT_RESOURCES_PAGE)

        f, d = resources_manager().get_info(files,wh.CURRENT_PATH)

        log.info(f)
        
        self.job_data.data = [f, d]
        self.job_data.ok = (pg.num_pages, wh.CURRENT_RESOURCES_PAGE, \
                            wh.CURRENT_RESOURCES_PAGE + 1, wh.CURRENT_RESOURCES_PAGE - 1)
        return self.job_data
