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

@package avi.utils.resources_manager

--------------------------------------------------------------------------------

This module provides an interface to the resources
"""
import os, math, collections
from avi.log import logger

from avi.warehouse import wh_frontend_config
from avi.warehouse import wh_global_config

from avi.utils.data.file_manager import file_manager

'''Resources to manage files'''
# Methods related to general file management

class resources_manager(object):
    """@class resources_manager
    This class manages the application resources
    """
    ## The log
    log = None
    def __init__(self):
        """Constructor
        
        Initializes the log
        """
        self.log = logger().get_log('resources_manager')
        
    def init(self):
        """Initialization method
        
        Creates the needed directories to store the resources

        Args:
        self: The object pointer
        """
        gconf = wh_global_config().get()
        # TODO: exception management
        if not self.dir_exists(gconf.SOURCES_PATH):
            try:
                os.makedirs(gconf.SOURCES_PATH)
            except OSError:
                pass
        if not self.dir_exists(gconf.GAIA_PATH):
            try:
                os.makedirs(gconf.GAIA_PATH)
            except OSError:
                pass
        if not self.dir_exists(gconf.HSA_PATH):
            try:
                os.makedirs(gconf.HSA_PATH)
            except OSError:
                pass
        if not self.dir_exists(gconf.RESULTS_PATH):
            try:
                os.makedirs(gconf.RESULTS_PATH)
            except OSError:
                pass
        if not self.dir_exists(gconf.TMP_PATH):
            try:
                os.makedirs(gconf.TMP_PATH)
            except OSError:
                pass
        if not self.dir_exists(gconf.UPLOADED_ALGORITHM_PATH):
            try:
                os.makedirs(gconf.UPLOADED_ALGORITHM_PATH)
            except OSError:
                pass        
        if not self.dir_exists(gconf.TMP_ALGORITHM_PATH):
            try:
                os.makedirs(gconf.TMP_ALGORITHM_PATH)
            except OSError:
                pass
        if not self.dir_exists(gconf.USER_PATH):
            try:
                os.makedirs(gconf.USER_PATH)
            except OSError:
                pass
        else:
            import shutil
            for f in os.listdir(gconf.TMP_ALGORITHM_PATH):
                full_path = os.path.join(gconf.TMP_ALGORITHM_PATH, f)
                try:
                    if os.path.isfile(full_path):
                        os.unlink(full_path)
                    elif os.path.isdir(full_path):
                        shutil.rmtree(full_path)
                except Exception:
                    pass
            pass

    def get_file_list(self, path):
        """Deprecated?
        Retrieves all the files and directories within a path

        Args:
        self: The object pointer
        path: The path

        Returns:
        All the files and directories within the given path
        """
        "Get a list of folders and files in the current folder"
        directory_list = os.listdir(path)
        directory_list.sort()
        directories = collections.OrderedDict()
        files = collections.OrderedDict()
        fm = file_manager()
        for f in directory_list:
            if os.path.isdir(os.path.join(path, f)):
                directories[f] = self. \
                convert_size(self.get_folder_size(os.path.join(path, f)))
            if os.path.isfile(os.path.join(path, f)):
                file_id = fm.get_file_id(path,f)
#                 import re 
#                 files[re.sub('[^A-Za-z0-9._]+.', '', f)] = self. \
                files[file_id] = (f, self. \
                convert_size(self.get_file_size(os.path.join(path, f))))
        #self.log = logger().get_log('directories')
        return directories, files

    def get_list(self, path):
        """Returns the files and directories names within a path
        
        Args: 
        self: The object pointer
        path: The path
        
        Returns:
        An array with all the files and directories names within a path
        """
        return os.listdir(path)

    def get_info(self, data, path):
        """Returns the files and directories information
        
        Returns the files and directories inforamtion within the given files 
        contained in 'data' and the given path
        Args: 
        self: The object pointer
        data: The files which information has to be retrieved
        path: The path
        
        Returns:
        All the files and directories informatin within 'data' and 'path'
        """
        directories = collections.OrderedDict()
        files = collections.OrderedDict()
        fm = file_manager()
        for f in data:
            if os.path.isdir(os.path.join(path, f)):
                directories[f] = self. \
                convert_size(self.get_folder_size(os.path.join(path, f)))
            if os.path.isfile(os.path.join(path, f)):
                file_id = fm.get_file_id(path,f)
                files[file_id] = (f, self. \
                convert_size(self.get_file_size(os.path.join(path, f))))
        return directories, files

    ####################### DIRECTORIES #######################################
       
    def dir_exists(self, path):
        """Checks if the directory exists
        
        Args:
        self: The object pointer
        path: Path to check

        Returns:
        True if the given directory exists, False otherwise
        """
        return os.path.isdir(path)   
    
    def move_absolute_directory(self, path):
        """Moves the current warehouse path to the given path

        This method changes the CURRENT_PATH stored in the wh_frontend_config 
        warehouse to the given path

        Args:
        self: The object pointer
        path: The new current path

        Returns:
        The new current path if everything went correctly, False otherwise
        
        See:
        wh_frontend_config: avi.warehouse.wh_frontend_config
        """
        if self.dir_exists(path):
            new_directory = wh_frontend_config().get().CURRENT_PATH = path 
            return new_directory
        else:
            self.log.info('The directory does not exist.')
            return False

    def directory_up(self, path):
        """Moves the current warehouse path to the parent of the given path

        This method changes the CURRENT_PATH stored in the wh_frontend_config 
        warehouse to the parent of the given path

        Args:
        self: The object pointer
        path: The path which parent will be the new current path

        Returns:
        The new current path if everything went correctly, None otherwise
        
        See:
        wh_frontend_config: avi.warehouse.wh_frontend_config
        """
        if path == wh_frontend_config().get().HOME_PATH:
            self.log.info('The directory does not exist.')
        else:
            wh_frontend_config() \
            .get().CURRENT_PATH = \
            self.move_absolute_directory(os.path.split(path)[0])
            return wh_frontend_config().get().CURRENT_PATH

    def directory_down(self, path, down_dir):
        """Moves the current warehouse path to the given path specified 
        directory

        This method changes the CURRENT_PATH stored in the wh_frontend_config 
        warehouse to the given path spacified directory

        Args:
        self: The object pointer
        path: The path from which the down_dir directory must be
        down_dir: The new current path

        Returns:
        The new current path if everything went correctly
        
        See:
        wh_frontend_config: avi.warehouse.wh_frontend_config
        """
        wh_frontend_config().get().CURRENT_PATH =  \
        self.move_absolute_directory(os.path.join(path, down_dir))
        return wh_frontend_config().get().CURRENT_PATH
    
    def create_directory(self, directory):
        """Deprecated"""
        import re, errno
        if re.match("^[a-zA-Z0-9_ ]*$", directory):
            path_full = \
            wh_frontend_config().get().CURRENT_PATH + "/" + directory
            try:
                os.makedirs(path_full)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
        else:
            raise
    
    def get_folder_size(self, directory):
        """Retruns the size of the given directory
        
        Args:
        self: The object pointer
        directory: The directory to be measured

        Retruns:
        The size of the given directory
        """
        total_size = os.path.getsize(directory)
        for item in os.listdir(directory):
            itempath = os.path.join(directory, item)
            if os.path.isfile(itempath):
                total_size += os.path.getsize(itempath)
            elif os.path.isdir(itempath):
                total_size += self.get_folder_size(itempath)
        return total_size
  
    def delete_directory(self, directory):
        """Deprecated"""
        import shutil
        folder = \
            wh_frontend_config().get().CURRENT_PATH + "/" + directory
        if os.path.isdir(folder):      
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path): 
                    shutil.rmtree(file_path)
                else:
                    self.log.info('The directory does not exist.')
            if  os.path.isdir(folder):
                os.rmdir(folder)
            else:
                self.log.info('The directory does not exist.')
        else:
            self.log.info('The directory does not exist.')

    def rename_directory(self, name, new_name):
        """Deprecated"""
        folder = \
            wh_frontend_config().get().CURRENT_PATH + "/" + name
        new_folder = \
            wh_frontend_config().get().CURRENT_PATH + "/" + new_name               
        if os.path.isdir(folder):
            if os.path.isdir(new_folder):
                self.log.info('The directory already exists.')
            else:
                os.rename(folder, new_folder)
        else:
            self.log.info('The directory does not exists.')         

    ####################### FILES ############################################# 
    
    def file_exists(self, path):
        """Checks if the file exists
        
        Args:
        self: The object pointer
        path: Path to check

        Returns:
        True if the given file exists, False otherwise
        """
        return os.path.isfile(path)
    
    def get_file_size(self, file):
        """Returns the size of the given file
        
        Args:
        self: The object pointer
        file: The file

        Returns:
        The size of the given file
        """
        if os.path.isfile(file):
            return os.path.getsize(file)
    
    def delete_file(self, file_name):
        """Deletes the given file
        
        Args:
        self: The object pointer
        file_name: the file to be deleted

        Raises:
        Exception: if the an unknow error happens
        """
#         file_to_delete = \
#             wh_frontend_config().get().CURRENT_PATH + "/" + file_name
        path_to_delete =  wh_frontend_config().get().CURRENT_PATH
        self.log.info(path_to_delete)
        self.log.info(file_name)
        self.log.info(file_name.startswith('gaia'))
        if file_name.startswith('gaia'):
            if 'gaia' not in path_to_delete:
                path_to_delete = "/data/output/sources/gaia"
        elif  file_name.startswith('hsa'):
            if 'hsa' not in path_to_delete:
                path_to_delete = "/data/output/sources/hsa"
        elif  file_name.startswith('res'):
            if 'results' not in path_to_delete:
                path_to_delete = "/data/output/results"
        elif  file_name.startswith('user'):
            if 'user' not in path_to_delete:
                path_to_delete = "/data/output/user"

        try:
#             os.remove(file_to_delete)
            file_manager().remove_file(file_name, path_to_delete)
        # this would be "except OSError, e:" before Python 2.6
        except OSError as e:
            # errno.ENOENT = no such file or directory 
            if e.errno != errno.ENOENT: 
                raise # re-raise exception if a different error occurred

    def rename_file(self, name, new_name):
        """Deprecated"""
        old_file = \
            wh_frontend_config().get().CURRENT_PATH + "/" + name
        new_file = \
            wh_frontend_config().get().CURRENT_PATH + "/" + new_name               
        if os.path.isfile(old_file):
            if os.path.isfile(new_file):
                self.log.info('The file already exists.')
            else:
                os.rename(old_file, new_file)
        else:
            self.log.info('The file does not exists.')
  
    ####################### UTILS #############################################
    def convert_size(self, size_bytes):
        """Convert the size to human readable
        
        Args:
        self: The object pointer
        size_bytes: The size to be converted

        Returns:
        The given size in a human readable way
        """
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

