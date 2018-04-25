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
along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
"""
from avi.models import (resource_model, algorithm_model, gaia_query_model,
                        herschel_query_model, plot_model, results_model,
                        algorithm_info_model)

from rest_framework import serializers

class algorithm_info_serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = algorithm_info_model
        fields =('name','name_view',
                 'source_file','definition_file','algorithm_type')

class algorithm_serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = algorithm_model
        fields =('id','alg_name','params')

class gaia_query_serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = gaia_query_model
        fields =('id','name','ra','dec','table')

class hsa_query_serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = herschel_query_model
        fields =('id','name','ra','dec','name_coord',
                 'table','instrument','level')

class resource_serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = resource_model
        fields =('id','name','path','file_type','job_id','date')

class plot_serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = plot_model
        fields = ('id', 'name', 'job_id', 'alg_name', 'script', 'html')

class results_serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = results_model
        fields = ('id', 'job_id')#, 'resources', 'plots')
