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

@package avi.core.interface.interface_manager

--------------------------------------------------------------------------------

This module manages the interfaces to the gaia and herschel archives.
"""
from avi.log import logger

from .gaia import gaia
from .herschel import herschel

class interface_manager:
    """@class interface_manager
    The interface_manager manages the interfaces to the gaia and herschel 
    archives.
    """
    ## the log
    log = None
    ## the log header
    str_log_header = 'interface_manager'
    ## the gaia archive configuration
    gaia_config = None
    ## the herschel archive configuration
    herschel_config = None
    
    def __init__(self):
        """The class constructor

        The constructor just initializes the log
        
        Args:
        self: The object pointer.
        """
        self.log = logger().get_log(self.str_log_header)

    def init(self, cfg):
        """Initializes the gaia and herschel archives configuration

        This methos extracts the gaia and herschel configurations from the 
        global configuration.
        
        Args:
        self: The object pointer
        cfg: The global configuration
        """
        self.gaia_config = cfg.get("gaia")
        self.herschel_config = cfg.get("herschel")
    
    def archive_get_adql(self, query, mission = 'gaia'):
        """Does an ADQL query to an archive.

        This method does an ADQL query to the given archive.

        Args:
        self: The object pointer.
        query: The ADQL query
        mission: The archive to be queried

        Returns:
        The data retrieved from the archive if the query was done correctly, 
        None otherwise
        """
        self.log.info("Doing a custom ADQL query to the %s archive...", mission)
        if mission == 'gaia':
            return self._archive_gaia_get_adql(query)
        elif mission == 'herschel':
            return self._archive_herschel_get_adql(query)
        else:
            self.log.error("Unknow mission %s", mission)
            return None

    def archive_get_circle(self, ra, dec, radius, table = None, params = None,
                           mission = 'gaia'):
        """Does a conical query to an archive.
        
        This method does a conical query to the given archive.

        Args:
        self: The object pointer
        ra: The ra coordinate
        dec: The dec coordinate
        radius: The radius of the query
        table: The table to be queried
        params: Special parameters for the query
        mission: The archive to be queried

        Returns:
        The data retrieved from the archive if the query was done correctly, 
        None otherwise
        """
        self.log.info("Doing a conical query to the %s archive...", mission)
        if mission == 'gaia':
            return self._archive_gaia_get_circle(ra,dec,radius,table,params)
        elif mission == 'herschel':
            return self._archive_herschel_get_circle(ra,dec,radius,table,params)
        else:
            self.log.error("Unknow mission %s",mission)
            return None
        
    def archive_get_box(self, ra, dec, width, height,
                        table = None, params = None, mission = 'gaia'):
        """Does a box-shape query to an archive.
        
        This method does a box-shape query to the given archive.

        Args:
        self: The object pointer
        ra: The ra coordinate
        dec: The dec coordinate
        width: The width of the box
        height: The height of the box
        table: The table to be queried
        params: Special parameters for the query
        mission: The archive to be queried

        Returns:
        The data retrieved from the archive if the query was done correctly, 
        None otherwise
        """
        self.log.info("Doing a box query to the %s archive...", mission)
        if mission == 'gaia':
            # FIXME:
            return None
            return self._archive_gaia_get_box(ra,dec,width,height,table,params)
        elif mission == 'herschel':
            return self._archive_herschel_get_box(ra,dec,width,height,table,params)
        else:
            self.log.error("Unknow mission %s",mission)
            return None
        
    def archive_get_polygon(self, ra, dec, vertexes,
                        table = None, params = None, mission = 'gaia'):
        """Does a polygonal query to an archive.
        
        This method does a polygonal query to the given archive.

        Args:
        self: The object pointer
        ra: The ra coordinate
        dec: The dec coordinate
        vertexes: An array of vertex forming the polygon
        table: The table to be queried
        params: Special parameters for the query
        mission: The archive to be queried

        Returns:
        The data retrieved from the archive if the query was done correctly, 
        None otherwise
        """
        self.log.info("Doing a polygonal query to the %s archive...", mission)
        if mission == 'gaia':
            # FIXME:
            return None
            return self._archive_gaia_get_polygon(ra,dec,vertexes,table,params)
        elif mission == 'herschel':
            return self._archive_herschel_get_polygon(ra,dec,vertexes,table,params)
        else:
            self.log.error("Unknow mission %s",mission)
            return None
        
    def archive_get_maps(self, ra, dec, radius, level = "All",
                         instrument = 'PACS', mission = 'herschel', table = None,
                         id = None, name = "data"):
        """Does a conical query to an archive.
        
        This method does a conical query to the given archive and retrieves the 
        maps in that area.

        Args:
        self: The object pointer
        ra: The ra coordinate
        dec: The dec coordinate
        radius: The radius of the query
        level: The processing level
        instrument: The instrument
        mission: The archive to be queried
        table: The table to be queried
        id: The id of the observation

        Returns:
        The data retrieved from the archive if the query was done correctly, 
        None otherwise
        """
        self.log.info("Retrieving maps from the %s archive...", mission)
        if mission == 'herschel':
            return self._archive_herschel_get_maps(ra,dec,radius,level,instrument, table, id, name)
        else:
            self.log.error("Unknow mission %s", mission)
            return None

    def archive_get_maps_box(self, ra, dec, width, height, level = "All",
                         instrument = 'PACS', mission = 'herschel', table = None,
                         id = None, name = "data"):
        """Does a box-shape query to an archive.
        
        This method does a box-shape query to the given archive and retrieves the 
        maps in that area.

        Args:
        self: The object pointer
        ra: The ra coordinate
        dec: The dec coordinate
        width: The width of the box
        height: The height of the box
        level: The processing level
        instrument: The instrument
        mission: The archive to be queried
        table: The table to be queried
        id: The id of the observation

        Returns:
        The data retrieved from the archive if the query was done correctly, 
        None otherwise
        """
        self.log.info("Retrieving maps from the %s archive...", mission)
        if mission == 'herschel':
            return self._archive_herschel_get_maps_box(ra,dec,width,height,level,instrument, table, id, name)
        else:
            self.log.error("Unknow mission %s", mission)
            return None

    def archive_get_maps_polygon(self, ra, dec, vertexes, level = "All",
                         instrument = 'PACS', mission = 'herschel', table = None,
                         id = None, name = "data"):
        """Does a polygonal query to an archive.
        
        This method does a polygonal query to the given archive and retrieves the 
        maps in that area.

        Args:
        self: The object pointer
        ra: The ra coordinate
        dec: The dec coordinate
        vertexes: An array of vertex forming the polygon
        level: The processing level
        instrument: The instrument
        mission: The archive to be queried
        table: The table to be queried
        id: The id of the observation

        Returns:
        The data retrieved from the archive if the query was done correctly, 
        None otherwise
        """
        self.log.info("Retrieving maps from the %s archive...", mission)
        if mission == 'herschel':
            return self._archive_herschel_get_maps_polygon(ra,dec,vertexes,level,instrument, table, id, name)
        else:
            self.log.error("Unknow mission %s", mission)
            return None
    #
    # Gaia
    #
    def _archive_gaia_get_adql(self, query):
        if not self.gaia_config:
            self.log.error('There is no configuration loaded!')
            return None
        g = gaia()
        if not g.init(self.gaia_config):
            self.log.error('Failed to load the gaia interface!')
            return None
        return g.get_adql(query)

    def _archive_gaia_get_circle(self, ra, dec, radius, table, params = None):
        if not self.gaia_config:
            self.log.error('There is no configuration loaded!')
            return None
        g = gaia()
        if not g.init(self.gaia_config):
            self.log.error('Failed to load the gaia interface!')
            return None
        if not table or table == "":
            return g.get_circle(ra,dec,radius,params = params)
        else:
            return g.get_circle(ra,dec,radius,table,params)
    
    def _archive_gaia_get_box(self, ra, dec, width, height, table, params = None):
        if not self.gaia_config:
            self.log.error('There is no configuration loaded!')
            return None
        g = gaia()
        if not g.init(self.gaia_config):
            self.log.error('Failed to load the gaia interface!')
            return None
        if not table or table == "":
            return g.get_box(ra,dec,width,height,params = params)
        else:
            return g.get_box(ra,dec,width,height,table,params)
    
    def _archive_gaia_get_polygon(self, ra, dec, vertexes, table, params = None):
        if not self.gaia_config:
            self.log.error('There is no configuration loaded!')
            return None
        g = gaia()
        if not g.init(self.gaia_config):
            self.log.error('Failed to load the gaia interface!')
            return None
        if not table or table == "":
            return g.get_polygon(ra,dec,vertexes,params = params)
        else:
            return g.get_polygon(ra,dec,vertexes,table,params)
    #
    # Herschel
    #
    def _archive_herschel_get_adql(self, query):
        if not self.herschel_config:
            self.log.error('There is no configuration loaded!')
            return None
        h = herschel()
        if not h.init(self.herschel_config):
            self.log.error('Failed to load the herschel interface!')
            return None
        return h.get_adql(query)

    def _archive_herschel_get_circle(self, ra, dec, radius, table, params = None):
        if not self.herschel_config:
            self.log.error('There is no configuration loaded!')
            return None
        h = herschel()
        if not h.init(self.herschel_config):
            self.log.error('Failed to load the herschel interaface!')
            return None
        if not table or table == "":
            return h.get_circle(ra,dec,radius,params = params)
        
        return h.get_circle(ra,dec,radius,table,params)
        
    def _archive_herschel_get_box(self, ra, dec, width, height,
                                  table, params = None):
        if not self.herschel_config:
            self.log.error('There is no configuration loaded!')
            return None
        h = herschel()
        if not h.init(self.herschel_config):
            self.log.error('Failed to load the herschel interface!')
            return None
        if not table or table == "":
            return h.get_box(ra,dec,width,height,params = params)

        return h.get_box(ra,dec,width,height,table,params)

    def _archive_herschel_get_polygon(self, ra, dec, vertexes,
                                      table, params = None):
        if not self.herschel_config:
            self.log.error('There is no configuration loaded!')
            return None
        h = herschel()
        if not h.init(self.herschel_config):
            self.log.error('Failed to load the herschel interface!')
            return None
        if not table or table == "":
            return h.get_polygon(ra,dec,vertexes,params = params)

        return h.get_polygon(ra,dec,vertexes,table,params)

    def _archive_herschel_get_maps(self, ra, dec, radius, 
                                   level, instrument, table, id, name):
        if not self.herschel_config:
            self.log.error('There is no configuration loaded!')
            return None
        h = herschel()
        if not h.init(self.herschel_config):
            self.log.error('Failed to load the herschel interaface!')
            return None
        h.job_id = id
        return h.get_images(ra,dec,radius,level,instrument,table=table, name=name)#, True)

    def _archive_herschel_get_maps_box(self, ra, dec, width, height, 
                                   level, instrument, table, id, name):
        if not self.herschel_config:
            self.log.error('There is no configuration loaded!')
            return None
        h = herschel()
        if not h.init(self.herschel_config):
            self.log.error('Failed to load the herschel interaface!')
            return None
        h.job_id = id
        return h.get_images_box(ra,dec,width,height,level,instrument,table=table, name=name)

    def _archive_herschel_get_maps_polygon(self, ra, dec, vertexes, 
                                   level, instrument, table, id, name):
        if not self.herschel_config:
            self.log.error('There is no configuration loaded!')
            return None
        h = herschel()
        if not h.init(self.herschel_config):
            self.log.error('Failed to load the herschel interaface!')
            return None
        h.job_id = id
        return h.get_images_polygon(ra,dec,vertexes,level,instrument,table=table, name=name)

    def archive_get_maps_by_id(self, obsid, level="All", instrument = 'PACS',
                               mission = 'herschel'):
        self.log.info("Retrieving maps from the %s archive...", mission)
        if mission == 'herschel':
            return _archive_herschel_get_maps_by_id(obsid,level,instrument)
        else:
            self.log.error("Unknow mission %s", mission)
            return None

    def _archive_herschel_get_maps_by_id(self, obsid, level, instrument):
        if not self.herschel_config:
            self.log.error('There is no configuration loaded!')
            return None
        h = herschel()
        if not h.init(self.herschel_config):
            self.log.error('Failed to load the herschel interaface!')
            return None
        return h.get_images_by_id(obsid,level,instrument)
