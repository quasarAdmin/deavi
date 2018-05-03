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
# Gaia interface

#from .connection.connection import connection
from .archive_interface import archive_interface
#from risea.utils.adql_helper import adql_helper
from avi.utils.adql_helper import adql_helper

#from risea.log import logger
from avi.log import logger

class gaia(archive_interface):

        def __init__(self):
                super(gaia, self).__init__()
                self.log = logger().get_log('gaia')

        def get_circle(self, ra, dec, radius, table = "gaiadr1.gaia_source", params = None):
                return super(gaia, self).get_circle(ra, dec, radius, table, params)
                
        def get_box(self, ra, dec, width, height, table = "gaiadr1.gaia_source", params = None):
                return super(gaia, self).get_box(ra, dec, width, height, table, params)
                
        def get_polygon(self, ra, dec, vertexes, table = "gaiadr1.gaia_source", params = None):
                return super(gaia, self).get_polygon(ra, dec, vertexes, table, params)

        # parallax filter
        def get_circle_parallax(self, ra, dec, radius, minpar, maxpar, table = "gaiadr1.tgas_source", params = None):
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
                query = "SELECT * FROM " + table
                query += " WHERE abs(pmra_error/pmra)<" + str(pmra_error_vs_pmra)
                query += " AND abs(pmdec_error/pmdec)<" + str(pmdec_error_vs_pmdec)
                query += " AND pmra IS NOT NULL AND abs(pmra)>" + str(pmra)
                query += " AND pmdec IS NOT NULL AND abs(pmdec)>" + str(pmdec)
                if(self.connection == None): print("No connection")
                data = self.connection.async_query(query)
                return data
        
        def gaia_own_pm_between_filter(self, table, pmra_max, pmra_min, pmdec_max, pmdec_min):
                query = "SELECT * FROM " + table
                query += " WHERE pmra BETWEEN " + str(pmra_min)
                query += " AND " + str(pmra_max)
                query += " AND pmdec BETWEEN " + str(pmdec_min)
                query += " AND " + str(pmdec_max)
                if(self.connection == None): print("No connection")
                data = self.connection.async_query(query)
                return data

        def gaia_login(self, user, passwd):
                return self.connection.login(user, passwd)

        def gaia_logout(self):
                ret = self.connection.logout()
                if ret == True: self.connection = None
                return ret

        def gaia_upload_table(self, name, table):
                return self.connection.upload_table(name, table)
