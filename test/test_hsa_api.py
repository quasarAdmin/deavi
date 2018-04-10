################################################################################
import unittest
import os.path
import json

try:
    from avi.core.api import get_positional_sources_from_herschel as positional
    from avi.core.api import get_maps_from_herschel as maps
except ImportError:
    import sys, os
    path = os.path.abspath(os.path.dirname(__file__))
    index = path.find("test")
    path = path[:index - 5]
    sys.path.append(path)
    from avi.core.api import get_positional_sources_from_herschel as positional
    from avi.core.api import get_maps_from_herschel as maps

class test_hsa_api(unittest.TestCase):

    # positional
    def _positional_input(self, filedata, outputfile='source_1', verbose=False):
        if verbose: print("testing: ",str(filedata))
        input_file = '/data/input/temp.json'
        output_file = '/data/output/'+outputfile+'.vot'
        fp = open(input_file, "w")
        jsondata = json.dumps(filedata)
        fp.write(jsondata)
        fp.close()
        positional(input_file)
        self.assertTrue(os.path.isfile(output_file))
        os.path.exists(input_file) and os.remove(input_file)
        os.path.exists(output_file) and os.remove(output_file)
        if verbose: print("test: OK")
        
    def test_positional_eq_cone_70_table_ok(self):
        filedata = {"input":{
                "source_1":{
                    "ra":"100.2417",
                    "dec":"9.895",
                    "shape":"cone",
                    "radius":"0.5",                    
                    "wavelength":"70",
                    "output":"table"
                }
            }}
        print(self.test_positional_eq_cone_70_table_ok.__name__)
        self._positional_input(filedata)

    def test_positional_eq_cone_70_table_outputname_ok(self):
        filedata = {"input":{
                "source_1":{
                    "output_file":"ngc2264",
                    "ra":"100.2417",
                    "dec":"9.895",
                    "shape":"cone",
                    "radius":"0.5",                    
                    "wavelength":"70",
                    "output":"table"
                }
            }}
        print(self.test_positional_eq_cone_70_table_outputname_ok.__name__)
        self._positional_input(filedata,"ngc2264")

    def test_positional_eq_box_70_table_ok(self):
        filedata = {"input":{
                "source_1":{
                    "ra":"100.2417",
                    "dec":"9.895",
                    "shape":"box",
                    "width": "1",
                    "height": "0.6",
                    "wavelength":"70",
                    "output":"table"
                }
            }}
        print(self.test_positional_eq_box_70_table_ok.__name__)
        self._positional_input(filedata)

    def test_positional_eq_polygon_70_table_ok(self):
        filedata = {"input":{
                "source_1":{
                    "ra":"10.0",
                    "dec":"-10.5",
                    "shape":"polygon",
                    "vertex_1":{"ra":"20.0", "dec":"20.5"},
                    "vertex_2":{"ra":"30.0", "dec":"30.5"},
                    "wavelength":"70",
                    "output":"table"
                }
            }}
        print(self.test_positional_eq_polygon_70_table_ok.__name__)
        self._positional_input(filedata)

    def test_positional_gal_cone_70_table_ok(self):
        filedata = {"input":{
                "source_1":{
                    "l":"202.9357",
                    "b":"2.1957",
                    "shape":"cone",
                    "radius": "0.5",
                    "wavelength":"70",
                    "output":"table"
                }
            }}
        print(self.test_positional_gal_cone_70_table_ok.__name__)
        self._positional_input(filedata)

    def test_positional_eqj2000_cone_70_table_ok(self):
        filedata = {"input":{
                "source_1":{
                    "ra":"06 40 58.000",
                    "dec":"+09 53 42.00",
                    "shape":"cone",
                    "radius": "0.5",
                    "wavelength":"70",
                    "output":"table"
                }
            }}
        print(self.test_positional_eqj2000_cone_70_table_ok.__name__)
        self._positional_input(filedata)

    def test_positional_eqj2000_cone_70_table_2_ok(self):
        filedata = {"input":{
                "source_1":{
                    "ra":"06h40m58.000s",
                    "dec":"+09d53m42.00s",
                    "shape":"cone",
                    "radius": "0.5",
                    "wavelength":"70",
                    "output":"table"
                }
            }}
        print(self.test_positional_eqj2000_cone_70_table_2_ok.__name__)
        self._positional_input(filedata)

    def test_positional_name_cone_70_table_ok(self):
        filedata = {"input":{
                "source_1":{
                    "name":"ngc2264",
                    "shape":"cone",
                    "radius": "0.5",
                    "wavelength":"70",
                    "output":"table"
                }
            }}
        print(self.test_positional_name_cone_70_table_ok.__name__)
        self._positional_input(filedata)
        
    # maps
    def test_maps(self):
        pass

if __name__ == '__main__':
    unittest.main()
