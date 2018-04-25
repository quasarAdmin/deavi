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
from avi.warehouse import wh_frontend_config

class change_page(parent):
    def start(self, data):
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
