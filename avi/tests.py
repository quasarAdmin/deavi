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
import inspect

from django.test import TestCase

"""

assertEqual(a,b)
assertNotEqual(a,b)
assertTrue(x)
assertFalse(x)
assertIs(a,b)
assertIsNot(a,b)
assertIsNone(x)
assertIsNotNone(x)
assertIn(a,b)
assertNotIn(a,b)
assertIsInstance(a,b)
assertNotIsInstance(a,b)
assertRaises(exc, fun, *args, **kwds)
assertRaisesRegexp(exc, r, fun, *args, **kwds)

"""

VERBOSE = False
INFO = True

def test_log(message = "", obj = None):
    if not VERBOSE: return
    if not obj: obj_name = ""
    else: obj_name = str(obj)
    try:
        caller = inspect.stack()[1][3]
    except:
        caller = ""
    print("[LOG] (" + obj_name + caller + "): " + message)

def test_info(message = "", obj = None):
    if not INFO: return
    if not obj: obj_name = ""
    else: obj_name = str(obj)
    try:
        caller = inspect.stack()[1][3]
    except:
        caller = ""
    print("[INFO] (" + obj_name + caller + "): " + message)
"""
class test_avi(TestCase):
    def __str__(self):
        return "test_avi."

    def setUp(self):
        test_log("Setting up the enviroment for the AVI testing...", self)
        input_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 'test','input')
        alg_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               'test','algorithms')
        test_log("Input path: %s"%(input_dir),self)
        test_log("Algorithms path: %s"%(alg_dir),self)
        algorithm_info_model.objects.create(name="test",
                                            source_file=alg_dir + "/test.py",
                                            name_view="Test View",
                                            definition_file=alg_dir + 
                                            "/test.json",
                                            algorithm_type="installed")
    def test_avi_initialization(self):
        test_log("Testing the AVI initialization...",self)
        ai = algorithm_info_model.objects.get(pk=1)
        test_log("algorithm_info_model created %s"%(str(not ai == None)))
        test_log("algorithm_info_model created %s"%(ai.name))

    def test_aaa(self):
        test_log("Testing AAA...",self)
        
"""     
"""
class test_pipeline_jobs(TestCase):
    def setUp(self):
        print("Setting up models for the %s"%(test_pipeline_jobs.__name__))
        pass
    def test_abort(self):
        from avi.test.avi_core_pipeline_job_abort import test_job_abort
        #unittest.main()
        pass"""
        

# Create your tests here.
