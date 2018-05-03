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
"""
from .job import job as parent

from avi.models import gaia_query_model, herschel_query_model

from avi.log import logger

class get_queries_status(parent):
    def start(self, data):
        log = logger().get_log("get_queries_status")

        ms = gaia_query_model.objects.all()

        data = {}
        i = 0
        for q in ms:
            log.info("query %s", q.name)
            status = q.request.pipe_state.state
            log.info("status: %s", status)
            #data[q.pk] = (q.name, status)
            data[i] = ("Gaia %s"%(q.name), status)
            i+=1
            #data.append((q.name, status))

        ms = herschel_query_model.objects.all()
        
        for q in ms:
            log.info("query %s", q.name)
            status = q.request.pipe_state.state
            log.info("status: %s", status)
            data[i] = ("HSA %s"%(q.name), status)
            i+=1

        self.job_data.data = data
        self.job_data.ok = ms is not None
        return self.job_data
