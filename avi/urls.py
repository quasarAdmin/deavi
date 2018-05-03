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
from django.conf.urls import url, include, patterns
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers

from . import views
from . import views_api

# initial configuration
# TODO
from avi.core.risea import risea
risea().get()

# urlpatterns configuration

router = routers.DefaultRouter()
router.register(r'resources', views_api.resources_list)
router.register(r'gaia_queries', views_api.gaia_queries_list)
router.register(r'hsa_queries', views_api.hsa_queries_list)
router.register(r'list_algorithms', views_api.algorithms_list)
router.register(r'plots', views_api.plot_list)
router.register(r'results', views_api.results_list)
router.register(r'alg_info', views_api.algorithms_info)

api_urls = [
    #url(r'^', include(router.urls)),
    url(r'^resource/(?P<resource_id>[0-9]+)/$', 
        views_api.resource.as_view(),name='api-resource'),
    url(r'^samp_resource/(?P<resource_id>[0-9]+)/$', 
        views_api.resource.as_view(),name='api-samp-resource'),
    url(r'^res/(?P<resource_id>[0-9]+)/$',
        views_api.get_resource.as_view(),name='api-get_resource'),
]

api_urls = format_suffix_patterns(api_urls)

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^', include(router.urls)),
                       url(r'^api/', include(api_urls, namespace='api')),
                       url(r'^(?P<fib>[0-9]+)$', views.create, name='create'),
                       url(r'^algorithms', views.pipeline_v2, name='pipe'),
                       url(r'^pipeline', views.pipeline, name='pipeline'),
                       url(r'^status', views.status, name='status'),
                       url(r'^ajax/get_results', 
                           views.get_results, name='get_results'),
                       url(r'^ajax/get_alg_info',
                           views.get_alg_info, name='get_alg_info'),
                       url(r'^ajax/get_plot', 
                           views.get_plot, name='get_plot'),
                       url(r'^queries/gaia', 
                           views.query_gaia, name='query_gaia'),
                       url(r'^queries/herschel', views.query_herschel, 
                           name='query_herschel'),
                       url(r'^queries/status', views.query_status, 
                           name='query_status'),
                       url(r'^queries/saved', views.query_saved, 
                           name='query_saved'),
                       url(r'^resources/filemanager', 
                           views.resources_filemanager, 
                           name='resources_filemanager'),
                       url(r'^help/about', views.help_about, name='help_about'),
                       url(r'^debug', views.debug, name='debug'),
                       url(r'^vr', views.vr, name='vr'),
                       url(r'^algorithm/(?P<alg_id>[-A-Za-z0-9_]+)/$', views.algorithm, name='algorithm'),
)
