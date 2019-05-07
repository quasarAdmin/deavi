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
    from avi.tests import test_log
except ImportError:
    import sys, os
    path = os.path.abspath(os.path.dirname(__file__))
    index = path.find("test")
    path = path[:index - 5]
    sys.path.append(path)
    from avi.tests import test_log
    
class test_interface(unittest.TestCase):
    def __str__(self): return "test_interface."

    @classmethod
    def setUpClass(cls):
        test_log("Setupclass...", cls)

    @classmethod
    def tearDownClass(cls):
        test_log("teardownclass",cls)

    def setUp(self):
        test_log("setup",self)

    def tearDown(self):
        test_log("teardown",self)

    def test_init(self):
        test_log("Initialization...", self)

    def test_delete(self):
        test_log("delete...", self)

if __name__ == '__main__':
    unittest.main()
