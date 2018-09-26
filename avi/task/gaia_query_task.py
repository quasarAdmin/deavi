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

@package avi.task.gaia_query_task

--------------------------------------------------------------------------------

This module manages the execution of queries to the gaia archive.

The module manages the execution of queries to the gaia archive.
"""
import time
import sys, traceback, os
from django.utils import timezone

from .task import task as parent
from .task import task_exception as err

from avi.log import logger

from avi.core.risea import risea
from avi.core.interface.interface_manager import interface_manager
from avi.core.interface.name_solvers import simbad, ned
from avi.utils.coordinates_manager import coordinates_manager
from avi.utils.data.file_manager import file_manager
from avi.utils.data.json_manager import json_manager
from avi.warehouse import wh_global_config as wh

class gaia_query_task(parent):
    """@class gaia_query_task
    The gaia_query_task class manages the execution of queries to the gaia 
    archive.

    It implementes the task interface and inherits the task_data attribute.

    @see task @link avi.task.task.task
    @see task_data @link avi.task.task.task_data
    """
    def output(self):
        """Deprecated"""
        pass

    def get_gaia_data(self, log, data):
        """Does a query to the gaia archive

        It will read the input contained in the data parameter and it will 
        query the gaia archive trough the interface_manager. Then it will save 
        the results using the file_manager
    
        Args:
        self: The object pointer
        log: The log
        data: The input data to the query

        Raises:
        task_exception: avi.task.task.task_exception
        
        See:
        interface_manager: avi.core.interface.interface_manager.interface_manager
        
        See also:
        file_manager: avi.utils.data.file_manager.file_manager
        """
        im = risea().get().interface_manager
        fm = file_manager()
        cm = coordinates_manager()
        
        jm = json_manager()

        if not im:
            log.error('There is no interface manager initialized!')
            raise err("There is no interface manager initialized!")
        try:
            ra = None
            dec = None
            if data.get('name') and data.get('name_coord') == 'name':
                log.info("Name attr %s found, retrieving coordinates from " \
                         + "Simbad/Ned databases", data['name'])
                coords = simbad().get_object_coordinates(data['name'])
                log.debug("simbad")
                if not coords:
                    log.debug("trying ned")
                    coords = ned().get_object_coordinates(data['name'])
                    log.debug("ned")
                if not coords:
                    log.error('Name %s not found in Simbad/Ned databases',
                              data['name'])
                    raise err('Name %s not found in Simbad/Ned databases',
                              data['name'])
                log.debug("coords")
                v_ra = coords['ra']
                v_dec = coords['dec']
                log.debug("%s - %s",v_ra, v_dec)
            else:
                log.info("Retrieving coordinates from the provided data...")
                v_ra = data.get('ra')
                v_dec = data.get('dec')
            if not v_ra or not v_dec:
                log.info("No equatorial coordinates found!")
                log.info("Reading galactic coordinates from data...")
                v_l = data.get('l')
                v_b = data.get('b')
                if not v_l or not v_b:
                    log.error('No valid coordinates found')
                    raise err('No valid coordinates found')
                coords = cm.gal_to_icrs(float(v_l), float(v_b))
                ra = coords['ra']
                dec = coords['dec']
            else:
                try:
                    ra = float(v_ra)
                    dec = float(v_dec)
                except ValueError:
                    coords = cm.icrs_degrees(v_ra, v_dec)
                    ra = coords['ra']
                    dec = coords['dec']
            src = None
            shape = data['shape']
            if shape != 'cone' and shape != 'box' and shape != 'polygon':
                log.error("Unknown shape!")
                raise err("Unknown shape!")
            
            log.info("Shape: %s", shape)
            
            table = data['table']
            if not table or table == "":
                table = "gaiadr1.gaia_source"

            log.info("Table: %s",table)

            if shape == 'cone':
                if not data['radius']:
                    log.error("No radius provided")
                    raise err("No radius provided")
                src = im._archive_gaia_get_circle(ra, dec,
                                                  data['radius'], table)
            elif shape == 'box':
                if not data['width'] or not data['height']:
                    log.error("No dimensions provided")
                    raise err("No dimensions provided")
                src = im._archive_gaia_get_box(ra, dec, data['width'],
                                               data['height'], table)
            elif shape == 'polygon':
                vertexes = jm.get_vertexes(data)
                src = im._archive_gaia_get_polygon(ra, dec, vertexes, table)

            if src != None:
                if not data.get('output_file'):
                    file_name = wh().get().SOURCES_FMT%{"mission":"gaia",
                                                        "date":str(round(time.time())),
                                                        "name":"data"}
                else:
                    file_name = wh().get().SOURCES_FMT%{"mission":"gaia",
                                                        "date":str(round(time.time())),
                                                        "name":data['output_file']}
                fm.save_file_plain_data(src,"%s.vot"%(file_name),
                                        wh().get().GAIA_PATH,
                                        self.task_id, "gaia", timezone.now())

            log.info("Everything done!")
            return

        except Exception:
            log.error("ups: %s", traceback.format_exc())
            raise err('%s', traceback.format_exc())

    def run(self):
        """Runs the query to the gaia archive.
        
        If the task_data contains the 'input_file' key it will read that value 
        and call get_gaia_data() once per input parameter found in the 
        input_file.
        
        If the task_data contains the 'adql' key it will query the archive 
        through the interface_manager using that query.

        Otherwise it will call get_gaia_data() with the input from task_data

        Args:
        self: The object pointer.

        Raises:
        task_exception: avi.task.task.task_exception

        See:
        interface_manager: avi.core.interface.interface_manager.interface_manager
        
        See also:
        get_gaia_data: get_gaia_data()
        """
        log = logger().get_log('gaia_query_task')
        
        jm = json_manager()
        data = self.task_data.data

        log.info("%s",str(data))
        
        if data.get('input_file') and data.get('name_coord') == 'file':
            log.info('There is an input file')
            try:
                d = jm.read_gaia_input(data['input_file'])
                for i in d:
                    self.get_gaia_data(log, i)
            except Exception:
                log.error("Exception while retrieving data from gaia")
                log.error(traceback.format_exc())
                raise err(traceback.format_exc())
            finally:
                os.remove(data['input_file'])
            return
        elif data.get('adql') and data.get('name_coord') == 'adql':
            log.info('ADQL query')
            im = risea().get().interface_manager
            fm = file_manager()
            
            adql = data['adql']

            if not im:
                log.error('There is no interface manager initialized!')
                raise err("There is no interface manager initialized!")
            src = im._archive_gaia_get_adql(adql)

            if src != None:
                if not data.get('output_file'):
                    file_name = wh().get().SOURCES_FMT%{"mission":"gaia",
                                                        "date":str(round(time.time())),
                                                        "name":"data"}
                else:
                    file_name = wh().get().SOURCES_FMT%{"mission":"gaia",
                                                        "date":str(round(time.time())),
                                                        "name":data['output_file']}
                fm.save_file_plain_data(src,"%s.vot"%(file_name),
                                        wh().get().GAIA_PATH,
                                        self.task_id, "gaia", timezone.now())

            log.info("Everything done!")
            return
        else:
            if data.get('shape') == 'polygon':
                jm.set_vertexes(data, data['polygon'])
            self.get_gaia_data(log, data)
            return
        
        # OLD
        try:
            ra = None
            dec = None
            if data.get('name'):
                log.info("Name attr %s found, retrieving coordinates from " \
                         + "Simbad/Ned databases", data['name'])
                coords = simbad().get_object_coordinates(data['name'])
                log.debug("simbad")
                if not coords:
                    log.debug("trying ned")
                    coords = ned().get_object_coordinates(data['name'])
                    log.debug("ned")
                if not coords:
                    log.error('Name %s not found in Simbad/Ned databases',
                              data['name'])
                    raise err('Name %s not found in Simbad/Ned databases',
                              data['name'])
                log.debug("coords")
                v_ra = coords['ra']
                v_dec = coords['dec']
                log.debug("%s - %s",v_ra, v_dec)
            else:
                log.info("Retrieving coordinates from the provided data...")
                v_ra = data.get('ra')
                v_dec = data.get('dec')
            if not v_ra or not v_dec:
                log.info("No equatorial coordinates found!")
                log.info("Reading galactic coordinates from data...")
                v_l = data.get('l')
                v_b = data.get('b')
                if not v_l or not v_b:
                    log.error('No valid coordinates found')
                    raise err('No valid coordinates found')
                coords = cm.gal_to_icrs(float(v_l), float(v_b))
                ra = coords['ra']
                dec = coords['dec']
            else:
                try:
                    ra = float(v_ra)
                    dec = float(v_dec)
                except ValueError:
                    coords = cm.icrs_degrees(v_ra, v_dec)
                    ra = coords['ra']
                    dec = coords['dec']
            src = None
            shape = data['shape']
            if shape != 'cone' and shape != 'box' and shape != 'polygon':
                log.error("Unknown shape!")
                raise err("Unknown shape!")
            
            log.info("Shape: %s", shape)
            
            table = data['table']
            if not table or table == "":
                table = "gaiadr1.gaia_source"

            log.info("Table: %s",table)

            if shape == 'cone':
                if not data['radius']:
                    log.error("No radius provided")
                    raise err("No radius provided")
                src = im._archive_gaia_get_circle(ra, dec,
                                                  data['radius'], table)
            elif shape == 'box':
                if not data['width'] or not data['height']:
                    log.error("No dimensions provided")
                    raise err("No dimensions provided")
                src = im._archive_gaia_get_box(ra, dec, data['width'],
                                               data['height'], table)
            elif shape == 'polygon':
                # TODO
                src = im._archive_gaia_get_polygon(ra, dec, None, table)

            if src != None:
                if not data.get('output_file'):
                    file_name = wh().get().SOURCES_FMT%{"mission":"gaia",
                                                        "date":str(round(time.time())),
                                                        "name":"data"}
                else:
                    file_name = wh().get().SOURCES_FMT%{"mission":"gaia",
                                                        "date":str(round(time.time())),
                                                        "name":data['output_file']}
                fm.save_file_plain_data(src,"%s.vot"%(file_name),
                                        wh().get().GAIA_PATH,
                                        self.task_id, "gaia", timezone.now())

            log.info("Everything done!")
            return

        except Exception:
            log.error("ups: %s", traceback.format_exc())
            raise err('%s', traceback.format_exc())
                
            
        # OLD
        if not data['table']:
            res = im.archive_get_circle(data['ra'],data['dec'],data['radius'],
                                        params = data['params'])
            fm.save_file_plain_data(res,
                                    "%f_%f_%f_%s.vot"\
                                    %(data['ra'],data['dec'],
                                      data['radius'],"default"))
        else:
            log.info('retrieving gaia data...')
            log.info('im ptr : ')
            res = im.archive_get_circle(data['ra'],data['dec'],data['radius'],
                                  data['table'],
                                  params = data['params'])
            if res:
                log.info('saving gaia data...')
                file_name = wh().get() \
                .SOURCES_FMT%{"mission":"gaia",
                              "date":str(round(time.time())),
                              "name":"data"}
                #data['name']}
                fm.save_file_plain_data(res,"%s.vot"%(file_name),
                                        #"%f_%f_%f_%s.vot"\
                                        #%(data['ra'],data['dec'],
                                        #  data['radius'],data['table']),
                                        wh().get().GAIA_PATH,
                                        self.task_id, "gaia", timezone.now())
            else:
                log.error("Something went wrong while querying the archive!")
                raise err("Something went wrong while querying the archive!")
            log.info("Everything done!")
                
