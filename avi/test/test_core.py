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
    from avi.core.risea import risea
    from avi.tests import test_log
    from avi.models import algorithm_info_model
except ImportError:
    import sys, os
    path = os.path.abspath(os.path.dirname(__file__))
    index = path.find("test")
    #path = path[:index - 1]
    path = path[:index - 5]
    sys.path.append(path)
    from avi.core.risea import risea
    from avi.tests import test_log
    from avi.models import algorithm_info_model
    
class test_core(unittest.TestCase):
    def __str__(self): return "test_risea."

    @classmethod
    def setUpClass(cls):
        pass
        """
        test_log("Setting up the enviroment for the AVI testing...", cls)
        input_dir = os.path.join(os.path.abspath(os.path.dirname(__file__))
                                 ,'input')
        alg_dir = os.path.join(os.path.abspath(os.path.dirname(__file__))
                               ,'algorithms')
        test_log("Input path: %s"%(input_dir),cls)
        test_log("Algorithms path: %s"%(alg_dir),cls)
        algorithm_info_model.objects.create(name="test",
                                            source_file=alg_dir + "/test.py",
                                            name_view="Test View",
                                            definition_file=alg_dir + 
                                            "/test.json",
                                            algorithm_type="installed")
        """
    @classmethod
    def tearDownClass(cls):
        test_log("teardownclass",cls)

    def setUp(self):
        test_log("setup",self)
        pass

    def tearDown(self):
        test_log("teardown",self)

    def test_init(self):
        test_log("Initialization...")
        r = risea().get()
        #ai = algorithm_info_model.objects.all()
        #self.assertIsNotNone(ai)
        #test_log(str(ai),self)

    def test_delete(self):
        test_log("delete...")

if __name__ == '__main__':
    unittest.main()
