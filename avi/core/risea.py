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

    instance = None

    class __risea:
        # TODO move this constant to common file
        # FIXME: ? should we be using input dir for this?
        str_log_config_file = 'avi/config/log_config.xml'
        str_config_file = 'avi/config/config.xml'
        str_global_config_file = 'avi/config/global_config.xml'
        #str_log_config_file = '/opt/gavip_avi/avi/config/log_config.xml'
        #str_config_file = '/opt/gavip_avi/avi/config/config.xml'
        
        str_log_header = 'risea'
        log = None
        
        cfg = None
        interface_manager = None
        
        #FIXME: deprecated, remove at some point
        gaia = None
        herschel = None
        file_manager = None
        resources_manager = None
        # warehouse
        current_frontend_resources_path = None
        
        def __init__(self):
            
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
            from .pipeline.pipeline_manager import pipeline_manager
            pm = pipeline_manager()
            res = pm.start_job(name, data)
            if res.ok:
                self.log.info("The job %s has started...", name)
                return res
            self.log.error("The job %s has NOT started!", name)
            return res
        
        def _start_gaia_query(self, data):
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
            if not self.file_manager:
                self.log.error('There is no file manager initialized!')
                return ""

            return self.file_manager.save_file_plain_data(data, name)
        
        #
        # Frontend configutaion management methods
        #
        def get_gaia_tables(self):
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
            from avi.core.algorithm.algorithm_manager import algorithm_manager
            return algorithm_manager().get_algorithm_info(data)

        def get_algorithm_list(self):
            from avi.core.algorithm.algorithm_manager import algorithm_manager
            return algorithm_manager().get_algorithm_list()
        
        def get_file_list(self):
            from avi.utils.resources_manager import resources_manager
            return resources_manager() \
                .get_file_list(wh_frontend_config().get().CURRENT_PATH)

        def  move_default_directory(self):
            from avi.utils.resources_manager import resources_manager
            return resources_manager() \
                .move_absolute_directory("".join(wh_frontend_config().\
                                                 get().HOME_PATH))

        def  directory_down(self, folder_local):
            from avi.utils.resources_manager import resources_manager
            return resources_manager() \
                .directory_down(wh_frontend_config().get().\
                                CURRENT_PATH, folder_local)

        def  directory_up(self):
            from avi.utils.resources_manager import resources_manager
            return resources_manager() \
                .directory_up(wh_frontend_config().get().CURRENT_PATH)

        def  create_directory(self, directory):
            from avi.utils.resources_manager import resources_manager
            return resources_manager() \
                .create_directory(directory)

        def  get_folder_size(self, directory):
            from avi.utils.resources_manager import resources_manager
            return resources_manager().get_folder_size(directory)

        def  delete_directory(self, directory):
            from avi.utils.resources_manager import resources_manager
            return resources_manager().delete_directory(directory)

        def  rename_directory(self, name, new_name):
            from avi.utils.resources_manager import resources_manager
            return resources_manager().rename_directory(name, new_name)

        def  delete_file(self, file_name):
            from avi.utils.resources_manager import resources_manager
            return resources_manager().delete_file(file_name)

        def  rename_file(self, name, new_name):
            from avi.utils.resources_manager import resources_manager
            return resources_manager().rename_file(name, new_name)


#         def  get_current_path(self):
#             from avi.utils.resources_manager import resources_manager
#             return resources_manager().get_current_path()
                

    # #########################################################################

        #
        #
        def get_ptr(self):
            return repr(self)
        #
        # end of the private class
        #

    # Public interface
        
    def __init__(self):
        if not risea.instance:
            risea.instance = risea.__risea()

    def get(self):
        return risea.instance

