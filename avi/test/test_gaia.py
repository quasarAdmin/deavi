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

from avi.core.interface_manager import interface_manager
from avi.utils.config_manager import configuration_manager

class test_gaia(unittest.TestCase):
    def __str__(self): return "test_gaia."

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
    
    str_config_file = "im_config.xml"
    str_bad_config_file = "im_bad_config.xml"

    adql_query = ""

    def _get_config_file(self, fname):
        return os.path.join(
                os.path.abspath(os.path.dirname(__file__)) ,'config', fname)

    # TEST #####################################################################

    def test_init(self):
        test_log("Testing the initialization method...",self)
        cfg = configuration_manager()
        if not cfg.load(self._get_config_file(self.str_config_file)):
            self.assertTrue(False)
        im = interface_manager()
        im.init(cfg)
        self.assertNotNone(im.gaia_config)
        if not cfg.load(self._get_config_file(self.str_bad_config_file)):
            self.assertTrue(False)
        im.init(cfg)
        self.assertNone(im.gaia_config)
        self.assertFalse(cfg.load(""))
        
    def test_get_adql(self):
        if not cfg.load(self._get_config_file(self.str_config_file)):
            self.assertTrue(False)
        im = interface_manager()
        im.init(cfg)
        self.assertNotNone(im.get_adql(self.adql_query))
        self.assertNone(im.get_adql(""))

    def test_get_circle(self):
        if not cfg.load(self._get_config_file(self.str_config_file)):
            self.assertTrue(False)
        im = interface_manager()
        im.init(cfg)
        # TODO:
        self.assertNotNone(im.get_circle(ra, dec, radius))

    def test_get_box(self):
        pass
    def test_get_polygon(self):
        pass