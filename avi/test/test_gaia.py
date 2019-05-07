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