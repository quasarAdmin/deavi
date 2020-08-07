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
import os
import unittest

try:
    from avi.tests import *
except ImportError:
    import sys, os
    path = os.path.abspath(os.path.dirname(__file__))
    index = path.find("test")
    path = path[:index - 5]
    sys.path.append(path)
    from avi.tests import *

from avi.core.algorithm.algorithm_manager import algorithm_manager
from avi.models import algorithm_info_model
from avi.warehouse import wh_global_config as warehouse

class test_algorithm_mananger(unittest.TestCase):
    def __str__(self): return "test_algorithm_mananger."

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # PRIVATE ##################################################################

    _def = {"algorithm":{
        "name":"test",
        "view_name":"Test View",
        "input":{
            "input_1":{
                "name": "p1",
                "view_name": "P 1",
                "type": "float"
            },
            "input_2":{
                "name": "p2",
                "view_name": "P 2",
                "type": "integer"
            },
            "input_3":{
                "name": "p3",
                "view_name": "P 3",
                "type": "long"
            },
            "input_4":{
                "name": "p4",
                "view_name": "P 4",
                "type": "complex"
            },
            "input_5":{
                "name": "p5",
                "view_name": "P 5",
                "type": "string"
            },
            "input_6":{
                "name": "p6",
                "view_name": "P 6",
                "type": "gaia_table"
            },
            "input_7":{
                "name": "p7",
                "view_name": "P 7",
                "type": "hsa_table"
            }
        }
    }}

    _val = {"algorithm":{
        "name":"test",
        "params":{
            "p1":0.0,
            "p2":0,
            "p3":0,
            "p4":0j,
            "p5":"",
            "p6":"/data/output/",
            "p7":"/data/output/"
        }
    }}

    def _create_algorithm_info(self):
        mng = algorithm_manager()
        alg_dir = os.path.join(os.path.abspath(os.path.dirname(__file__))
                               ,'algorithms', 'installed')

        mng.update_database(alg_dir, 'installed')

        alg_dir = os.path.join(os.path.abspath(os.path.dirname(__file__))
                               ,'algorithms', 'temp')

        mng.update_database(alg_dir,'temporal')

        alg_dir = os.path.join(os.path.abspath(os.path.dirname(__file__))
                               ,'algorithms', 'uploaded')
        
        mng.update_database(alg_dir,'uploaded')

    def _delete_algorithm_info(self):
        alg_info = algorithm_info_model.objects.all()
        for i in alg_info:
            i.delete()

    def _post_exec_algorithm(self, pk = 1, name = "test", p1 = 0, 
                             p2 = 0, p3 = 0, p4 = 0,p5 = "" , p6 = "" , 
                             p7 = ""):
        ret = {str(pk)+"_p1": [p1],
               str(pk)+"_p2": [p2],
               str(pk)+"_p3": [p3],
               str(pk)+"_p4": [p4],
               str(pk)+"_p5": [p5],
               str(pk)+"_p6": [p6],
               str(pk)+"_p7": [p7]}
        return ret

    # TEST #####################################################################

    def test_update_database(self):
        test_log("Testing the updating of the database...",self)
        
        self._create_algorithm_info()

        test_log("Testing the algorithm_info_models created",self)

        alg = algorithm_info_model.objects.filter(name='installed', 
                                                  algorithm_type='installed')
        
        self.assertTrue(alg)

        alg = algorithm_info_model.objects.filter(name='temp', 
                                                  algorithm_type='temporal')

        self.assertTrue(alg)

        alg = algorithm_info_model.objects.filter(name='uploaded', 
                                                  algorithm_type='uploaded')

        self.assertTrue(alg)

        test_log("Testing the 'non-creation' of a duplicated algorithm_info_model",self)

        self._create_algorithm_info()

        alg = algorithm_info_model.objects.filter(name='installed', 
                                                  algorithm_type='installed')
        
        self.assertEqual(len(alg),1)

        alg = algorithm_info_model.objects.filter(name='temp', 
                                                  algorithm_type='temporal')

        self.assertEqual(len(alg),1)

        alg = algorithm_info_model.objects.filter(name='uploaded', 
                                                  algorithm_type='uploaded')

        self.assertEqual(len(alg),1)

        #self._delete_algorithm_info()

    def test_init_with_data(self):
        test_log("Testing the initialization method...",self)

        test_log("Changing the warehouse paths",self)

        wh = warehouse().get()

        wh.ALGORITHM_PATH = os.path.join(
            os.path.abspath(os.path.dirname(__file__)) ,'algorithms', 
            'installed')

        wh.UPLOADED_ALGORITHM_PATH = os.path.join(
            os.path.abspath(os.path.dirname(__file__)) ,'algorithms', 
            'uploaded')

        test_log("Testing the initialization with algorithm already in the database",self)

        self._create_algorithm_info()

        mng = algorithm_manager()
        mng.init()

        alg = algorithm_info_model.objects.filter(name='installed', 
                                                  algorithm_type='installed')
        
        self.assertEqual(len(alg),1)

        alg = algorithm_info_model.objects.filter(name='temp', 
                                                  algorithm_type='temporal')

        self.assertFalse(alg)

        alg = algorithm_info_model.objects.filter(name='uploaded', 
                                                  algorithm_type='uploaded')

        self.assertEqual(len(alg),1)

        #self._delete_algorithm_info()

    def test_init(self):
        test_log("Testing the initialization method...",self)

        test_log("Changing the warehouse paths",self)

        wh = warehouse().get()

        wh.ALGORITHM_PATH = os.path.join(
            os.path.abspath(os.path.dirname(__file__)) ,'algorithms', 
            'installed')

        wh.UPLOADED_ALGORITHM_PATH = os.path.join(
            os.path.abspath(os.path.dirname(__file__)) ,'algorithms', 
            'uploaded')

        test_log("Testing the initialization with an empty database",self)

        mng = algorithm_manager()
        mng.init()

        alg = algorithm_info_model.objects.filter(name='installed', 
                                                  algorithm_type='installed')
        
        self.assertEqual(len(alg),1)

        alg = algorithm_info_model.objects.filter(name='temp', 
                                                  algorithm_type='temporal')

        self.assertFalse(alg)

        alg = algorithm_info_model.objects.filter(name='uploaded', 
                                                  algorithm_type='uploaded')

        self.assertEqual(len(alg),1)

        #self._delete_algorithm_info()

    def test_get_algorithm(self):
        test_log("Testing the get_algorithm method...",self)
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            'algorithms')

        mng = algorithm_manager()

        test_log("Testing an OK file",self)

        ret = mng.get_algorithm(path+"/test.json")

        self.assertEqual(self._def, ret)
        self.assertEqual(str(self._def), str(ret))

        test_log("Testing non valid files",self)
        
        ret = mng.get_algorithm(path+"/test.py")

        self.assertIsNone(ret)
        self.assertNotEqual(self._def, ret)
        self.assertNotEqual(str(self._def), str(ret))

        ret = mng.get_algorithm(path+"/non_existing_file.json")

        self.assertIsNone(ret)
        self.assertNotEqual(self._def, ret)
        self.assertNotEqual(str(self._def), str(ret))

        ret = mng.get_algorithm(path)

        self.assertIsNone(ret)
        self.assertNotEqual(self._def, ret)
        self.assertNotEqual(str(self._def), str(ret))

        ret = mng.get_algorithm("/non/existing/path/test.json")

        self.assertIsNone(ret)
        self.assertNotEqual(self._def, ret)
        self.assertNotEqual(str(self._def), str(ret))

    def test_get_info(self):
        test_log("Testing the get_info method...",self)
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            'algorithms')

        mng = algorithm_manager()

        test_log("Testing an OK file",self)

        ret = mng.get_info(path+"/test.json",'name')

        self.assertEqual(self._def['algorithm']['name'], ret)
        self.assertEqual(str(self._def['algorithm']['name']), str(ret))

        test_log("Testing non valid files",self)
        
        ret = mng.get_info(path+"/test.py",'name')

        self.assertIsNone(ret)
        self.assertNotEqual(self._def['algorithm']['name'], ret)
        self.assertNotEqual(str(self._def['algorithm']['name']), str(ret))

        ret = mng.get_info(path+"/non_existing_file.json",'name')

        self.assertIsNone(ret)
        self.assertNotEqual(self._def['algorithm']['name'], ret)
        self.assertNotEqual(str(self._def['algorithm']['name']), str(ret))

        ret = mng.get_info(path,'name')

        self.assertIsNone(ret)
        self.assertNotEqual(self._def['algorithm']['name'], ret)
        self.assertNotEqual(str(self._def['algorithm']['name']), str(ret))

        ret = mng.get_info("/non/existing/path/test.json",'name')

        self.assertIsNone(ret)
        self.assertNotEqual(self._def['algorithm']['name'], ret)
        self.assertNotEqual(str(self._def['algorithm']['name']), str(ret))

        test_log("Testing non valied keys",self)
        
        ret = mng.get_info(path+"/test.json",'non-existiny-key')

        self.assertIsNone(ret)

        ret = mng.get_info(path+"/test.json",None)

        self.assertIsNone(ret)

    def test_has_param_type(self):
        test_log("Testing the get_info method...",self)
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            'algorithms')

        mng = algorithm_manager()

        test_log("Testing an OK file",self)

        ret = mng.has_param_type(path+"/test.json",'float')
        self.assertTrue(ret)

        ret = mng.has_param_type(path+"/test.json",'integer')
        self.assertTrue(ret)
        
        ret = mng.has_param_type(path+"/test.json",'long')
        self.assertTrue(ret)

        ret = mng.has_param_type(path+"/test.json",'complex')
        self.assertTrue(ret)

        ret = mng.has_param_type(path+"/test.json",'string')
        self.assertTrue(ret)

        ret = mng.has_param_type(path+"/test.json",'gaia_table')
        self.assertTrue(ret)

        ret = mng.has_param_type(path+"/test.json",'hsa_table')
        self.assertTrue(ret)

        test_log("Testing non valid files",self)
        
        ret = mng.has_param_type(path+"/test.py",'float')

        self.assertIsNone(ret)

        ret = mng.has_param_type(path+"/non_existing_file.json",'float')

        self.assertIsNone(ret)

        ret = mng.has_param_type(path,'float')

        self.assertIsNone(ret)

        ret = mng.has_param_type("/non/existing/path/test.json",'float')

        self.assertIsNone(ret)

        test_log("Testing non valied types",self)
        
        ret = mng.has_param_type(path+"/test.json",'non-existiny-type')

        self.assertFalse(ret)

        ret = mng.has_param_type(path+"/test.json",None)

        self.assertFalse(ret)

    def test_get_algorithm_data(self):
        test_log("Testing the get_info method...",self)
        alg_dir = os.path.join(os.path.abspath(os.path.dirname(__file__))
                               ,'algorithms')
        #algorithm_info_model.objects.create(name="test",
        #                                    source_file=alg_dir + "/test.py",
        #                                    name_view="Test View",
        #                                    definition_file=alg_dir + 
        #                                    "/test.json",
        #                                    algorithm_type="installed")

        mng = algorithm_manager()

        test_log("Testing an OK file and OK post",self)
        
        post = self._post_exec_algorithm()

        ret = mng.get_algorithm_data("1", 'test', alg_dir + "/test.json", post)
        self.assertEqual(sorted(ret), sorted(self._val))
        self.assertEqual(str(sorted(ret)), str(sorted(self._val)))

        test_log("Testing non valid files",self)

        ret = mng.get_algorithm_data("1", 'test', alg_dir + "/test.py",post)
        self.assertIsNone(ret)

        ret = mng.get_algorithm_data('1','test', 
                                     alg_dir+"/non_existing_file.json",post)
        self.assertIsNone(ret)

        ret = mng.get_algorithm_data('1','test', alg_dir,post)
        self.assertIsNone(ret)

        ret = mng.get_algorithm_data('1','test',"/non/existing/path/test.json",
                                     post)
        self.assertIsNone(ret)

        test_log("Testing non valid POST",self)

        post = None
        ret = mng.get_algorithm_data("1", 'test', alg_dir + "/test.json", post)
        self.assertIsNone(ret)

        post = {}
        ret = mng.get_algorithm_data("1", 'test', alg_dir + "/test.json", post)
        self.assertIsNone(ret)
        #self._delete_algorithm_info()

if __name__ == '__main__':
    unittest.main()
