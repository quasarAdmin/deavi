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
#from avi.models import TutorialModel #gaia_query_model

# FIXME:
from avi.models import gaia_query_model

class gaia_query(parent):

    def start(self, data):
        # TODO:
        #m, created = TutorialModel.objects.get_or_create(fib_num = int(data))
        #gaia_test.delay(data)
        #self.job_data.data = data
        #self.job_data.ok = True
        #return self.job_data
        m = gaia_query_model(name_coord = data['name_coord'] == "name",
                             name = data['name'],
                             input_file = data['input_file'],
                             ra = float(data['ra']),
                             dec = float(data['dec']),
                             shape = data['shape'],
                             radius = float(data['radius']),
                             width = data['width'] if data['width'] else 0,
                             height = data['height'] if data['height'] else 0  ,
                             polygon = data['polygon'],
                             table = data['table'],
                             params = "",
                             file_name = data['file_name'],
                             adql = data['adql'])
        m.save()
        #TutorialModel.objects.get_or_create(fib_num = int(data))
        self.job_data.data = m
        self.job_data.ok = True
        return self.job_data
