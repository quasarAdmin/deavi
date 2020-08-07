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
"""

import traceback

from .risea import risea

def get_positional_sources_from_herschel(input_file):
    
    from avi.utils.data.json_manager import json_manager
    from avi.utils.data.file_manager import file_manager
    from avi.utils.coordinates_manager import coordinates_manager
    from avi.core.interface.name_solvers import simbad, ned
    
    jm = json_manager()
    fm = file_manager()
    cm = coordinates_manager()
    r = risea().get()
    im = r.interface_manager
    data = jm.read_herschel_input(input_file)
    c = 0
    for i in data:
        c += 1
        try:
            ra = None
            dec = None
            if i.get('name'):
                coords = simbad().get_object_coordinates(i['name'])
                if not coords:
                    coords = ned().get_object_coordinates(i['name'])
                if not coords:
                    continue
                v_ra = coords['ra']
                v_dec = coords['dec']
            else:
                v_ra = i.get('ra')
                v_dec = i.get('dec')
                
            if not v_ra or not v_dec:
                v_l = i.get('l')
                v_b = i.get('b')
                if not v_l or not v_b:
                    continue
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
            table = None
            src = None
            wl = int(i['wavelength'])
            if wl == 70 or wl == 100 or wl == 160:
                table = "cat_hppsc_%s"%(str(wl).zfill(3))
            elif wl == 250 or wl == 350 or wl == 500:
                table = "cat_spsc_%i"%(wl)
            if i['shape'] == 'cone':
                radius = float(i['radius'])
                src = im._archive_herschel_get_circle(ra,dec,radius,table)
            elif i['shape'] == 'box':
                width = float(i['width'])
                height = float(i['height'])
                src = im._archive_herschel_get_box(ra,dec,width,height,table)
            elif i['shape'] == 'polygon':
                vertexes = jm.get_vertexes(i)
                src = im._archive_herschel_get_polygon(ra,dec,vertexes,table)
                
            if src != None:
                if i.get('output_file'):
                    fm.save_file_plain_data(src,"%s.vot"%(i['output_file']))
                else:
                    fm.save_file_plain_data(src,"source_%i.vot"%(c))
        except ValueError as e:
            print("Value Error")
            print(traceback.format_exc())
            pass
        except Exception as e:
            print("Exception")
            print(traceback.format_exc())
            pass

def get_maps_from_herschel(input_file):

    from avi.utils.data.json_manager import json_manager
    from avi.utils.data.file_manager import file_manager
    from avi.utils.coordinates_manager import coordinates_manager
    from avi.core.interface.name_solvers import simbad, ned
    
    jm = json_manager()
    fm = file_manager()
    cm = coordinates_manager()
    r = risea().get()
    im = r.interface_manager
    data = jm.read_herschel_input(input_file)
    c = 0
    for i in data:
        c += 1
        try:
            ra = None
            dec = None
            if i.get('name'):
                coords = simbad().get_object_coordinates(i['name'])
                if not coords:
                    coords = ned().get_object_coordinates(i['name'])
                if not coords:
                    continue
                v_ra = coords['ra']
                v_dec = coords['dec']
            else:
                v_ra = i.get('ra')
                v_dec = i.get('dec')
                
            if not v_ra or not v_dec:
                v_l = i.get('l')
                v_b = i.get('b')
                if not v_l or not v_b:
                    continue
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
            table = None
            src = None
            wl = int(i['wavelength'])
            if wl == 70 or wl == 100 or wl == 160:
                table = "cat_hppsc_%s"%(str(wl).zfill(3))
            elif wl == 250 or wl == 350 or wl == 500:
                table = "cat_spsc_%i"%(wl)
            radius = float(i['size'])
            im.archive_get_maps(ra,dec, radius, 'All', 'PACS', table = table) 
        except ValueError as e:
            print("Value Error")
            print(traceback.format_exc())
            pass
        except Exception as e:
            print("Exception")
            print(traceback.format_exc())
            pass
