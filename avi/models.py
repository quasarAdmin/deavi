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

@package avi.models

--------------------------------------------------------------------------------

This module provides the models for the application.

@see https://docs.djangoproject.com/en/2.0/topics/db/models/
"""
from django.db import models

# Create your models here.
try:
    # ############################################################################
    # ################################## AVI #####################################
    # ############################################################################

    from pipeline.models import AviJob as parent

    # Model for querying the Gaia archive
    #class gaia_query_model(AviJob):
    #    ra = models.FloatField()
    #    dec = models.FloatField()
    #    radius = models.FloatField()
    #    table = models.CharField(max_length=255)
    #    params = models.TextField(max_length=255)
    
    #    pipeline_task = "gaia_query"
    
    # Tutorial for class
    #class TutorialModel(AviJob):
    #    fib_num = models.IntegerField()
    #    pipeline_task = "CalcFib"

except ImportError:

    # ############################################################################
    # ################################# DEAVI ####################################
    # ############################################################################
    from pipeline.models import avi_job as parent

class algorithm_model(parent):
    """@class algorithm_model
    The algorithm_model defines the data base model for the algorithm execution
    
    The algorithm_model defines the data base model for the algorithm execution.
    
    It inherits from the AviJob class or the avi_job class, depending on which 
    platform is the application running on.
    """
    ## The name of the algorithm
    alg_name = models.CharField(max_length=255)
    ## The input parameter of the algorithm
    params = models.TextField()
    ## Deprecated
    results = models.TextField()
    ## Error message
    error_message = models.TextField()
    ## Is aborted?
    is_aborted = models.BooleanField(default=False)
    ## pipeline name used to get the pipeline task and start it
    pipeline_task = "algorithm"
    
class gaia_query_model(parent):
    """@class gaia_query_model
    The gaia_query_model defines the data base model for the gaia query 
    execution
    
    The gaia_query_model defines the data base model for the gaia query 
    execution

    It inherits from the AviJob class or the avi_job class, depending on which 
    platform is the application running on.
    """
    ## has the query to be done by coordiantes, name, input file or adql?
    name_coord = models.CharField(max_length=255)
    ## name of the object to be queried
    name = models.CharField(max_length=255)
    ## input file containing multiple queries information
    input_file = models.CharField(max_length=255)
    ## ra
    ra = models.FloatField()
    ## dec
    dec = models.FloatField()
    ## shape of the query
    shape = models.CharField(max_length=255)
    ## radius of the query
    radius = models.FloatField()
    ## width of the query
    width = models.FloatField()#null=True)
    ## height of the query
    height = models.FloatField()#null=True)
    ## array containing the vertexes of a polygon
    polygon = models.TextField()#null=True)
    ## table of the archive to be queried
    table = models.CharField(max_length=255)
    ## special parameters
    params = models.TextField(max_length=255)
    ## output file name
    file_name = models.CharField(max_length=255)
    ## an ADQL query
    adql = models.TextField()#max_length=255)
    
    ## deprecated
    archive = models.CharField(max_length=255, default='gaia')
    ## Is aborted?
    is_aborted = models.BooleanField(default=False)
    ## pipeline name used to get the pipeline task and start it
    pipeline_task = "gaia_query"

    def __lt__(self, other):
        return self.pk < other.pk

class herschel_query_model(parent):
    """@class herschel_query_model
    The herschel_query_model defines the data base model for the herschel query 
    execution
    
    The herschel_query_model defines the data base model for the herschel query 
    execution

    It inherits from the AviJob class or the avi_job class, depending on which 
    platform is the application running on.
    """
    ## has the query to be done by coordiantes, name, input file or adql?
    name_coord = models.CharField(max_length=255)
    ## name of the object to be queried
    name = models.CharField(max_length=255)#,null=True)
    ## input file containing multiple queries information
    input_file = models.CharField(max_length=255)
    ## ra
    ra = models.FloatField()#null=True)
    ## dec
    dec = models.FloatField()#null=True)
    ## shape of the query
    shape = models.CharField(max_length=255)
    ## radius of the query
    radius = models.FloatField()#null=True)
    ## width of the query
    width = models.FloatField()#null=True)
    ## height of the query
    height = models.FloatField()#null=True)
    ## array containing the vertexes of a polygon
    polygon = models.TextField()#null=True)
    ## is it a positional source catalog query or images?
    positional_images = models.BooleanField()
    ## table of the archive to be queried
    table = models.CharField(max_length=255)#,null=True)
    ## herschel instrument
    instrument = models.CharField(max_length=255)#,null=True)
    ## processing level
    level = models.CharField(max_length=255)#,null=True)
    ## special params
    params = models.TextField(max_length=255)#,null=True)
    ## output file name
    file_name = models.CharField(max_length=255)
    ## an ADQL query
    adql = models.TextField()#max_length=255)
    ## deprecated
    archive = models.CharField(max_length=255, default='hsa')
    ## Is aborted?
    is_aborted = models.BooleanField(default=False)
    ## pipeline name used to get the pipeline task and start it
    pipeline_task = "herschel_query"
    
    def __lt__(self, other):
        return self.pk < other.pk

class sim_query_model(parent):
    """@class sim_query_model
    The sim_query_model defines the data base model for the simulations query 
    execution
    
    The sim_query_model defines the data base model for the simulations query 
    execution

    It inherits from the AviJob class or the avi_job class, depending on which 
    platform is the application running on.
    """
    ## Total mass (solar-mass)
    total_mass = models.FloatField()
    ## virial ratio
    virial_ratio = models.FloatField()
    ## Half-mass radius (pc) 0.1, 0.5, 1.0
    half_mass_radius = models.FloatField()
    ## Fractal dimension
    fractal_dimension = models.FloatField()
    ## Degree of mass-segregation
    mass_segregation_degree = models.FloatField()
    ## Binary fraction (%)
    binary_fraction = models.FloatField()
    ## Is aborted?
    is_aborted = models.BooleanField(default=False)
    ## pipeline name used to get the pipeline task and start it
    pipeline_task = "sim_query"
    
    def __lt__(self, other):
        return self.pk < other.pk

class resource_model(models.Model):
    """@class resource_model
    The resource_model defines the data base model for the resources.
    
    The resource_model defines the data base model for the resources. It will 
    store the information of those resources.
    """
    ## name of the resource
    sort_name = models.CharField(max_length=255)
    ## full name of the resource
    name = models.CharField(max_length=255)
    ## path of the resource
    path = models.CharField(max_length=255)
    ## type of retource
    file_type = models.CharField(max_length=255)
    ## id of the job that created this resource
    job_id = models.IntegerField()# Foreign key
    ## date of the resource creation
    date = models.DateField()

class plot_model(models.Model):
    """@class plot_model
    The plot_model defines the data base model for the plots.

    The plot_model define the data base model for the plots. It will store 
    the information of those plots.
    
    It stores the bokeh plots information in a html/js form.

    @see https://bokeh.pydata.org/en/latest/
    """
    ## name of the plot
    name = models.CharField(max_length=255)
    ## if of the job that created this plot
    job_id = models.IntegerField()
    ## the name of the algorithm that created this plot
    alg_name = models.CharField(max_length=255)
    ## the javascript script of the plot
    script = models.TextField()#models.FileField()
    ## the html of the plot
    html = models.TextField()#models.FileField()

class results_model(models.Model):
    """@class result_model
    The result_model defines the data base model for the results.
    
    The result_model defines the data base model for the results of a certain 
    job. It will store a list of resources and plots created by a ceratin job.
    """
    ## the id of the job that created those results
    job_id = models.IntegerField()
    ## the list of resources
    resources = models.ManyToManyField(resource_model)
    ## the list of plots
    plots = models.ManyToManyField(plot_model)

class algorithm_info_model(models.Model):
    """@class algorithm_info_model
    The algorithm_info_model defines the data base model for the algorithms 
    information
    
    The algorithm_info_model defines the data base model for the algorithms 
    information. It will store all the needed information of an algorithm to be 
    defined.
    """
    ## name of the algorithm
    name = models.CharField(max_length=255)
    ## name that must be shown in the user interface
    name_view = models.CharField(max_length=255)
    ## path to the source file of the algorithm
    source_file = models.CharField(max_length=255)
    ## path to the definition file of the algorithm
    definition_file = models.CharField(max_length=255)
    ## the algorithm type -> installed, temporal, uploaded
    algorithm_type = models.CharField(max_length=255)

    def __lt__(self, other):
        return self.pk < other.pk
