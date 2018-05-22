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

@package avi.utils.config_manager

--------------------------------------------------------------------------------

This module features the configuration_manager class
"""
import xml.etree.ElementTree
import os.path

#from risea.log import logger
from avi.log import logger

def read_login(path):
    """Deprecated, used for debugging purposes only"""
    file = open(path, "r")
    ret = {}
    ret['user'] = file.readline()
    ret['user'] = ret['user'][:-1]
    ret['passwd'] = file.readline()
    file.close()
    return ret

class configuration_manager:
    """@class configuration_manager
    This class manages the application configuration

    The class reads the configuration files and store the information readed.
    """
    ## Gaia configuration
    gaia_config = None
    ## Herschel configuration
    herschel_config = None
    ## SAMP configuration
    samp_config = None
    ## file manager configuration
    file_manager_config = None
    ## Herschel archive tables
    hsa_tables = None
    ## Gaia DR1 tables
    gaiadr1_tables = None
    ## Gaia DR2 tables
    gaiadr2_tables = None

    ## XML file's root
    xml_root = None
    ## The log
    log = None

    def __init__(self):
        """The constructor
        
        Initializes the log

        Args:
        self: The object pointer
        """
        self.log = logger().get_log('configuration_manager')

    def get(self, config_name):
        """Returns the given configuration
        
        Reads the xml_root and returns the given configuration from it.

        Args:
        self: The object pointer
        config_name: The configuration to be returned

        Returns: 
        The given configuration if it is located in the xml_root, None otherwise
        """
        if not self.xml_root:
            self.log.error("There is no config file loaded")
            return None
        ret = None
        for child in self.xml_root:
            if child.tag == config_name:
                ret = {}
                for att in child:
                    ret[att.tag] = child.find(att.tag).text
        return ret

    def load(self, config_file):
        """Loads the configuration file
        
        Loads a given configuration file

        Args:
        self: The object pointer
        config_file: The configuration file
        
        Returns:
        True if the configuration file was read correctly, False otherwise
        """
        if(not os.path.isfile(config_file)):
            self.log.error('Configuration file %s not found!', config_file)
            return False
        self.xml_root = xml.etree.ElementTree.parse(config_file).getroot()
        return True
        
    def _load(self, config_file):
        """Deprecated"""
        if(not os.path.isfile(config_file)):
            self.log.error('Configuration file %s not found!', config_file)
            return False
        xml_root = xml.etree.ElementTree.parse(config_file).getroot()
        self.xml_root = xml_root
        current_config = None
        for child in xml_root:
            if child.tag == 'gaia':
                self.gaia_config = {}
                current_config = self.gaia_config
            elif child.tag == 'samp':
                self.samp_config = {}
                current_config = self.samp_config
            elif child.tag == 'herschel':
                self.herschel_config = {}
                current_config = self.herschel_config
            elif child.tag == 'file_manager':
                self.file_manager_config = {}
                current_config = self.file_manager_config
            elif child.tag == 'hsa_tables':
                self.hsa_tables = {}
                current_config = self.hsa_tables
            elif child.tag == 'gaiadr1_tables':
                self.gaiadr1_tables = {}
                current_config = self.gaiadr1_tables
            elif child.tag == 'gaiadr2_tables':
                self.gaiadr2_tables = {}
                current_config = self.gaiadr2_tables
            
            if current_config != None:    
                for att in child:
                    current_config[att.tag] = child.find(att.tag).text
                
                current_config = None
        return True

class logger_configuration:
    """Deprecated, moved to another module"""
    log_config = None
    def load(self, log_config):
        self.log_config = {}
        log = logger()
        if(not os.path.isfile(log_config)):
            print('Warning, log configuration file ' +log_config+' not found!')
            print('Will now initialize default log configuration...')
            log.default_log()
            return log
        xml_root = xml.etree.ElementTree.parse(log_config).getroot()
        for child in xml_root:
            if child.tag == 'config':
                self.load_config(child, log)
            if child.tag == 'level':
                self.load_level(child, log)
            #self.log_config[child.tag] = child.text
            #log.create(child.tag, child.text)
        return log
    
    def load_level(self, node, log):
        for child in node:
            log.create(child.tag, child.text)
        
    def load_config(self, node, log):
        fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        default_level = "info"
        file_fmt = "sfm-demo.log"
        backup_count = 0
        max_bytes = 0
        rotation = False
        console = True
        for child in node:
            if child.tag == 'format':
                fmt = node.find(child.tag).text
            if child.tag == 'default_level':
                default_level = node.find(child.tag).text
            if child.tag == 'file_config':
                if child.get('to_file') == 'true':
                    file_fmt = child.find('file_format').text
                    backup_count = child.find('backup_count').text
                    max_bytes = child.find('max_bytes').text
                else:
                    file_fmt = None
                if child.get('rotation') == 'true':
                    rotation = True
                if child.get('console') == 'false':
                    console = False
        log.set_config(fmt, default_level, file_fmt, console, rotation, backup_count, max_bytes)
