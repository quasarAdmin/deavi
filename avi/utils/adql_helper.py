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
class adql_helper:
    def dic_to_str(self, dic):
        ret = ""
        for val in dic:
            ret += str(val) + ", "
        return ret[:-2]
    
    def circle_defintion(self, x, y, radius, coord_system = "ICRS"):
        return "1= CONTAINS(POINT('"+coord_system+"',ra,dec), CIRCLE('"+coord_system+"', " + str(x) + ", " + str(y) + ", " + str(radius) + "))"
    
    def box_definition(self, x, y, width, height, coord_system = 'ICRS'):
        return "(1= CONTAINS(POINT('ICRS',ra,dec), BOX('ICRS', " + str(x) + ", " + str(y) + ", " + str(width) + " , " + str(height) + ")))"

    def polygon_definition(self, x, y, vertexes, coord_system = "ICRS"):
        str_ver = str(x) + ", " + str(y)
        for i in vertexes:
            str_ver += ", " + str(i['ra']) + ", " + str(i['dec'])
        return "1= CONTAINS(POINT('"+coord_system+"',ra,dec), " \
            "POLYGON('"+coord_system+"', "+str_ver+"))"
