"""
Copyright (C) 2016-2020 Quasar Science Resources, S.L.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.

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
