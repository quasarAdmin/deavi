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

@package avi.tasks

--------------------------------------------------------------------------------

This module is an interface to the asynchronous tasks.

This modules provides interfaces to the asynchronous tasks.

This tasks are implemented using luigi

@see https://luigi.readthedocs.io/en/stable/
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
from avi.task.sim_query_task import sim_query_task
from avi.task.task import task_exception

class algorithm(parent):
    """@class algorithm
    The algorithm class is the interface to the algorithm_task
    
    See:
    algorithm_task: avi.task.algorithm_task.algorithm_task
    """
    ## Information of the task request
    request = AviParameter()
    ## The name of the algorithm
    alg_name = AviParameter()
    ## The input parameters
    params = AviParameter()
    ## Deprecated
    results = AviParameter()
    ## An error message
    error_message = AviParameter()

    def output(self):
        """Deprecated"""
        algorithm_task().output()
        return AviLocalTarget("/data/output/test.text")

    def run(self):
        """Runs the task
        Args:
        self: The object pointer

        Raises:
        Exception
        """
        t = algorithm_task()
        t.task_id = self.request.algorithm_model_model.pk
        t.task_data.data = self.params
        try:
            t.run()
        except task_exception as err:
            self.error_message = err.message
            raise Exception(err.message)
        except Exception as unknown:
            self.error_message = unknown.message
            raise Exception("Unknown error")

class gaia_query(parent):
    """@class gaia_query
    The gaia_query class is the interface to the gaia_query_task

    See:
    gaia_query_task: avi.task.gaia_query_task.gaia_query_task
    """
    ## Information of the task request
    request = AviParameter()
    ## Has the query to be done by coordinates or name?
    name_coord = AviParameter()
    ## Name of the object to be queried
    name = AviParameter()
    ## Input file containing multiple queries information
    input_file = AviParameter()
    ## ra
    ra = AviParameter()
    ## dec
    dec = AviParameter()
    ## shape of the query
    shape = AviParameter()
    ## radius of the query
    radius = AviParameter()
    ## width of the query
    width = AviParameter()
    ## height of the query
    height = AviParameter()
    ## array containing the vertexes of a polygon
    polygon = AviParameter()
    ## table of the archive to be queried
    table = AviParameter()
    ## special parameters
    params = AviParameter()
    ## output file name
    file_name = AviParameter()
    ## an ADQL query
    adql = AviParameter()
    
    def output(self):
        """Deprecated"""
        gaia_query_task().output()
        return AviLocalTarget("/data/output/test.txt")
        
    def run(self):
        """Runs the task
        Args:
        self: The object pointer

        Raises:
        Exception
        """
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
    """@class herschel_query
    The herschel_query class is the interface to the herschel_query_task
    
    See:
    herschel_query_task: avi.task.herschel_query_task.herschel_query_task
    """
    ## Information of the task request
    request = AviParameter()
    ## Has the query to be done by coordinates or name?
    name_coord = AviParameter()
    ## Name of the object to be queried
    name = AviParameter()
    ## Input file containing multiple queries information
    input_file = AviParameter()
    ## ra
    ra = AviParameter()
    ## dec
    dec = AviParameter()
    ## Shape of the query
    shape = AviParameter()
    ## Radius of the query
    radius = AviParameter()
    ## Width of the query
    width = AviParameter()
    ## Height of the query
    height = AviParameter()
    ## Array containing the vertexes of a polygon
    polygon = AviParameter()
    ## Is it a positional source catalog query or not?
    positional_images = AviParameter()
    ## Table of the archive to be queried
    table = AviParameter()
    ## Herschel instrument
    instrument = AviParameter()
    ## Processing level of the images
    level = AviParameter()
    ## Special parameters
    params = AviParameter()
    ## Output file name
    file_name = AviParameter()
    ## An ADQL query
    adql = AviParameter()
    
    def output(self):
        """Deprecated"""
        herschel_query_task().output()
        return AviLocalTarget("/data/output/test.txt")
    def run(self):
        """Runs the task
        Args:
        self: The object pointer

        Raises:
        Exception
        """
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

class sim_query(parent):
    """@class herschel_query
    The herschel_query class is the interface to the herschel_query_task
    
    See:
    herschel_query_task: avi.task.herschel_query_task.herschel_query_task
    """
    ## Information of the task request
    request = AviParameter()
    ## name of the object to be queried
    name = AviParameter()
    ## Total mass (solar-mass)
    total_mass = AviParameter()
    ## virial ratio
    virial_ratio = AviParameter()
    ## Half-mass radius (pc) 0.1, 0.5, 1.0
    half_mass_radius = AviParameter()
    ## Fractal dimension
    fractal_dimension = AviParameter()
    ## Degree of mass-segregation
    mass_segregation_degree = AviParameter()
    ## Binary fraction (%)
    binary_fraction = AviParameter()
    
    def output(self):
        """Deprecated"""
        sim_query_task().output()
        return AviLocalTarget("/data/output/test.txt")
    def run(self):
        """Runs the task
        Args:
        self: The object pointer

        Raises:
        Exception
        """
        log = logger().get_log('risea')
        log.info('deavi_task run...')
        t = sim_query_task()
        t.task_id = self.request.sim_query_model_model.pk
        data = {'name': t.task_id,
                'total_mass':self.total_mass,
                'virial_ratio':self.virial_ratio,
                'half_mass_radius':self.half_mass_radius,
                'fractal_dimension':self.fractal_dimension,
                'mass_segregation_degree':self.mass_segregation_degree,
                'binary_fraction':self.binary_fraction}
        t.task_data.data = data
        t.run()            
            
#except ImportError:
    # ############################################################################
    # ################################# DEAVI ####################################
    # ############################################################################
    #pass
