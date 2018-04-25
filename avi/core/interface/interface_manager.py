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
from avi.log import logger

from .gaia import gaia
from .herschel import herschel

class interface_manager:

    log = None
    str_log_header = 'interface_manager'

    gaia_config = None
    herschel_config = None
    
    def __init__(self):
        self.log = logger().get_log(self.str_log_header)

    def init(self, cfg):
        self.gaia_config = cfg.get("gaia")
        self.herschel_config = cfg.get("herschel")
    
    def archive_get_adql(self, query, mission = 'gaia'):
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
                         id = None):
        self.log.info("Retrieving maps from the %s archive...", mission)
        if mission == 'herschel':
            return self._archive_herschel_get_maps(ra,dec,radius,level,instrument, table, id)
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
                                   level, instrument, table, id):
        if not self.herschel_config:
            self.log.error('There is no configuration loaded!')
            return None
        h = herschel()
        if not h.init(self.herschel_config):
            self.log.error('Failed to load the herschel interaface!')
            return None
        h.job_id = id
        return h.get_images(ra,dec,radius,level,instrument,table=table)#, True)

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
