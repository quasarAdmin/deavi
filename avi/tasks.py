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
try:
    # ############################################################################
    # ################################## AVI #####################################
    # ############################################################################
    #import os
    
    #from django.conf import settings
    
    #from pipeline.classes import (
    #    AviTask,
    #    AviParameter, AviLocalTarget,
    #)
    from pipeline.classes import AviTask as parent
    from pipeline.classes import AviParameter, AviLocalTarget

except ImportError:
    from pipeline.luigi_tasks import avi_task as parent
    from pipeline.luigi_tasks import parameter as AviParameter
    from pipeline.luigi_tasks import local_target as AviLocalTarget

import os

from avi.log import logger
from avi.task.algorithm_task import algorithm_task
from avi.task.gaia_query_task import gaia_query_task
from avi.task.herschel_query_task import herschel_query_task

class algorithm(parent):
    request = AviParameter()
    alg_name = AviParameter()
    params = AviParameter()
    results = AviParameter()
    error_message = AviParameter()

    def output(self):
        algorithm_task().output()
        return AviLocalTarget("/data/output/test.text")

    def run(self):
        t = algorithm_task()
        t.task_id = self.request.algorithm_model_model.pk
        t.task_data.data = self.params
        try:
            t.run()
        except Exception:
            raise Exception("some error")

class gaia_query(parent):
    request = AviParameter()
    name_coord = AviParameter()
    name = AviParameter()
    input_file = AviParameter()
    ra = AviParameter()
    dec = AviParameter()
    shape = AviParameter()
    radius = AviParameter()
    width = AviParameter()
    height = AviParameter()
    polygon = AviParameter()
    table = AviParameter()
    params = AviParameter()
    file_name = AviParameter()
    adql = AviParameter()
    
    def output(self):
        gaia_query_task().output()
        return AviLocalTarget("/data/output/test.txt")
        
    def run(self):
        t = gaia_query_task()
        t.task_id = self.request.gaia_query_model_model.pk
        data = {'name_coord':self.name_coord,
                'name':self.name,
                'input_file':self.input_file,
                'ra':self.ra,
                'dec':self.dec,
                'shape':self.shape,
                'radius':self.radius,
                'width':self.width,
                'height':self.height,
                'polygon':self.polygon,
                'table':self.table,
                'params':self.params,
                'output_file':self.file_name,
                'adql':self.adql}
        t.task_data.data = data
        t.run()
            
class herschel_query(parent):
    request = AviParameter()
    name_coord = AviParameter()
    name = AviParameter()
    input_file = AviParameter()
    ra = AviParameter()
    dec = AviParameter()
    shape = AviParameter()
    radius = AviParameter()
    width = AviParameter()
    height = AviParameter()
    polygon = AviParameter()
    positional_images = AviParameter()
    table = AviParameter()
    instrument = AviParameter()
    level = AviParameter()
    params = AviParameter()
    file_name = AviParameter()
    adql = AviParameter()
    
    def output(self):
        herschel_query_task().output()
        return AviLocalTarget("/data/output/test.txt")
    def run(self):
        log = logger().get_log('risea')
        log.info('deavi_task run...')
        t = herschel_query_task()
        t.task_id = self.request.herschel_query_model_model.pk
        data = {'name_coord':self.name_coord,
                'name':self.name,
                'input_file':self.input_file,
                'ra':self.ra,
                'dec':self.dec,
                'shape':self.shape,
                'radius':self.radius,
                'width':self.width,
                'height':self.height,
                'polygon':self.polygon,
                'positional_images':self.positional_images,
                'table':self.table,
                'instrument':self.instrument,
                'level':self.level,
                'params':self.params,
                'output_file':self.file_name,
                'adql':self.adql}
        t.task_data.data = data
        t.run()
            
            
#except ImportError:
    # ############################################################################
    # ################################# DEAVI ####################################
    # ############################################################################
    #pass
