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
