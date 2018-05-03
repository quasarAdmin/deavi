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

from avi.models import plot_model
from avi.log import logger

class get_plot(parent):
    def start(self, data):
        ms = plot_model.objects.filter(pk=data)
        if not ms:
            self.job_data.ok = False
            self.job_data.data = None
            return self.job_data
        
        ret = {}
        ret['html'] = ms[0].html
        ret['sc'] = ms[0].script
        self.job_data.ok = True
        self.job_data.data = ret
        return self.job_data
