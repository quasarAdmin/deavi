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

@package avi.core.risea

--------------------------------------------------------------------------------

This module provides the RISEA interface
"""
# RISEA's API
# Here goes the API of the star form mapper project

# FIXME: ignore astroquery warnings
import warnings, os
from astropy.utils.exceptions import AstropyWarning
warnings.simplefilter('ignore',category=AstropyWarning)
# #################################

#from anaconda_navigator.config import HOME_PATH
# from risea.log import logger
from avi.log import logger

from avi.warehouse import wh_frontend_config
from avi.warehouse import wh_global_config

class risea:
    """@class risea
    This class provides the RISEA interface

    It uses the singleton pattern to ensure there is only one instance of RISEA 
    and also to provide accessibility in any secion of the code
    """
    instance = None

    class __risea:
        """Private class to feature the singleton pattern"""
        # FIXME: ? should we be using input dir for this?
        ## Deprecated
        str_log_config_file = 'avi/config/log_config.xml'
        ## Deprecated
        str_config_file = 'avi/config/config.xml'
        ## Deprecated
        str_global_config_file = 'avi/config/global_config.xml'
        #str_log_config_file = '/opt/gavip_avi/avi/config/log_config.xml'
        #str_config_file = '/opt/gavip_avi/avi/config/config.xml'
        
        ## The log header
        str_log_header = 'risea'
        ## The log
        log = None
        ## The application configuration
        cfg = None
        ## The interface manager
        interface_manager = None
        
        #FIXME: deprecated, remove at some point
        ## Deprecated
        gaia = None
        ## Deprecated
        herschel = None
        ## Deprecated
        file_manager = None
        ## Deprecated
        resources_manager = None
        # warehouse
        ## Deprecated
        current_frontend_resources_path = None
        
        def __init__(self):
            """Constructor
            
            Initializes the log, the warehouses, the configuration and the 
            interface_manager
            
            Args:
            self: The object pointer
            """
            ipath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config')
            #wh_global_config().get().INPUT_PATH
            self.str_log_config_file = os.path.join(ipath, 'log_config.xml')
            self.str_config_file = os.path.join(ipath, 'config.xml')
            self.str_global_config_file = os.path.join(ipath, 'global_config.xml')
            from avi.utils.config_manager import logger_configuration
            log_cfg = logger_configuration()
            log_cfg.load(self.str_log_config_file)
            self.log = logger().get_log(self.str_log_header)
            self.log.info("Initialization of RISEA...")
            self.log.info("RISEA ptr : %s",self.get_ptr())

            # loading cfg
            from avi.utils.config_manager import configuration_manager
            self.cfg = configuration_manager()
            if not self.cfg.load(self.str_config_file):
                self.log.error("Failed to load the configuration %s",
                               self.str_config_file)
                return
            
            # Initialization of the warehouses
            cfg = configuration_manager()
            if not cfg.load(self.str_global_config_file):
                self.log.error("Failed to load the configuration %s",
                               self.str_global_config_file)
                return
            
            wh_global_config().get().load(cfg.get("global"))
            wh_frontend_config().get().load(cfg.get("frontend"))
            wh_frontend_config().get().\
                CURRENT_PATH = os.path.\
                normpath("".join(wh_global_config().get().RESOURCES_PATH))
            wh_frontend_config().get().\
                HOME_PATH = os.path.\
                normpath("".join(wh_global_config().get().RESOURCES_PATH))
            self.log.info("current id : %s\n resources id : %s",
                          id(wh_frontend_config().get().CURRENT_PATH),
                          id(wh_global_config().get().RESOURCES_PATH))
            # Initialization of the interface manager
            from .interface.interface_manager import interface_manager
            self.interface_manager = interface_manager()
            self.interface_manager.init(self.cfg)
            # Initialization of the resources
            from avi.utils.resources_manager import resources_manager
            resources_manager().init()

        #
        # Initialization methods
        #
        
        #
        # Archive's data retrievement methods
        #
        
        #   
        # Asynchronous tasks and pipeline methods
        #
        def start_job(self, name,  data):
            """Starts a new job

            This method starts a new job with the given name and the given data

            Args:
            self: The object pointer
            name: The name of the job
            data: The input data

            Returns:
            The result of the job initialization
            """
            from .pipeline.pipeline_manager import pipeline_manager
            pm = pipeline_manager()
            res = pm.start_job(name, data)
            if res.ok:
                self.log.info("The job %s has started...", name)
                return res
            self.log.error("The job %s has NOT started!", name)
            return res
        
        def _start_gaia_query(self, data):
            """Deprecated"""
            from .pipeline.pipeline_manager import pipeline_manager
            pm = pipeline_manager()

            res = pm.start_job(name = "gaia_query", data = data)
            if res.ok:
                self.log.info("The gaia query has started...")
                return res
            
            self.log.error("The gaia query has NOT started...")
            return res
        
        #    
        # File management methods
        #
        def save_plain_votable(self, data, name):
            """Deprecated"""
            if not self.file_manager:
                self.log.error('There is no file manager initialized!')
                return ""

            return self.file_manager.save_file_plain_data(data, name)
        
        #
        # Frontend configutaion management methods
        #
        def get_gaia_tables(self):
            """Deprecated"""
            if not self.cfg:
                return []
            #if not self.cfg.gaiadr1_tables:
            #    return []
            ret = []
            tables = self.cfg.get("gaiadr1_tables")
            for k in tables:
                #self.log.debug(k)
                ret.append(tables[k])
            return ret

        def get_algorithm(self, data):
            """Returns the algorithm information
            Args:
            self: The object pointer
            data: A JSON file with the information

            Returns:
            A dictionary with the algorithm information
            """
            from avi.core.algorithm.algorithm_manager import algorithm_manager
            return algorithm_manager().get_algorithm_info(data)

        def get_algorithm_list(self):
            """Returns the list of algorithms
            
            Args:
            self: The object pointer
            
            Returns:
            A dictionary with the information of all algorithms
            """
            from avi.core.algorithm.algorithm_manager import algorithm_manager
            return algorithm_manager().get_algorithm_list()
        
        def get_file_list(self):
            """Deprecated"""
            from avi.utils.resources_manager import resources_manager
            return resources_manager() \
                .get_file_list(wh_frontend_config().get().CURRENT_PATH)

        def  move_default_directory(self):
            """Moves the warehouse current path to the home directory
            
            Args:
            self: The object pointer
            
            Returns:
            The warehouse current path
            """
            from avi.utils.resources_manager import resources_manager
            return resources_manager() \
                .move_absolute_directory("".join(wh_frontend_config().\
                                                 get().HOME_PATH))

        def  directory_down(self, folder_local):
            """Moves the warehouse current path to the given new location
            
            Args:
            self: The object pointer
            folder_local: The directory to enter

            Returns:
            The warehouse current path
            """
            from avi.utils.resources_manager import resources_manager
            return resources_manager() \
                .directory_down(wh_frontend_config().get().\
                                CURRENT_PATH, folder_local)

        def  directory_up(self):
            """Moves the warehouse current path to the parent directory
            
            Args:
            self: The object pointer
            
            Returns:
            The warehouse current path
            """
            from avi.utils.resources_manager import resources_manager
            return resources_manager() \
                .directory_up(wh_frontend_config().get().CURRENT_PATH)

        def  create_directory(self, directory):
            """Deprecated"""
            from avi.utils.resources_manager import resources_manager
            return resources_manager() \
                .create_directory(directory)

        def  get_folder_size(self, directory):
            """Deprecated"""
            from avi.utils.resources_manager import resources_manager
            return resources_manager().get_folder_size(directory)

        def  delete_directory(self, directory):
            """Deprecated"""
            from avi.utils.resources_manager import resources_manager
            return resources_manager().delete_directory(directory)

        def  rename_directory(self, name, new_name):
            """Deprecated"""
            from avi.utils.resources_manager import resources_manager
            return resources_manager().rename_directory(name, new_name)

        def  delete_file(self, file_name):
            """Deletes the given file
            
            Args:
            self: The object pointer
            file_name: The file to be deleted
            
            Raises:
            Exception: if something went wrong with the deletion
            """
            from avi.utils.resources_manager import resources_manager
            return resources_manager().delete_file(file_name)

        def  rename_file(self, name, new_name):
            """Deprecated"""
            from avi.utils.resources_manager import resources_manager
            return resources_manager().rename_file(name, new_name)


#         def  get_current_path(self):
#             from avi.utils.resources_manager import resources_manager
#             return resources_manager().get_current_path()
                

    # #########################################################################

        #
        #
        def get_ptr(self):
            """For debuggin purposes only"""
            return repr(self)
        #
        # end of the private class
        #

    # Public interface
        
    def __init__(self):
        """Constructor
        
        The constructor will create a new __risea object in case 
        there is none initialized, otherwise it will not do anything
        
        Args:
        self: The object pointer
        """
        if not risea.instance:
            risea.instance = risea.__risea()

    def get(self):
        """Returns the risea intance
        
        Args:
        self: The object pointer
        
        Returns:
        The instance of the warehouse
        """
        return risea.instance

