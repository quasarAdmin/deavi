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

@package avi.utils.adql_helper

--------------------------------------------------------------------------------

This module helps to create ADQL queries from single parameters
"""
class adql_helper:
    """@class adql_helper
    The adql_helper class provides methods to construct ADQL queries from given 
    parameters.
    """
    def dic_to_str(self, dic):
        """Creates a string with a given dictionary
        
        This method creates a string with the values of a given dictionary

        Args:
        self: The object pointer
        dic: The dictionary

        Returns:
        A string formed with the values of the given dictionary
        """
        ret = ""
        for val in dic:
            ret += str(val) + ", "
        return ret[:-2]
    
    def circle_defintion(self, x, y, radius, coord_system = "ICRS"):
        """Defines a conical query in ADQL
        
        Defines a conical query in ADQL with the given paramters

        Args:
        self: The object pointer
        x: The X coordinate of the center
        y: The Y coordinate of the center
        radius: The radius
        coord_system: The coordinates system

        Returns:
        A string with the definition of the cone
        """
        return "1= CONTAINS(POINT('"+coord_system+"',ra,dec), CIRCLE('"+coord_system+"', " + str(x) + ", " + str(y) + ", " + str(radius) + "))"
    
    def box_definition(self, x, y, width, height, coord_system = 'ICRS'):
        """Defines a box-shaped query in ADQL
        
        Defines a box-shaped query in ADQL with the given paramters

        Args:
        self: The object pointer
        x: The X coordinate of the center
        y: The Y coordinate of the center
        width: The width of the box
        height: The height of the box
        coord_system: The coordinates system

        Returns:
        A string with the definition of the box
        """
        return "(1= CONTAINS(POINT('ICRS',ra,dec), BOX('ICRS', " + str(x) + ", " + str(y) + ", " + str(width) + " , " + str(height) + ")))"

    def polygon_definition(self, x, y, vertexes, coord_system = "ICRS"):
        """Defines a polygonal-shaped query in ADQL
        
        Defines a polygonal-shaped query in ADQL with the given paramters

        Args:
        self: The object pointer
        x: The X coordinate of the first vertex
        y: The Y coordinate of the first vertex
        vertexes: An array with the rest of the vertexes
        coord_system: The coordinates system

        Returns:
        A string with the definition of the polygon
        """
        str_ver = str(x) + ", " + str(y)
        for i in vertexes:
            str_ver += ", " + str(i['ra']) + ", " + str(i['dec'])
        return "1= CONTAINS(POINT('"+coord_system+"',ra,dec), " \
            "POLYGON('"+coord_system+"', "+str_ver+"))"
