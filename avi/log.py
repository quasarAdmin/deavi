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

@package avi.log

--------------------------------------------------------------------------------

This module provides a logger for the project.

This module is formed by the logger class and the logger_configuration class.
"""
import logging
import logging.handlers
import xml.etree.ElementTree
import os.path

class logger:
    """@class logger
    The logger class provides the log utilities.
    
    It uses the singleton pattern to ensure there is only
    one instance of the log and also provides accessibility 
    in any section of the code.
    """
    ## Instance of the __logger
    instance = None
    ## The name of the log file
    file_name = None
    ## Is in console mode?
    console = False
    ## Has to do file rotation?
    rotation = False
    ## Number of backups
    backup_count = 0
    ## Max bytes per file
    max_bytes = 0
    ## The log handler
    handler = None
    ## The default level of logging
    default_level = 'critical'
    ## Is the configuration loaded?
    is_config_loaded = False
    class __logger:
        """Private class to feature the singleton pattern."""
        log = None
        def __init__(self):
            """__logger constructor"""
            self.log = {}
    
    def __init__(self):
        """logger constructor
        
        The constructor will create a new __logger object in case there is
        none initialized, otherwise it will not do anything.
        
        Args:
        self: The object pointer.
        """
        #logging.basicConfig(filename='log.log', level=logging.INFO)
        if not logger.instance:
            logger.instance = logger.__logger()
            
    def default_log(self):
        """Sets a default log in case no configuration is loaded"""
        #logging.basicConfig(level = logging.DEBUG)
        logging.basicConfig(level = logging.CRITICAL)
        
    def create(self, name, level):
        """Creates a new log
        
        This method creates a new log with the given name and the given level

        Args:
        self: The object pointer.
        name: The name of the new log.
        level: The level of the new log.
        """
        log = logging.getLogger(name)
        log.setLevel(self.get_level(level))
        if self.rotation:
            log.addHandler(self.handler)
            if not self.console:
                log.propagate = False
        logger.instance.log[name] = log
        
    def get_log(self, name):
        """Returns a log

        Returns a log by the given name. If the log does not exist, 
        it will create a new log with the given name and the default level.
        
        Args:
        self: The object pointer.
        name: The name of the log to retrieve.

        Returns:
        The log

        Examples:
        log = logger().get_log("log_name")
        """
        try:
            logger.instance.log[name]
        except KeyError:
            self.create(name,self.default_level)
        return logger.instance.log[name]
    
    def set_config(self, fmt, lvl, file, console, rotation, backup_count, max_bytes):
        """Sets up the log configuration.

        Sets the log configuration with the given parameters.
        
        Args:
        self: The object pointer.
        fmt: The log format.
        lvl: The default level.
        file: The name of the log file.
        console: Is console mode?
        rotation: Has file rotation?
        backup_count: Number of backups.
        max_bytes: Max number of bytes per file.
        """
        self.file_name = file
        self.console = console
        self.rotation = rotation
        self.backup_count = int(backup_count)
        self.max_bytes = int(max_bytes)
        self.default_level = lvl
        
        if not file or rotation:
            logging.basicConfig(format = fmt, level = self.get_level(lvl))
            if self.rotation:
                self.handler = logging.handlers.RotatingFileHandler(
                    filename = self.file_name,
                    maxBytes = self.max_bytes,
                    backupCount= self.backup_count)
                formatter = logging.Formatter(fmt)
                self.handler.setFormatter(formatter)
        else:
            logging.basicConfig(format = fmt, filename = file, level = self.get_level(lvl))
        is_config_loaded = True
    
    def get_level(self, level):
        """Returns the logging level.
        
        Returns the logging level by a given string.
        
        Args:
        self: The object pointer.
        level: The string with the level to retrieve.
        
        Returns:
        The logging level.
        """
        if level == 'debug':
            return logging.DEBUG
        if level == 'info':
            return logging.INFO
        if level == 'warning':
            return logging.WARNING
        if level == 'error':
            return logging.ERROR
        if level == 'critical':
            return logging.CRITICAL

class logger_configuration:
    """@class logger_configuration
    The logger_configuration class provides methods to configure the logger.
    
    It reads a configuration file and sets up the logger.
    """
    ## Dictionary with the configuration information extracted from 
    # the configuration file.
    log_config = None
    def load(self, log_config):
        """Loads the configuration file.

        It reads the file and extracts the configuration. If there is not 
        configuration file sets the default configuration.

        Args:
        log_config: The configuration file.

        Returns:
        The configured log.
        """
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
        """Create the logs within a xml node.

        Reads the given xml node and creates the logs within it.

        Args:
        node: The xml node.
        log: The logger in which the logs will be created.
        """
        for child in node:
            log.create(child.tag, child.text)
        
    def load_config(self, node, log):
        """Loads the configuration within a xml node.

        Reads the given xml node and sets the configuration within it.

        Args:
        node: The xml node.
        log: the logger in which the configuration will be set.
        """
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
