
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
