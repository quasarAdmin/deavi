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

@package avi.serializers

--------------------------------------------------------------------------------

This module provides serializers for the models using the Django REST framework 
serializers.

@see http://www.django-rest-framework.org/api-guide/serializers/#hyperlinkedmodelserializer
@see avi.models
"""
from avi.models import (resource_model, algorithm_model, gaia_query_model,
                        herschel_query_model, plot_model, results_model,
                        algorithm_info_model)

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
                 'source_file','definition_file','algorithm_type')

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
