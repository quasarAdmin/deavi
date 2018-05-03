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

from avi.models import herschel_query_model

class herschel_query(parent):
    def start(self,data):
        m = herschel_query_model(name_coord = data['name_coord'] == "name",
                                 name = data['name'], #if data['name'] != "" \
                                 #else None,
                                 ra = data['ra'],
                                 dec = data['dec'],
                                 shape = data['shape'],
                                 radius = data['radius'],
                                 width = data['width'] if data['width'] else 0,
                                 height = data['height'] if data['height'] else 0  ,
                                 polygon = data['polygon'],#if data['polygon']!="" \
                                 #else None,
                                 positional_images = \
                                 data['positional_images'] == "images",
                                 table = data['table'],
                                 instrument = data['instrument'],
                                 level = data['level'],
                                 params = "")
        m.save()
        self.job_data.data = m
        self.job_data.ok = True
        return self.job_data
