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
from .connection.connection import connection
# from risea.utils.adql_helper import adql_helper
from avi.utils.adql_helper import adql_helper

class archive_interface:
    
    connection = None
    log = None
    
    def __init__(self):
        self.connection = connection()
        
    def init(self, cfg):
        return self.connection.init(cfg)
    
    def get_columns(self, table):
        query = "SELECT top 1 * FROM " + table
        # TODO 
        return self.connection.async_query(query)

    def get_adql(self, query):
        self.log.info("ADQL query sent to the archive")
        data = self.connection.async_query(query)
        self.log.info("Query finished")
        return data
    
    def get_circle(self, ra, dec, radius, table = None, params = None):
        self.log.info("Conical query to the archive with ra: %f, dec: %f, radius: %f",ra, dec, radius)
        columns = "*"
        if params:
            columns = adql_helper().dic_to_str(params)
        query = "SELECT " + columns + " FROM  " + table
        query += " WHERE "+adql_helper().circle_defintion(ra, dec, radius)
        data = self.connection.async_query(query)
        self.log.info("Query finished")
        return data
    
    def get_box(self, ra, dec, width, height, table = None, params = None):
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
