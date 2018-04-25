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
import logging
import logging.handlers
import xml.etree.ElementTree
import os.path

class logger:
    instance = None
    file_name = None
    console = False
    rotation = False
    backup_count = 0
    max_bytes = 0
    handler = None
    default_level = 'critical'

    is_config_loaded = False
    class __logger:
        log = None
        def __init__(self):
            self.log = {}
    
    def __init__(self):
        #logging.basicConfig(filename='log.log', level=logging.INFO)
        if not logger.instance:
            logger.instance = logger.__logger()
            
    def default_log(self):
        #logging.basicConfig(level = logging.DEBUG)
        logging.basicConfig(level = logging.CRITICAL)
        
    def create(self, name, level):
        log = logging.getLogger(name)
        log.setLevel(self.get_level(level))
        if self.rotation:
            log.addHandler(self.handler)
            if not self.console:
                log.propagate = False
        logger.instance.log[name] = log
        
    def get_log(self, name):
        try:
            logger.instance.log[name]
        except KeyError:
            self.create(name,self.default_level)
        return logger.instance.log[name]
    
    def set_config(self, fmt, lvl, file, console, rotation, backup_count, max_bytes):
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
