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
@package avi.core.interface.gaia

--------------------------------------------------------------------------------

This module provides the interface to the gaia archive 
"""
# Gaia interface

#from .connection.connection import connection
from .archive_interface import archive_interface
#from risea.utils.adql_helper import adql_helper
from avi.utils.adql_helper import adql_helper

#from risea.log import logger
from avi.log import logger

class gaia(archive_interface):
        """@class gaia
        The gaia class provides the interface to the gaia archive.
        
        It inherits from the archive_interface, thus it uses the connection 
        object to access the archive.

        @see avi.core.interface.archive_interface.archive_interface
        @see avi.core.interface.connection.connection.connection
        """
        def __init__(self):
                """The gaia constructor

                The constructor initializes the log and calls the parent class 
                constructor to create the connection object

                Args:
                self: the object pointer
                
                See:
                connection: avi.core.interface.connection.connection.connection
                """
                super(gaia, self).__init__()
                self.log = logger().get_log('gaia')

        def get_circle(self, ra, dec, radius, table = "gaiadr1.gaia_source", params = None):
                """Does a conical query to the archive.
        
                This method calls the parent method get_circle to do the query
                
                Args:
                self: The object pointer
                ra: The ra coordinate
                dec: The dec coordinate
                radius: The radius of the query
                table: The table to be queried
                params: Special parameters to the query
                
                Returns:
                The data retrieve from that query if everything was done 
                correctly, None otherwise
                
                See:
                archive_interface: avi.core.interface.archive_interface.archive_interface
                """
                return super(gaia, self).get_circle(ra, dec, radius, table, params)
                
        def get_box(self, ra, dec, width, height, table = "gaiadr1.gaia_source", params = None):
                """Does a box-shaped query to the archive.
        
                This method calls the parent method get_box to do the query
                
                Args:
                self: The object pointer
                ra: The ra coordinate
                dec: The dec coordinate
                width: The width of the box
                height: The height of the box
                table: The table to be queried
                params: Special parameters to the query

                Returns:
                The data retrieve from that query if everything was done 
                correctly, None otherwise
                
                See:
                archive_interface: avi.core.interface.archive_interface.archive_interface
                """
                return super(gaia, self).get_box(ra, dec, width, height, table, params)
                
        def get_polygon(self, ra, dec, vertexes, table = "gaiadr1.gaia_source", params = None):
                """Does a polygonal-shaped query to the archive.
        
                This method calls the parent method get_polygon to do the query
                
                Args:
                self: The object pointer
                ra: The ra coordinate
                dec: The dec coordinate
                vertexes: An array of vertex forming the polygon
                table: The table to be queried
                params: Special parameters to the query

                Returns:
                The data retrieve from that query if everything was done 
                correctly, None otherwise
                
                See:
                archive_interface: avi.core.interface.archive_interface.archive_interface
                """
                return super(gaia, self).get_polygon(ra, dec, vertexes, table, params)

        # parallax filter
        def get_circle_parallax(self, ra, dec, radius, minpar, maxpar, table = "gaiadr1.tgas_source", params = None):
                """Does a conical query filtering by parallax

                This method uses the connection object to do a conical query 
                to the archive filtering by a minimum and maximum parallax

                It uses the adql_helper class to create an ADQL query from the 
                given parameters

                Args:
                self: The object pointer
                ra: The ra coordinate
                dec: The dec coordinate
                radius: The radius of the query
                minpar: The minimum parallax
                maxpar: The maximum parallax
                table: The table to be queried
                params: Special parameters to the query
                
                Returns:
                The data retrieve from that query if everything was done 
                correctly, None otherwise

                See:
                connection: avi.core.interface.connection.connection.connection
                
                See also:
                adql_helper: avi.utils.adql_helper.adql_helper
                """
                self.log.info('Entering get_circle_parallax with ra %f and dec %f',ra, dec)
                columns = "*"
                if params:
                        columns = adql_helper().dic_to_str(params)
                query = "SELECT "+ columns +" FROM " + table
                query +=" WHERE "+adql_helper().circle_defintion(ra, dec, radius)
                query += " AND (parallax > " + str (minpar) + ")"
                query += " AND (parallax < " + str (maxpar) + ")"
                data = self.connection.async_query(query)
                self.log.info('query finished')
                return data
                
        def get_box_parallax(self, ra, dec, width, height, minpar, maxpar, table = "gaiadr1.gaia_source", params = None):
                """Does a box-shaped query filtering by parallax

                This method uses the connection object to do a box-shaped query 
                to the archive filtering by a minimum and maximum parallax

                It uses the adql_helper class to create an ADQL query from the 
                given parameters

                Args:
                self: The object pointer
                ra: The ra coordinate
                dec: The dec coordinate
                width: The width of the box
                height: The height of the box
                minpar: The minimum parallax
                maxpar: The maximum parallax
                table: The table to be queried
                params: Special parameters to the query
                
                Returns:
                The data retrieve from that query if everything was done 
                correctly, None otherwise

                See:
                connection: avi.core.interface.connection.connection.connection
                
                See also:
                adql_helper: avi.utils.adql_helper.adql_helper
                """
                self.log.info('Entering get_box_parallax with ra %f and dec %f',ra, dec)
                columns = "*"
                if params:
                        columns = adql_helper().dic_to_str(params)
                query = "SELECT "+ columns +" FROM " + table
                query += " WHERE "+adql_helper().box_definition(ra, dec, width, height)
                query += " AND (parallax > " + str (minpar) + ")"
                query += " AND (parallax < " + str (maxpar) + ")"
                data = self.connection.async_query(query)
                self.log.info('query finished')
                return data

        def get_circle_error_pm(self, ra, dec, radius, pmra_error_vs_pmra, pmdec_error_vs_pmdec, pmra, pmdec, table = "gaiadr1.gaia_source", params = None):
                """Does a conical query filtering by the error of the 
                propermotion

                This method uses the connection object to do a conical query 
                to the archive filtering by the error of the propermotion in 
                the ra and the dec

                It uses the adql_helper class to create an ADQL query from the 
                given parameters

                Args:
                self: The object pointer
                ra: The ra coordinate
                dec: The dec coordinate
                radius: The radius of the query
                pmra_error_vs_pmra: The propermotion in ra error
                pmdec_error_vs_pmdec: The propermotion in the dec error
                pmra: The propermotion in ra
                pmdec: The propermotion in dec
                table: The table to be queried
                params: Special parameters to the query
                
                Returns:
                The data retrieve from that query if everything was done 
                correctly, None otherwise

                See:
                connection: avi.core.interface.connection.connection.connection
                
                See also:
                adql_helper: avi.utils.adql_helper.adql_helper
                """
                columns = "*"
                if params:
                        columns = adql_helper().dic_to_str(params)
                query = "SELECT "+ columns +" FROM " + table
                query +=" WHERE "+adql_helper().circle_defintion(ra, dec, radius)
                query += " AND abs(pmra_error/pmra)<" + str(pmra_error_vs_pmra)
                query += " AND abs(pmdec_error/pmdec)<" + str(pmdec_error_vs_pmdec)
                query += " AND pmra IS NOT NULL AND abs(pmra)>" + str(pmra)
                query += " AND pmdec IS NOT NULL AND abs(pmdec)>" + str(pmdec)
                if(self.connection == None): print("No connection")
                data = self.connection.async_query(query)
                return data

        def get_circle_pm(self, ra, dec, radius, pmra_max, pmra_min, pmdec_max, pmdec_min, table = "gaiadr1.gaia_source", params = None):
                """Does a conical query filtering by the propermotions

                This method uses the connection object to do a conical query 
                to the archive filtering by a minimum and a maximum 
                propermotions
                
                It uses the adql_helper class to create an ADQL query from the 
                given parameters

                Args:
                self: The object pointer
                ra: The ra coordinate
                dec: The dec coordinate
                radius: The radius of the query
                pmra_max: The maximum propermotion in ra
                pmra_min: The minimum propermotion in ra
                pmdec_max: The Maximum propermotion in dec
                pmdec_min: The minimum propermotion in dec
                table: The table to be queried
                params: Special parameters to the query
                
                Returns:
                The data retrieve from that query if everything was done 
                correctly, None otherwise

                See:
                connection: avi.core.interface.connection.connection.connection
                
                See also:
                adql_helper: avi.utils.adql_helper.adql_helper
                """
                columns = "*"
                if params:
                        columns = adql_helper().dic_to_str(params)
                query = "SELECT "+ columns +" FROM " + table
                query +=" WHERE "+adql_helper().circle_defintion(ra, dec, radius)
                query += " AND pmra BETWEEN " + str(pmra_min)
                query += " AND " + str(pmra_max)
                query += " AND pmdec BETWEEN " + str(pmdec_min)
                query += " AND " + str(pmdec_max)
                if(self.connection == None): print("No connection")
                data = self.connection.async_query(query)
                return data

        def get_box_error_pm(self, ra, dec, width, height, pmra_error_vs_pmra, pmdec_error_vs_pmdec, pmra, pmdec, table = "gaiadr1.gaia_source", params = None):
                """Does a box-shaped query filtering by the error of the 
                propermotion

                This method uses the connection object to do a box-shaped query 
                to the archive filtering by the error of the propermotion in 
                the ra and the dec

                It uses the adql_helper class to create an ADQL query from the 
                given parameters

                Args:
                self: The object pointer
                ra: The ra coordinate
                dec: The dec coordinate
                width: The width of the box
                height: The height of the box
                pmra_error_vs_pmra: The propermotion in ra error
                pmdec_error_vs_pmdec: The propermotion in the dec error
                pmra: The propermotion in ra
                pmdec: The propermotion in dec
                table: The table to be queried
                params: Special parameters to the query
                
                Returns:
                The data retrieve from that query if everything was done 
                correctly, None otherwise

                See:
                connection: avi.core.interface.connection.connection.connection
                
                See also:
                adql_helper: avi.utils.adql_helper.adql_helper
                """
                columns = "*"
                if params:
                        columns = adql_helper().dic_to_str(params)
                query = "SELECT "+ columns +" FROM " + table
                query +=" WHERE "+adql_helper().box_definition(ra, dec, width, height)
                query += " AND abs(pmra_error/pmra)<" + str(pmra_error_vs_pmra)
                query += " AND abs(pmdec_error/pmdec)<" + str(pmdec_error_vs_pmdec)
                query += " AND pmra IS NOT NULL AND abs(pmra)>" + str(pmra)
                query += " AND pmdec IS NOT NULL AND abs(pmdec)>" + str(pmdec)
                if(self.connection == None): print("No connection")
                data = self.connection.async_query(query)
                return data

        def get_box_pm(self, ra, dec, width, height, pmra_max, pmra_min, pmdec_max, pmdec_min, table = "gaiadr1.gaia_source", params = None):
                """Does a box-shaped query filtering by the propermotions

                This method uses the connection object to do a box-shaped query 
                to the archive filtering by a minimum and a maximum 
                propermotions
                
                It uses the adql_helper class to create an ADQL query from the 
                given parameters

                Args:
                self: The object pointer
                ra: The ra coordinate
                dec: The dec coordinate
                width: The width of the box
                height: The height of the box
                pmra_max: The maximum propermotion in ra
                pmra_min: The minimum propermotion in ra
                pmdec_max: The Maximum propermotion in dec
                pmdec_min: The minimum propermotion in dec
                table: The table to be queried
                params: Special parameters to the query
                
                Returns:
                The data retrieve from that query if everything was done 
                correctly, None otherwise

                See:
                connection: avi.core.interface.connection.connection.connection
                
                See also:
                adql_helper: avi.utils.adql_helper.adql_helper
                """
                columns = "*"
                if params:
                        columns = adql_helper().dic_to_str(params)
                query = "SELECT "+ columns +" FROM " + table
                query +=" WHERE "+adql_helper().box_definition(ra, dec, width, height)
                query += " AND pmra BETWEEN " + str(pmra_min)
                query += " AND " + str(pmra_max)
                query += " AND pmdec BETWEEN " + str(pmdec_min)
                query += " AND " + str(pmdec_max)
                if(self.connection == None): print("No connection")
                data = self.connection.async_query(query)
                return data
                
        def gaia_own_pm_filter(self, table, pmra_error_vs_pmra, pmdec_error_vs_pmdec, pmra, pmdec):
                """Deprecated"""
                query = "SELECT * FROM " + table
                query += " WHERE abs(pmra_error/pmra)<" + str(pmra_error_vs_pmra)
                query += " AND abs(pmdec_error/pmdec)<" + str(pmdec_error_vs_pmdec)
                query += " AND pmra IS NOT NULL AND abs(pmra)>" + str(pmra)
                query += " AND pmdec IS NOT NULL AND abs(pmdec)>" + str(pmdec)
                if(self.connection == None): print("No connection")
                data = self.connection.async_query(query)
                return data
        
        def gaia_own_pm_between_filter(self, table, pmra_max, pmra_min, pmdec_max, pmdec_min):
                """Deprecated"""
                query = "SELECT * FROM " + table
                query += " WHERE pmra BETWEEN " + str(pmra_min)
                query += " AND " + str(pmra_max)
                query += " AND pmdec BETWEEN " + str(pmdec_min)
                query += " AND " + str(pmdec_max)
                if(self.connection == None): print("No connection")
                data = self.connection.async_query(query)
                return data

        def gaia_login(self, user, passwd):
                """Logs in to the archive
                """
                return self.connection.login(user, passwd)

        def gaia_logout(self):
                """Logs out of the archive
                """
                ret = self.connection.logout()
                if ret == True: self.connection = None
                return ret

        def gaia_upload_table(self, name, table):
                """Uploads a table"""
                return self.connection.upload_table(name, table)
