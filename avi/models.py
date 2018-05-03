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
from django.db import models

# Create your models here.
# TODO: import this just while running in gavip
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
    alg_name = models.CharField(max_length=255)
    params = models.TextField()
    results = models.TextField()
    error_message = models.TextField()
    
    is_aborted = models.BooleanField(default=False)

    pipeline_task = "algorithm"
    
class gaia_query_model(parent):
    name_coord = models.BooleanField()
    name = models.CharField(max_length=255)
    input_file = models.CharField(max_length=255)
    ra = models.FloatField()
    dec = models.FloatField()
    shape = models.CharField(max_length=255)
    radius = models.FloatField()
    width = models.FloatField()#null=True)
    height = models.FloatField()#null=True)
    polygon = models.TextField()#null=True)
    table = models.CharField(max_length=255)
    params = models.TextField(max_length=255)
    file_name = models.CharField(max_length=255)
    adql = models.TextField()#max_length=255)

    archive = models.CharField(max_length=255, default='gaia')

    is_aborted = models.BooleanField(default=False)

    pipeline_task = "gaia_query"

class herschel_query_model(parent):
    name_coord = models.BooleanField()
    name = models.CharField(max_length=255)#,null=True)
    input_file = models.CharField(max_length=255)
    ra = models.FloatField()#null=True)
    dec = models.FloatField()#null=True)
    shape = models.CharField(max_length=255)
    radius = models.FloatField()#null=True)
    width = models.FloatField()#null=True)
    height = models.FloatField()#null=True)
    polygon = models.TextField()#null=True)
    positional_images = models.BooleanField()
    table = models.CharField(max_length=255)#,null=True)
    instrument = models.CharField(max_length=255)#,null=True)
    level = models.CharField(max_length=255)#,null=True)
    params = models.TextField(max_length=255)#,null=True)
    file_name = models.CharField(max_length=255)
    adql = models.TextField()#max_length=255)

    archive = models.CharField(max_length=255, default='hsa')

    is_aborted = models.BooleanField(default=False)

    pipeline_task = "herschel_query"

class resource_model(models.Model):
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    file_type = models.CharField(max_length=255)
    job_id = models.IntegerField()# Foreign key
    date = models.DateField()

class plot_model(models.Model):
    name = models.CharField(max_length=255)
    job_id = models.IntegerField()
    alg_name = models.CharField(max_length=255)
    script = models.TextField()#models.FileField()
    html = models.TextField()#models.FileField()

class results_model(models.Model):
    job_id = models.IntegerField()
    resources = models.ManyToManyField(resource_model)
    plots = models.ManyToManyField(plot_model)

class algorithm_info_model(models.Model):
    name = models.CharField(max_length=255)
    name_view = models.CharField(max_length=255)
    source_file = models.CharField(max_length=255)
    definition_file = models.CharField(max_length=255)
    # installed, temporal, uploaded
    algorithm_type = models.CharField(max_length=255)
