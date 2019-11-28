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

@package avi.task.sim_query_task

--------------------------------------------------------------------------------

This module manages the execution of queries to the simulations server.

The module manages the execution of queries to the simulations server.
"""
import time
import sys, traceback, os
from django.utils import timezone

import shutil, urllib

try:
    from urllib.parse import urlencode
    from urllib.request import Request, urlopen
    url_lib = urllib.request
except ImportError:
    from urllib2 import Request, urlopen
    from urllib import urlencode
    url_lib = urllib2

from .task import task as parent
from .task import task_exception as err

from avi.log import logger

from avi.core.risea import risea
from avi.core.interface.interface_manager import interface_manager
from avi.core.interface.name_solvers import simbad, ned
from avi.utils.coordinates_manager import coordinates_manager
from avi.utils.data.file_manager import file_manager
from avi.utils.data.json_manager import json_manager
from avi.warehouse import wh_global_config as wh

class sim_query_task(parent):
    """@class sim_query_task
    The sim_query_task class manages the execution of queries to the simulations 
    server.

    It implementes the task interface and inherits the task_data attribute.

    @see task @link avi.task.task.task
    @see task_data @link avi.task.task.task_data
    """
    def output(self):
        """Deprecated"""
        pass

    def total_mass_2_str(num):
        pass
    def virial_ratio_2_str(num):
        pass
    def half_mass_radius_2_str(num):
        pass
    def fractal_dimension_2_str(num):
        pass
    def segregation_degree_2_str(num):
        pass
    def binary_fraction(num):
        pass
    def total_mass_2_str_name(num):
        pass
    def half_mass_radius_2_str_name(num):
        pass
    def virial_ratio_2_str_name(num):
        pass

    def download_file(file_name):
        pass

    def parse_url(url):
        #if item:
        #   download_file(item)
        #else:
        #    parse_url(item)
        pass

    def run(self):
        """Runs the query to the simulations server.

        Args:
        self: The object pointer.

        Raises:
        task_exception: avi.task.task.task_exception
        """
        base_url = "http://sims.starformmapper.es/files/"
        sub_folder = "pure_nbody_sims/"
        tm = "Total_Mass_"+int(self.data['total_mass'])+"Msun/"
        vr = "Virial_equilibrium_Q0p"+int(self.data['virial_ratio']*10)+"/"
        hmr = "Rh01/"
        fd = "D30"
        sd = "S00"
        bf = "bin00"
        tm_name = "M103"
        hmr_name = "r01"
        vr_name = "Q05/"

        print(urlopen(base_url+pure_nbody_sims+"Total_Mass_1000Msun/Virial_equilibrium_Q0p5/Rh01/D20S00bin00M103r01Q05"))
        return

        try:
            response = urlopen(base_url+pure_nbody_sims+"Total_Mass_1000Msun/Virial_equilibrium_Q0p5/Rh01/D20S00bin00M103r01Q05/D20S00bin00M103r01Q05.NBODY")
        except Excetion as err:
            raise err('Cannot download the file')
        file_name = "/data/output/"+"test.tgz"
        fp = open(file_name, 'wb')
        shutil.copyfileobj(response, fp)
        fp.close()
        pass
                
