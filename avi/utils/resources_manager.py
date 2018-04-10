import os, math, collections
from avi.log import logger

from avi.warehouse import wh_frontend_config
from avi.warehouse import wh_global_config

from avi.utils.data.file_manager import file_manager

'''Resources to manage files'''
# Methods related to general file management

class resources_manager(object):
    
    log = None
    def __init__(self):
        self.log = logger().get_log('resources_manager')
        
    def init(self):
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
        return os.listdir(path)

    def get_info(self, data, path):
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
        return os.path.isdir(path)   
    
    def move_absolute_directory(self, path):
        if self.dir_exists(path):
            new_directory = wh_frontend_config().get().CURRENT_PATH = path 
            return new_directory
        else:
            self.log.info('The directory does not exist.')
            return False

    def directory_up(self, path):
        if path == wh_frontend_config().get().HOME_PATH:
            self.log.info('The directory does not exist.')
        else:
            wh_frontend_config() \
            .get().CURRENT_PATH = \
            self.move_absolute_directory(os.path.split(path)[0])
            return wh_frontend_config().get().CURRENT_PATH

    def directory_down(self, path, down_dir):
        wh_frontend_config().get().CURRENT_PATH =  \
        self.move_absolute_directory(os.path.join(path, down_dir))
        return wh_frontend_config().get().CURRENT_PATH
    
    def create_directory(self, directory):
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
        total_size = os.path.getsize(directory)
        for item in os.listdir(directory):
            itempath = os.path.join(directory, item)
            if os.path.isfile(itempath):
                total_size += os.path.getsize(itempath)
            elif os.path.isdir(itempath):
                total_size += self.get_folder_size(itempath)
        return total_size
  
    def delete_directory(self, directory):
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
        return os.path.isfile(path)
    
    def get_file_size(self, file):
        if os.path.isfile(file):
            return os.path.getsize(file)
    
    def delete_file(self, file_name):
#         file_to_delete = \
#             wh_frontend_config().get().CURRENT_PATH + "/" + file_name
        path_to_delete =  wh_frontend_config().get().CURRENT_PATH
        self.log.info(path_to_delete)

        try:
#             os.remove(file_to_delete)
            file_manager().remove_file(file_name, path_to_delete)
        # this would be "except OSError, e:" before Python 2.6
        except OSError as e:
            # errno.ENOENT = no such file or directory 
            if e.errno != errno.ENOENT: 
                raise # re-raise exception if a different error occurred

    def rename_file(self, name, new_name):
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
       if size_bytes == 0:
           return "0B"
       size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
       i = int(math.floor(math.log(size_bytes, 1024)))
       p = math.pow(1024, i)
       s = round(size_bytes / p, 2)
       return "%s %s" % (s, size_name[i])

