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
    from avi.tests import *
except ImportError:
    import sys, os
    path = os.path.abspath(os.path.dirname(__file__))
    index = path.find("test")
    path = path[:index - 5]
    sys.path.append(path)
    from avi.tests import *
    
from avi.task.algorithm_task import algorithm_task as task
from avi.task.task import task_exception
from avi.models import algorithm_info_model

class test_task(unittest.TestCase):
    def __str__(self): return "test_task."

    @classmethod
    def setUpClass(cls):
        test_log("setupclass...", cls)

    @classmethod
    def tearDownClass(cls):
        test_log("teardownclass",cls)

    def setUp(self):
        test_log("setup",self)

    def tearDown(self):
        test_log("teardown",self)

    # PRIVATE ##################################################################

    _exec = '{"algorithm":{"name":"test","params":{"p1":0.0,"p2":0,"p3":0,'+ \
    '"p4":0j,"p5":"EXEC","p6":"'+os.path.dirname(os.path.realpath(__file__))+ \
    '/test.dat","p7":"/data/output/"}}}'
    _bad_data = '{Bad data]'
    _bad_data_no_name = '{"algorithm":{"params":{"p1":0.0,"p2":0,"p3":0,"p4":0j,"p5":"CRASH","p6":"/data/output/","p7":"/data/output/"}}}'
    _bad_data_db = '{"algorithm":{"name":"no_db","params":{"p1":0.0,"p2":0,"p3":0,"p4":0j,"p5":"CRASH","p6":"/data/output/","p7":"/data/output/"}}}'
    _crash = '{"algorithm":{"name":"test","params":{"p1":0.0,"p2":0,"p3":0,"p4":0j,"p5":"CRASH","p6":"/data/output/","p7":"/data/output/"}}}'

    # TEST #####################################################################

    def test_algorithm_run(self):
        test_log("Testing the algorithm_task run method...",self)
        t = task()
        t.task_data.data = self._exec
        t.task_id = 1
        t.run()
        
        test_file = os.path.dirname(os.path.realpath(__file__))+"/test.dat"

        f = open(test_file)
        fdata = f.read()
        f.close()
        
        data = "0.0\n0\n0\n0j\nEXEC\n"+test_file+"\n/data/output/"
        self.assertEqual(data, fdata)
    
        os.remove(test_file)

        t.task_data.data = self._crash
        t.task_id = 1
        self.assertRaises(task_exception, t.run)

        t.task_data.data = self._bad_data
        t.task_id = 1
        self.assertRaises(task_exception, t.run)

        t.task_data.data = self._bad_data_db
        t.task_id = 1
        self.assertRaises(task_exception, t.run)

if __name__ == '__main__':
    unittest.main()
