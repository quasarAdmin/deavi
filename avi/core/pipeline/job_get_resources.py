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

from avi.models import resource_model
from avi.warehouse import wh_global_config as wh
from avi.log import logger

class get_resources(parent):
    def start(self, data):
        ms = resource_model.objects.all()
        data = {}
        gaia = {}
        hsa = {}
        data['gaia'] = gaia
        data['hsa'] = hsa
        for q in ms:
            if q.file_type == 'gaia':
                gaia[q.name] = q.name
            elif q.file_type == 'hsa':
                hsa[q.name] = q.name
        self.job_data.ok = True
        self.job_data.data = data
        return self.job_data
