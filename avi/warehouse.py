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

@package avi.warehouse

--------------------------------------------------------------------------------

This module provides the warehouses for the application
"""
# Module for the risea's warehouses

from avi.log import logger

class wh_global_config:
    """@class wh_global_config
    This class provides the global configuration constants

    It uses the singleton pattern to ensure there is only one instance of the 
    warehouse and also to provide accessibility in any section of the code
    """
    class __wh_global_config:
        """Private class to feature the singleton pattern"""
        ## The name of the container
        CONTAINER_NAME = 'deavi'
        #CONTAINER_NAME = 'gavip'
        ## The applicatio version
        VERSION = '0.0.1'
        ## Is it running in production?
        production = False
        ## Path to the resources
        RESOURCES_PATH = "/data/output/"
        ## Output path
        OUTPUT_PATH = "/data/output/"
        ## Sources path
        SOURCES_PATH = "/data/output/"
        ## Gaia path
        GAIA_PATH = "/data/output/"
        ## Herschel path
        HSA_PATH = "/data/output/"
        ## Simulations path
        SIM_PATH = "/data/output/"
        ## Results path
        RESULTS_PATH = "/data/output/"
        ## User path
        USER_PATH = "/data/output/"
        ## Temporal files path
        TMP_PATH = "/data/output/"
        ## Algorithm path
        ALGORITHM_PATH = "avi/algorithms/"
        ## Input path
        INPUT_PATH = "/data/input/"
        ## Uploaded algorithm path
        UPLOADED_ALGORITHM_PATH = "/data/input/"
        ## Temporal algorithm path
        TMP_ALGORITHM_PATH = "/data/input/"
        
        ## Sources format
        SOURCES_FMT = "source.dat"
        ## Results format
        RESULTS_FMT = "result.dat"
        ## User data format
        USER_FMT = "user.dat"
        ## Are the algorithms loaded?
        ALGORITHMS_LOADED = False
        ## AVI URL
        AVI_URL = "/"#"/avis/deavi_0_0_1/"
        ## AVI URL NAME
        AVI_URL_NAME = "deavi_0_0_1"
        ## Portal URL
        PORTAL_URL = ""
        ## The log
        log = None
        ## The log header
        str_log_header = 'wh_global_config'
        
        def load(self, cfg = None):
            """Loads the warehouse

            Loads the warehouse with the given configuration

            Args:
            self: The object pointer
            cfg: The configuration to be loaded
            """
            if not cfg:
                self.log.info('cfg missing, loading default configuration...')
                return
            
            import os
            
            self.log.info('loading cfg...')
            self.CONTAINER_NAME = cfg['container']
            self.VERSION = cfg['version']
            self.production = cfg['production'] == 'True'
            #self.RESOURCES_PATH = cfg['resources_path']
            self.SOURCES_PATH = os.path.join(self.OUTPUT_PATH, 
                                             cfg["sources_path"])
            self.GAIA_PATH = os.path.join(self.SOURCES_PATH, cfg["gaia_path"])
            self.HSA_PATH = os.path.join(self.SOURCES_PATH, cfg["hsa_path"])
            self.SIM_PATH = os.path.join(self.SOURCES_PATH, cfg["sim_path"])
            self.RESULTS_PATH = os.path.join(self.OUTPUT_PATH, 
                                             cfg["results_path"])
            self.USER_PATH = os.path.join(self.OUTPUT_PATH,
                                          cfg["user_path"])
            self.TMP_PATH = os.path.join(self.OUTPUT_PATH, cfg["tmp_path"])

            self.ALGORITHM_PATH = os.path.join( \
                os.path.dirname(os.path.abspath(__file__)), 'algorithms')

            self.UPLOADED_ALGORITHM_PATH = os.path.join(self.OUTPUT_PATH, 
                                                   cfg["uploaded_alg_path"])
            self.TMP_ALGORITHM_PATH = os.path.join(self.OUTPUT_PATH, 
                                                   cfg["tmp_alg_path"]) 
            
            self.SOURCES_FMT = cfg["sources_fmt"]
            self.RESULTS_FMT = cfg["results_fmt"]
            self.USER_FMT = cfg["user_fmt"]
            
            self.log.debug(self.OUTPUT_PATH)
            self.log.debug(self.SOURCES_PATH)
            self.log.debug(self.GAIA_PATH)
            self.log.debug(self.HSA_PATH)
            self.log.debug(self.RESULTS_PATH)
            self.log.debug(self.SOURCES_FMT)
            self.log.debug(self.RESULTS_FMT)
            
        def __init__(self):
            """Constructor
            Initializes the log and sets some the initial values of the 
            warehouse
            
            Args:
            self: The object pointer
            """
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
            #self.PORTAL_URL = "https://net.quasarsr.com/deavi"
            #self.AVI_URL = "https://net.quasarsr.com/deavi/"

        #
        #
        #
    def __init__(self):
        """Constructor
        
        The constructor will create a new __wh_global_config object in case 
        there is none initialized, otherwise it will not do anything
        
        Args:
        self: The object pointer
        """
        if not wh_global_config.instance:
            wh_global_config.instance = wh_global_config.__wh_global_config()

    def get(self):
        """Returns the warehouse intance
        
        Args:
        self: The object pointer
        
        Returns:
        The instance of the warehouse
        """
        return wh_global_config.instance

    instance = None

class wh_names:
    """@class wh_names
    This class provides the name constants of the application

    It uses the singleton pattern to ensure there is only one instance of the 
    warehouse and algo to provide accessibility in any section of the code
    """
    class __wh_names:
        """Private class to feature the singleton pattern"""
        # Job names
        ## Gaia query job name
        JOB_GAIA_QUERY = "gaia_query"
        ## Herschel query job name
        JOB_HSA_QUERY = "herschel_query"
        ## Simulation query job name
        JOB_SIM_QUERY = "sim_query"
        ## Get queries status job name
        JOB_GET_QUERIES_STATUS = "get_queries_status"
        ## Get pipeline status job name
        JOB_GET_PIPELINE_STATUS = "get_pipeline_status"
        ## Get resources job name
        JOB_GET_RESOURCES = "get_resources"
        ## Save SAMP data job name
        JOB_SAVE_SAMP_DATA = "save_samp_data"
        ## Save User data job name
        JOB_SAVE_USER_DATA = "save_user_data"
        ## Get results job name
        JOB_GET_RESULTS = "get_results"
        ## Get plot job name
        JOB_GET_PLOT = "get_plot"
        ## Get result job name
        JOB_GET_RESULT = "get_result"
        ## Get query info job name
        JOB_GET_QUERY_INFO = "get_query_info"
        ## Get query status job name
        JOB_GET_QUERY_STATUS = "get_query_status"
        ## Abort job name
        JOB_ABORT = "abort"
        ## Delete job name
        JOB_DELETE = "delete"
        ## Relaunch job name
        JOB_RELAUNCH_ALGORITHM = "relaunch_algorithm"
        ## Launch in query job name
        JOB_LAUNCH = "launch"
        ## Change page job name
        JOB_CHANGE_PAGE = "change_page"
        ## Sort by job name
        JOB_SORT_BY = "sort_by"
        ## Get files job name
        JOB_GET_FILES = "get_files"
        ## Delete files
        JOB_DELETE_FILE = "delete_file"
        ## Get algorithm job name
        JOB_GET_ALGORITHM = "get_algorithm"
        ## Get algorithm info job name
        JOB_GET_ALGORITHM_INFO = "get_algorithm_info"
        ## Get algorithms job name
        JOB_GET_ALGORITHMS = "get_algorithms"
        ## Algorithm job name
        JOB_ALGORITHM = "algorithm"

        def __init__(self):
            """Constructor
            
            Args:
            self: The object pointer
            """
            pass
        #
        #
        #
    def __init__(self):
        """Constructor
        
        The constructor will create a new __wh_names object in case 
        there is none initialized, otherwise it will not do anything
        
        Args:
        self: The object pointer
        """
        if not wh_names.instance:
            wh_names.instance=wh_names.__wh_names()
    def get(self):
        """ Returns the warehouse intance
        
        Args:
        self: The object pointer
        
        Returns:
        The instance of the warehouse
        """
        return wh_names.instance

    instance = None

class wh_common:
    """@class wh_common
    Deprecated

    It uses the singleton pattern to ensure there is only one instance of the 
    warehouse and algo to provide accessibility in any section of the code
    """
    class __wh_common:
        """Private class to feature the singleton pattern"""
        # Job status
        queries_started = 0

        def __init__(self):
            """Constructor
            
            Args:
            self: The object pointer
            """
            pass
        #
        #
        #
    def __init__(self):
        """Constructor
        
        The constructor will create a new __wh_common object in case 
        there is none initialized, otherwise it will not do anything
        
        Args:
        self: The object pointer
        """
        if not wh_common.instance:
            wh_common.instance=wh_common.__wh_common()
    def get(self):
        """ Returns the warehouse intance
        
        Args:
        self: The object pointer
        
        Returns:
        The instance of the warehouse
        """
        return wh_common.instance

    instance = None
    
class wh_frontend_config:
    """@class wh_frontend_config
    This class provides the frontend configuration constants

    It uses the singleton pattern to ensure there is only one instance of the 
    warehouse and algo to provide accessibility in any section of the code
    """
    class __wh_frontend_config:
        """Private class to feature the singleton pattern"""
        ## Current resources manager path
        CURRENT_PATH = None
        ## The home path
        HOME_PATH = None
        ## Number of archives
        NUM_ARCHIVES = 2
        ## Maximum pages
        MAX_PAGES = 5
        ## Maximum algorithms per page
        MAX_ALG_PER_PAGE = 5
        ## Maximum executions per page
        MAX_EXEC_PER_PAGE = 5
        ## Maximum queries per page
        MAX_QUERY_PER_PAGE = 5
        ## Maximum resources per page
        MAX_RESOURCES_PER_PAGE = 5
        ## Maximum results per page
        MAX_RESULTS_PER_PAGE = 5
        ## Current algorithm page
        CURRENT_ALG_PAGE = 1
        ## Current executions page
        CURRENT_EXEC_PAGE = 1
        ## Current queries page
        CURRENT_QUERY_PAGE = 1
        ## Current resources page
        CURRENT_RESOURCES_PAGE = 1
        ## Current results page
        CURRENT_RESULTS_PAGE = 1

        # SORTING BY name date id status size
        ## Sorting algorithms by
        SORTING_ALG_BY = "name"
        ## Sorting executions by
        SORTING_EXEC_BY = "-date"
        ## Sorting queries by
        SORTING_QUERY_BY = "date"
        ## Sorting resources by
        SORTING_RESOURCES_BY = "name"
        ## Sorting results by
        SORTING_RESULTS_BY = "name"
        ## The log
        log = None
        ## The log header
        str_log_header = 'wh_frontend_config'

        def __init__(self):
            """Constructor
            Initializes the log
            
            Args:
            self: The object pointer
            """
            self.log = logger().get_log(self.str_log_header)

        def load(self, cfg = None):
            """Loads the warehouse

            Loads the warehouse with the given configuration

            Args:
            self: The object pointer
            cfg: The configuration to be loaded
            """
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
        """Constructor
        
        The constructor will create a new __wh_frontend_config object in case 
        there is none initialized, otherwise it will not do anything
        
        Args:
        self: The object pointer
        """
        if not wh_frontend_config.instance:
            wh_frontend_config.instance=wh_frontend_config.__wh_frontend_config()
    def get(self):
        """ Returns the warehouse intance
        
        Args:
        self: The object pointer
        
        Returns:
        The instance of the warehouse
        """
        return wh_frontend_config.instance

    instance = None
