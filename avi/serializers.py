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

@package avi.serializers

--------------------------------------------------------------------------------

This module provides serializers for the models using the Django REST framework 
serializers.

@see http://www.django-rest-framework.org/api-guide/serializers/#hyperlinkedmodelserializer
@see avi.models
"""
from avi.models import (resource_model, algorithm_model, gaia_query_model,
                        herschel_query_model, plot_model, results_model,
                        algorithm_info_model, algorithm_group_model)

from rest_framework import serializers

class algorithm_info_serializer(serializers.HyperlinkedModelSerializer):
    """@class algorithm_info_serializer
    Serializes the algorithm_info_model

    @see avi.models.algorithm_info_model
    """
    class Meta:
        """@class Meta
        Meta class
        """
        ## The model name
        model = algorithm_info_model
        ## The fields to serialize
        fields =('name','name_view',
                 'source_file','definition_file','algorithm_type', 'algorithm_group')

class algorithm_group_serializer(serializers.HyperlinkedModelSerializer):
    """@class algorithm_group_serializer
    Serializes the algorithm_group_model

    @see avi.models.algorithm_group_model
    """
    class Meta:
        """@class Meta
        Meta class
        """
        ## The model name
        model = algorithm_group_model
        ## The fields to serialize
        fields =('name','name_view',
                 'position','position')

class algorithm_serializer(serializers.HyperlinkedModelSerializer):
    """@class algorithm_serializer
    Serializes the algorithm_model

    @see avi.models.algorithm_model
    """
    class Meta:
        """@class Meta
        Meta class
        """
        ## The model name
        model = algorithm_model
        ## The fields to serialize
        fields =('id','alg_name','params')

class gaia_query_serializer(serializers.HyperlinkedModelSerializer):
    """@class gaia_query_serializer
    Serializes the gaia_query_model

    @see avi.models.gaia_query_model
    """
    class Meta:
        """@class Meta
        Meta class
        """
        ## The model name
        model = gaia_query_model
        ## The fields to serialize
        fields =('id','name','ra','dec','table')

class hsa_query_serializer(serializers.HyperlinkedModelSerializer):
    """@class hsa_query_serializer
    Serializes the herschel_query_model

    @see avi.models.herschel_query_model
    """
    class Meta:
        """@class Meta
        Meta class
        """
        ## The model name
        model = herschel_query_model
        fields =('id','name','ra','dec','name_coord',
                 'table','instrument','level')

class resource_serializer(serializers.HyperlinkedModelSerializer):
    """@class resource_serializer
    Serializes the resource_model

    @see avi.models.resource_model
    """
    class Meta:
        """@class Meta
        Meta class
        """
        ## The model name
        model = resource_model
        ## The fields to serialize
        fields =('id','name','path','file_type','job_id','date')

class plot_serializer(serializers.HyperlinkedModelSerializer):
    """@class plot_serializer
    Serializes the plot_model

    @see avi.models.plot_model
    """
    class Meta:
        """@class Meta
        Meta class
        """
        ## The model name
        model = plot_model
        ## The fields to serialize
        fields = ('id', 'name', 'job_id', 'alg_name', 'script', 'html')

class results_serializer(serializers.HyperlinkedModelSerializer):
    """@class results_serializer
    Serializes the results_model

    @see avi.models.results_model
    """
    class Meta:
        """@class Meta
        Meta class
        """
        ## The model name
        model = results_model
        ## The fields to serialize
        fields = ('id', 'job_id')#, 'resources', 'plots')
