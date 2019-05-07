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

@package avi.views_api

--------------------------------------------------------------------------------

This module provides the API views

@see http://www.django-rest-framework.org/api-guide/viewsets/
@see http://www.django-rest-framework.org/api-guide/views/
"""
import os
import mimetypes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
from wsgiref.util import FileWrapper


from avi.warehouse import wh_global_config as wh
from avi.models import (resource_model, algorithm_model, gaia_query_model,
                        herschel_query_model, plot_model, results_model,
                        algorithm_info_model)
from avi.serializers import (resource_serializer, algorithm_serializer,
                             gaia_query_serializer, hsa_query_serializer, 
                             plot_serializer, results_serializer,
                             algorithm_info_serializer)

class algorithms_info(viewsets.ModelViewSet):
    """@class algorithms_info
    This class provides a view for the algorithm_info_model

    @see avi.models.algorithm_info_model
    @see avi.serializers.algorithm_info_serializer
    """
    ## query to the model
    queryset = algorithm_info_model.objects.all()
    ## serializer class
    serializer_class = algorithm_info_serializer

class algorithms_list(viewsets.ModelViewSet):
    """@class algorithms_list
    This class provides a view for the algorithm_model

    @see avi.models.algorithm_model
    @see avi.serializers.algorithm_serializer
    """
    ## query to the model
    queryset = algorithm_model.objects.all()
    ## serializer class
    serializer_class = algorithm_serializer

class gaia_queries_list(viewsets.ModelViewSet):
    """@class gaia_queries_list
    This class provides a view for the gaia_query_model

    @see avi.models.gaia_query_model
    @see avi.serializers.gaia_query_serializer
    """
    ## query to the model
    queryset = gaia_query_model.objects.all()
    ## serializer class
    serializer_class = gaia_query_serializer

class hsa_queries_list(viewsets.ModelViewSet):
    """@class hsa_queries_list
    This class provides a view for the herschel_query_model

    @see avi.models.herschel_query_model
    @see avi.serializers.hsa_query_serializer
    """
    ## query to the model
    queryset = herschel_query_model.objects.all()
    ## serializer class
    serializer_class = hsa_query_serializer

class resources_list(viewsets.ModelViewSet):
    """@class resources_list
    This class provides a view for the resource_model

    @see avi.models.resource_model
    @see avi.serializers.resource_serializer
    """
    ## query to the model
    queryset = resource_model.objects.all()
    ## serializer class
    serializer_class = resource_serializer

class plot_list(viewsets.ModelViewSet):
    """@class plot_list
    This class provides a view for the plot_model

    @see avi.models.plot_model
    @see avi.serializers.plot_serializer
    """
    ## query to the model
    queryset = plot_model.objects.all()
    ## serializer class
    serializer_class = plot_serializer

class results_list(viewsets.ModelViewSet):
    """@class results_list
    This class provides a view for the results_model

    @see avi.models.results_model
    @see avi.serializers.results_serializer
    """
    ## query to the model
    queryset = results_model.objects.all()
    ## serializer class
    serializer_class = results_serializer

class samp_resource(APIView):
    """@class samp_resource
    This class provides a APIView to retrieve a resource and serve it in a SAMP 
    readable format
    """
    def get(self, request, resource_id):
        """Serves a resource in a SAMP readable format

        Args:
        self: The object pointer
        request: HttpRequest object
        resource_id: The id of the resource

        Returns:
        A HttpResponse with the resource
        """
        res = resource_model.objects.filter(pk=resource_id)
        if not res:
            return None
        full_name = os.path.join(res[0].path, res[0].name)
        file_data = open(full_name,'rb')
        file_type = 'application/xml'
        name, ext = os.path.splitext(res[0].name) 
        if ext == ".fits" or ext == ".tar":
            file_type = 'application/tar+gzip'
        response = HttpResponse(file_data, content_type=file_type)
        return response
        
class resource(APIView):
    """@class samp_resource
    This class provides a APIView to retrieve a resource and serve it
    """
    def get(self, request, resource_id):
        """Serves a resource

        Args:
        self: The object pointer
        request: HttpRequest object
        resource_id: The id of the resource

        Returns:
        A HttpResponse with the resource
        """
        #return JsonResponse({"votable":3, "ASD": 123})
        #vot_name = open('/data/output/100.241700_9.895000_0.100000_gaia_source.vot','rb')
        res = resource_model.objects.filter(pk=resource_id)
        if not res:
            return None
        full_name = os.path.join(res[0].path, res[0].name)
        file_data = open(full_name,'rb')
        file_type = 'application/xml'
        name, ext = os.path.splitext(res[0].name) 
        if ext == ".fits" or ext == ".tar":
            file_type ='application/x-tar'
        elif ext != ".xml" or ext != ".vot":
            file_type = mimetypes.guess_type(full_name)[0]

        size = os.path.getsize(full_name)

        if wh().get().production:
            response = HttpResponse()
            response['Content-Disposition'] = 'attachment; filename="%s"'%res[0].name
            response['X-Sendfile'] = full_name
            return response

        if size <= 20:
            response = HttpResponse(file_data, content_type=file_type)
            response['Content-Disposition'] = 'attachment; filename="%s"'%res[0].name
            response['Content-Length'] = os.path.getsize(full_name)
            return response

        chunk_size = 8192
        response = StreamingHttpResponse(FileWrapper(open(full_name, 'rb'), 
                                                     chunk_size),
                                         content_type=file_type)
        response['Content-Length'] = size
        response['Content-Disposition'] = 'attachment; filename="%s"'%res[0].name
        return response

class get_resource(APIView):
    """@class samp_resource
    This class provides a APIView to retrieve a resource and serve it
    """
    def get(self, request, resource_id):
        """Serves a resource

        Args:
        self: The object pointer
        request: HttpRequest object
        resource_id: The id of the resource

        Returns:
        A HttpResponse with the resource
        """
        res = resource_model.objects.filter(pk=resource_id)
        if not res:
            return None
        full_name = os.path.join(res[0].path, res[0].name)
        file_data = open(full_name, 'rb')
        file_type = 'application/text'
        name, ext = os.path.splitext(res[0].name) 
        if ext == ".vot" or ext == ".xml":
            file_type = 'application/xml'
            return HttpResponse(file_data, content_type=file_type)
        response = HttpResponse(file_data)#, content_type=file_type)
        #response['Content-Disposition'] = 'filename="%s"'%res[0].name
        return response
