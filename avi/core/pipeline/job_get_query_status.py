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

@package avi.core.pipeline.job_get_results

--------------------------------------------------------------------------------

This module provides the get_query_status job.
"""
from .job import job as parent

from avi.models import gaia_query_model
from avi.models import herschel_query_model
from avi.models import resource_model

from avi.log import logger

class get_query_status(parent):
    # TODO: doc
    def start(self, data):
        # TODO: doc
        log = logger().get_log("views")
        if data.get('mission') == 'gaia':
            #m = gaia_query_model.objects.all.filter(pk=data['id'])
            #m = gaia_query_model.objects.all
            m = gaia_query_model.objects.get(pk=data['id'])
            if m == None:
                self.job_data.ok = False
                return self.job_data
            self.job_data.ok = True
            self.job_data.data = m.request.pipeline_state.state
            return self.job_data
            
        if  data.get('mission') == 'hsa':
            m = herschel_query_model.objects.get(pk=data['id'])
            if m == None:
                self.job_data.ok = False
                return self.job_data
            self.job_data.ok = True
            self.job_data.data = m.request.pipeline_state.state
            return self.job_data