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
