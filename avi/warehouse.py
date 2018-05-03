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
# Module for the risea's warehouses

from avi.log import logger

class wh_global_config:

    class __wh_global_config:

        CONTAINER_NAME = 'deavi'
        #CONTAINER_NAME = 'gavip'
        VERSION = '0.0.1'
        
        production = False

        RESOURCES_PATH = "/data/output/"
        OUTPUT_PATH = "/data/output/"
        SOURCES_PATH = "/data/output/"
        GAIA_PATH = "/data/output/"
        HSA_PATH = "/data/output/"
        RESULTS_PATH = "/data/output/"
        TMP_PATH = "/data/output/"
        ALGORITHM_PATH = "avi/algorithms/"

        INPUT_PATH = "/data/input/"
        UPLOADED_ALGORITHM_PATH = "/data/input/"
        TMP_ALGORITHM_PATH = "/data/input/"
        
        
        SOURCES_FMT = "source.dat"
        RESULTS_FMT = "result.dat"

        ALGORITHMS_LOADED = False
        
        AVI_URL = "/"#"/avis/deavi_0_0_1/"
        AVI_URL_NAME = "deavi_0_0_1"
        PORTAL_URL = ""

        log = None
        str_log_header = 'wh_global_config'
        
        def load(self, cfg = None):
            if not cfg:
                self.log.info('cfg missing, loading default configuration...')
                return
            
            import os
            
            self.log.info('loading cfg...')
            self.CONTAINER_NAME = cfg['container']
            self.VERSION = cfg['version']
            #self.RESOURCES_PATH = cfg['resources_path']
            self.SOURCES_PATH = os.path.join(self.OUTPUT_PATH, 
                                             cfg["sources_path"])
            self.GAIA_PATH = os.path.join(self.SOURCES_PATH, cfg["gaia_path"])
            self.HSA_PATH = os.path.join(self.SOURCES_PATH, cfg["hsa_path"])
            self.RESULTS_PATH = os.path.join(self.OUTPUT_PATH, 
                                             cfg["results_path"])
            self.TMP_PATH = os.path.join(self.OUTPUT_PATH, cfg["tmp_path"])

            self.ALGORITHM_PATH = os.path.join( \
                os.path.dirname(os.path.abspath(__file__)), 'algorithms')

            self.UPLOADED_ALGORITHM_PATH = os.path.join(self.OUTPUT_PATH, 
                                                   cfg["uploaded_alg_path"])
            self.TMP_ALGORITHM_PATH = os.path.join(self.OUTPUT_PATH, 
                                                   cfg["tmp_alg_path"]) 
            
            self.SOURCES_FMT = cfg["sources_fmt"]
            self.RESULTS_FMT = cfg["results_fmt"]
            
            self.log.debug(self.OUTPUT_PATH)
            self.log.debug(self.SOURCES_PATH)
            self.log.debug(self.GAIA_PATH)
            self.log.debug(self.HSA_PATH)
            self.log.debug(self.RESULTS_PATH)
            self.log.debug(self.SOURCES_FMT)
            self.log.debug(self.RESULTS_FMT)
            
        def __init__(self):
            self.log = logger().get_log(self.str_log_header)
            try:
                from django.conf import settings
                self.log.debug("output path: %s", settings.OUTPUT_PATH)
                self.log.debug("media path: %s", settings.MEDIA_URL)
                self.log.debug("static path: %s", settings.STATIC_URL)
                self.log.debug("media root: %s", settings.MEDIA_ROOT)
                # TODO: ? set media and static paths?
                self.OUTPUT_PATH = settings.OUTPUT_PATH
                self.INPUT_PATH = settings.INPUT_PATH
                
                if settings.AVI_URL_NAME:
                    self.AVI_URL_NAME = settings.AVI_URL_NAME
                if settings.PORTAL_URL:
                    self.PORTAL_URL = settings.PORTAL_URL
                if settings.AVI_ROOT_URL:
                    self.AVI_URL = settings.AVI_ROOT_URL
            #except ImportError:
            except Exception:
                pass
            self.RESOURCES_PATH = self.OUTPUT_PATH

        #
        #
        #
    def __init__(self):
        if not wh_global_config.instance:
            wh_global_config.instance = wh_global_config.__wh_global_config()

    def get(self):
        return wh_global_config.instance

    instance = None

class wh_names:

    class __wh_names:

        # Job names
        JOB_GAIA_QUERY = "gaia_query"
        JOB_HSA_QUERY = "herschel_query"
        JOB_GET_QUERIES_STATUS = "get_queries_status"
        JOB_GET_PIPELINE_STATUS = "get_pipeline_status"
        JOB_GET_RESOURCES = "get_resources"
        JOB_GET_RESULTS = "get_results"
        JOB_GET_PLOT = "get_plot"
        JOB_GET_RESULT = "get_result"
        JOB_ABORT = "abort"
        JOB_DELETE = "delete"
        JOB_CHANGE_PAGE = "change_page"
        JOB_SORT_BY = "sort_by"
        JOB_GET_FILES = "get_files"
        
        JOB_GET_ALGORITHM = "get_algorithm"
        JOB_GET_ALGORITHM_INFO = "get_algorithm_info"
        JOB_GET_ALGORITHMS = "get_algorithms"

        JOB_ALGORITHM = "algorithm"

        def __init__(self):
            pass
        #
        #
        #
    def __init__(self):
        if not wh_names.instance:
            wh_names.instance=wh_names.__wh_names()
    def get(self):
        return wh_names.instance

    instance = None

class wh_common:

    class __wh_common:

        # Job status
        queries_started = 0

        def __init__(self):
            pass
        #
        #
        #
    def __init__(self):
        if not wh_common.instance:
            wh_common.instance=wh_common.__wh_common()
    def get(self):
        return wh_common.instance

    instance = None
    
class wh_frontend_config:

    class __wh_frontend_config:
        
        CURRENT_PATH = None
        HOME_PATH = None

        NUM_ARCHIVES = 2

        MAX_PAGES = 5
        MAX_ALG_PER_PAGE = 5
        MAX_EXEC_PER_PAGE = 5
        MAX_QUERY_PER_PAGE = 5
        MAX_RESOURCES_PER_PAGE = 5
        MAX_RESULTS_PER_PAGE = 5
        
        CURRENT_ALG_PAGE = 1
        CURRENT_EXEC_PAGE = 1
        CURRENT_QUERY_PAGE = 1
        CURRENT_RESOURCES_PAGE = 1
        CURRENT_RESULTS_PAGE = 1

        # SORTING BY name date id status size
        SORTING_ALG_BY = "name"
        SORTING_EXEC_BY = "-date"
        SORTING_QUERY_BY = "date"
        SORTING_RESOURCES_BY = "name"
        SORTING_RESULTS_BY = "name"

        log = None
        str_log_header = 'wh_frontend_config'

        def __init__(self):
            self.log = logger().get_log(self.str_log_header)

        def load(self, cfg = None):
            if not cfg:
                self.log.info('cfg missing, loading default configuration...')
                return
            
            self.log.info('loading cfg...')
            self.MAX_ALG_PER_PAGE = cfg['max_alg_per_page']
            self.MAX_EXEC_PER_PAGE = cfg['max_exec_per_page']
        
        #
        #
        #
    def __init__(self):
        if not wh_frontend_config.instance:
            wh_frontend_config.instance=wh_frontend_config.__wh_frontend_config()
    def get(self):
        return wh_frontend_config.instance

    instance = None
