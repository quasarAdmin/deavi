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

@package avi.core.interface.archive_interface

--------------------------------------------------------------------------------

This module provides a parent class from which the rest of the archive 
interfaces will inherit.
"""
from .connection.connection import connection
# from risea.utils.adql_helper import adql_helper
from avi.utils.adql_helper import adql_helper

class archive_interface:
    """@class archive_interface
    The archive_interface provices a parent class from which the rest of the 
    archives interfaces will inherit.
    """
    ## A connection object @see avi.core.interface.connection.connection.connection
    connection = None
    ## The log
    log = None
    
    def __init__(self):
        """The archive_interface constructor
        
        Creates a new connection object

        Args:
        self: The object pointer.

        See:
        connection: avi.core.interface.connection.connection.connection
        """
        self.connection = connection()
        
    def init(self, cfg):
        """Initializes the archive_interface

        This method initializes the connection object witht he given 
        configuration

        Args:
        self: The object pointer.
        cfg: The configuration to be loaded.
        
        Returns:
        True if the configuration is loaded correctly, False otherwise

        See:
        connection: avi.core.interface.connection.connection
        """
        return self.connection.init(cfg)
    
    def get_columns(self, table):
        """TODO"""
        query = "SELECT top 1 * FROM " + table
        # TODO 
        return self.connection.async_query(query)

    def get_adql(self, query):
        """Does an ADQL query to the archive.
        
        This method uses the connection object to do an ADQL query to the 
        archive

        Args:
        self: The object pointer
        query: The ADQL query

        Returns:
        The data retrieve from that query if everything was done correctly, 
        None otherwise

        See:
        connection: avi.core.interface.connection.connection.connection
        """
        self.log.info("ADQL query sent to the archive")
        data = self.connection.async_query(query)
        self.log.info("Query finished")
        return data
    
    def get_circle(self, ra, dec, radius, table = None, params = None):
        """Does a conical query to the archive.
        
        This method uses the connection object to do a conical query to the 
        archive

        It uses the adql_helper class to create an ADQL query from the given 
        parameters

        Args:
        self: The object pointer
        ra: The ra coordinate
        dec: The dec coordinate
        radius: The radius of the query
        table: The table to be queried
        params: Special parameters to the query

        Returns:
        The data retrieve from that query if everything was done correctly, 
        None otherwise

        See:
        connection: avi.core.interface.connection.connection.connection

        See also:
        adql_helper: avi.utils.adql_helper.adql_helper
        """
        self.log.info("Conical query to the archive with ra: %f, dec: %f, radius: %f",ra, dec, radius)
        columns = "*"
        if params:
            columns = adql_helper().dic_to_str(params)
        query = "SELECT " + columns + " FROM  " + table
        query += " WHERE "+adql_helper().circle_defintion(ra, dec, radius)
        #self.log.info(str(query))
        data = self.connection.async_query(query)
        self.log.info("Query finished")
        return data
    
    def get_box(self, ra, dec, width, height, table = None, params = None):
        """Does a box-shaped query to the archive.
        
        This method uses the connection object to do a box-shaped query to the 
        archive

        It uses the adql_helper class to create an ADQL query from the given 
        parameters

        Args:
        self: The object pointer
        ra: The ra coordinate
        dec: The dec coordinate
        width: The width of the box
        height: The height of the box
        table: The table to be queried
        params: Special parameters to the query

        Returns:
        The data retrieve from that query if everything was done correctly, 
        None otherwise

        See:
        connection: avi.core.interface.connection.connection.connection

        See also:
        adql_helper: avi.utils.adql_helper.adql_helper
        """
        self.log.info('Entering get_box with ra %f and dec %f',ra, dec)
        columns = "*"
        if params:
            columns = adql_helper().dic_to_str(params)
        query = "SELECT " + columns + " FROM  " + table
        query +=" WHERE "+adql_helper().box_definition(ra, dec, width, height)
        data = self.connection.async_query(query)
        self.log.info('query finished')
        return data

    def get_polygon(self, ra, dec, vertexes, table = None, params = None):
        """Does a polygonal-shaped query to the archive.
        
        This method uses the connection object to do a polygonal-shaped query 
        to the archive

        It uses the adql_helper class to create an ADQL query from the given 
        parameters

        Args:
        self: The object pointer
        ra: The ra coordinate
        dec: The dec coordinate
        vertexes: An array of vertex forming the polygon
        table: The table to be queried
        params: Special parameters to the query

        Returns:
        The data retrieve from that query if everything was done correctly, 
        None otherwise

        See:
        connection: avi.core.interface.connection.connection.connection

        See also:
        adql_helper: avi.utils.adql_helper.adql_helper
        """
        self.log.info('Entering get_polygon')
        columns = "*"
        if params:
            columns = adql_helper().dic_to_str(params)
        query = "SELECT " + columns + " FROM " + table
        query +=" WHERE " + adql_helper().polygon_definition(ra, dec, vertexes)
        self.log.info(query)
        data = self.connection.async_query(query)
        self.log.info('query finished')
        return data
