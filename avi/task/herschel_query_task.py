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

@package avi.task.herschel_query_task

--------------------------------------------------------------------------------

This module manages the execution of queries to the herschel archive.

The module manages the execution of queries to the herschel archive.
"""
import sys, traceback, os
from django.utils import timezone
import time

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

class herschel_query_task(parent):
    """@class herschel_query_task
    The herschel_query_task class manages the execution of queries to the 
    herschel archive.

    It implementes the task interface and inherits the task_data attribute.

    @see task @link avi.task.task.task
    @see task_data @link avi.task.task.task_data
    """
    def output(self):
        """Deprecated"""
        pass
    def get_herschel_data(self, log, data):
        """Does a query to the herschel archive

        It will read the input contained in the data parameter and it will 
        query the herschel archive trough the interface_manager. Then it will 
        save the results using the file_manager
    
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
        log.debug('get_herschel_data method')
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
                if not coords:
                    coords = ned().get_object_coordinates(data['name'])
                if not coords:
                    log.error('Name %s not found in Simbad/Ned data bases',
                              data['name'])
                    raise err('Name %s not found in Simbad/Ned data bases',
                              data['name'])
                v_ra = coords['ra']
                v_dec = coords['dec']
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
                coords = cm.gal_to_icrs(float(v_l),float(v_b))
                ra = coords['ra']
                dec = coords['dec']
            else:
                try:
                    ra = float(v_ra)
                    dec = float(v_dec)
                except ValueError:
                    coords = cm.icrs_degrees(v_ra,v_dec)
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
                table = "v_active_observation"

            log.info("Table: %s","hsa.%s"%(table))

            if not data['positional_images']:
                log.info("Retrieving positional sources from "
                         + "the herschel archive...")
                if shape == 'cone':
                    if not data['radius']:
                        log.error("No radius provided")
                        raise err("No radius provided")
                    src = im._archive_herschel_get_circle(ra, dec,
                                                          data['radius'], table)
                elif shape == 'box':
                    if not data['width'] or not data['height']:
                        log.error("No dimensions provided")
                        raise err("No dimansions provided")
                    src = im._archive_herschel_get_box(ra, dec, data['width'],
                                                       data['height'], table)
                elif shape == 'polygon':
                    vertexes = jm.get_vertexes(data)
                    src = im._archive_herschel_get_polygon(ra,dec,vertexes,table)

                if src != None:
                    if not data.get('output_file'):
                        file_name = wh().get() \
                        .SOURCES_FMT%{"mission":"hsa",
                                      "date":str(round(time.time())),
                                      "name":"data"}
                    else:
                        file_name = wh().get() \
                        .SOURCES_FMT%{"mission":"hsa",
                                      "date":str(round(time.time())),
                                      "name":data['output_file']}
                    fm.save_file_plain_data(src,"%s.vot"%(file_name),
                                            wh().get().HSA_PATH,
                                            self.task_id, "hsa", timezone.now())
                                                #"%f_%f_%s_%s.vot" \
                                                #%(ra,dec,shape,table))
                                                
                else:
                    log.error("Something went wrong while querying the archive!")
                    raise err("Something went wrong while querying the archive!")

                log.info("Everything done!")
                return

            log.info('Retrieving maps from the herschel archive...')

            if shape == 'cone':
                if not data['radius']:
                    log.error("No radius provided")
                    raise err("No radius provided")
                if not data.get('output_file'):
                    im.archive_get_maps(ra, dec,data['radius'],data['level'],
                                                 data['instrument'],
                                                 id = self.task_id)
                else:
                    log.info("fileeeeeeeeeee")
                    im.archive_get_maps(ra, dec,data['radius'],data['level'],
                                                 data['instrument'],
                                                 id = self.task_id,
                                                 name = data['output_file'])
                log.info("Everything done!")
                return
            elif shape == 'box':
                if not data['width'] or not data['height']:
                    log.error("No dimensions provided")
                    raise err("No dimansions provided")
                if not data.get('output_file'):
                    im.archive_get_maps_box(ra, dec, data['width'], data['height'],
                                            data['level'], data['instrument'],
                                            id = self.task_id) 
                else:
                    im.archive_get_maps_box(ra, dec, data['width'], data['height'],
                                            data['level'], data['instrument'],
                                            id = self.task_id,
                                            name = data['output_file']) 
                log.info("Everything done!")
                return
            elif shape == 'polygon':
                vertexes = jm.get_vertexes(data)
                if not data.get('output_file'):
                    im.archive_get_maps_polygon(ra, dec, vertexes,
                                            data['level'], data['instrument'],
                                            id = self.task_id) 
                else:
                    im.archive_get_maps_polygon(ra, dec, vertexes,
                                            data['level'], data['instrument'],
                                            id = self.task_id,
                                            name = data['output_file'])
                log.info("Everything done!")
                return
            log.error("Something went wrong...")
            raise err("Something went wrong...")
        except Exception:
            log.error(traceback.format_exc())
            raise err(traceback.format_exc())

    def run(self):
        """Runs the query to the herschel archive.
        
        If the task_data contains the 'input_file' key it will read that value 
        and call get_herschel_data() once per input parameter found in the 
        input_file.
        
        If the task_data contains the 'adql' key it will query the archive 
        through the interface_manager using that query.

        Otherwise it will call get_herschel_data() with the input from task_data

        Args:
        self: The object pointer.

        Raises:
        task_exception: avi.task.task.task_exception

        See:
        interface_manager: avi.core.interface.interface_manager.interface_manager
        
        See also:
        get_herschel_data: get_herschel_data()
        """
        def get_herschel_data(log, data):
            """Deprecated"""
            pass
            
        log = logger().get_log('herschel_query_task')

        data = self.task_data.data
        jm = json_manager()
        if data.get('input_file') and data.get('name_coord') == 'file':
            log.info('There is an input file')
            #self.get_herschel_data(log, data)
            try:
                d = jm.read_herschel_input(data['input_file'])
                for i in d:
                    if i.get('name'):
                        i['name_coord'] = 'name'
                    if i.get('wavelength'):
                        wl = int(i['wavelength'])
                        if wl == 70 or wl == 100 or wl == 160:
                            i['tablee'] = "hsa.pacs_point_source_%s"%(str(wl).zfill(3))
                            #"cat_hppsc_%s"%(str(wl).zfill(3))
                        elif wl == 250 or wl == 350 or wl == 500:
                            i['tablee'] = "hsa.spire_point_source_%s"%(wl)
                            #"cat_spsc_%i"%(wl)
                    if i.get('positional_source'):
                        if i['positional_source'] == 'False':
                            i['positional_images'] = True
                        else:
                            i['positional_images'] = False
                    else:
                        i['positional_images'] = True
                    self.get_herschel_data(log, i)
            except Exception:
                log.error("Exception while retrieving data from herschel")
                log.error(traceback.format_exc())
                raise err(traceback.format_exc())
            finally:
                pass
                #os.remove(data['input_file'])
            return
        elif data.get('adql') and data.get('name_coord') == 'adql':
            log.info('ADQL query')
            im = risea().get().interface_manager
            fm = file_manager()
        
            adql = data['adql']

            if not im:
                log.error('There is no interface manager initialized!')
                raise err("There is no interface manager initialized!")
            src = im._archive_herschel_get_adql(adql)

            if src != None:
                if not data.get('output_file'):
                    file_name = wh().get().SOURCES_FMT%{"mission":"hsa",
                                                        "date":str(round(time.time())),
                                                        "name":"data"}
                else:
                    file_name = wh().get().SOURCES_FMT%{"mission":"hsa",
                                                        "date":str(round(time.time())),
                                                        "name":data['output_file']}
                fm.save_file_plain_data(src,"%s.vot"%(file_name),
                                        wh().get().HSA_PATH,
                                        self.task_id, "hsa", timezone.now())

            log.info("Everything done!")
            return
        else:
            if data.get('shape') == 'polygon':
                jm.set_vertexes(data, data['polygon'])
            log.info("added vertexes %s", str(data))
            self.get_herschel_data(log, data)
            return
