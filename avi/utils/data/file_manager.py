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

@package avi.utils.data.file_manager

--------------------------------------------------------------------------------

This module provides the file management
"""
import os
import traceback
import tarfile

from avi.log import logger

from avi.warehouse import wh_global_config
from avi.models import resource_model

class file_manager:
    """@class file_manager
    This class provides the files management
    """
    ## Deprecated
    resources_path = ''
    ## The log
    log = None
    def __init__(self):
        """Constructor
        
        It initializes the log
        """
        self.log = logger().get_log('file_manager')
        #self.date = timezone.now()

    # deprecated
    def __init(self, cfg):
        """Deprecated"""
        if not cfg:
            return False
        try:
            self.resources_path = cfg['resources_path']
            return True
        except KeyError:
            return False

    def save(self):
        """Not implemented"""
        pass

    def update_db(self):
        """Not implemented"""
        pass
    
    def get_file_id(self, path, name):
        """Returns the resource_model id of a given file
        
        Returns the resource_model id of a given file. If the file does not 
        exists then it returns 0

        Args:
        self: The object pointer
        path: The path to the file
        name: The name of the file
        
        Returns:
        The id of the resource_model associated with the given file if the 
        file exists, 0 otherwise

        See:
        resource_model: avi.models.resource_model
        """
        resources = resource_model.objects.filter(path=path).filter(name=name)
        if not resources:
            return 0
        self.log.debug(resources[0].id)
        return resources[0].pk

    def save_file_info(self, name, file_name, id, task_name, date):
        """Saves the information of a given file

        Uses the resource_model to saves the given file information

        Args:
        self: The object pointer
        name: The name of the file
        file_name: The full name of the file
        id: The job id associated with the task that created this file
        task_name: Name of the task that created this file
        date: The date of creation

        Returns:
        The created resource_model

        See:
        resource_model: avi.models.resource_model
        """
        full_name = os.path.basename(file_name)
        path = os.path.dirname(file_name)
        try:
            from avi.models import resource_model
            model = resource_model(sort_name = name,
                                   name = full_name,
                                   path = path,
                                   file_type = task_name,
                                   job_id = id,
                                   date = date)
            model.save()
            return model
        except Exception:
            self.log.warning("Something went wrong while updating the db"
                             " saving tmp file to update the db later")
            self.log.warning(traceback.format_exc())
            tmp_path = wh_global_config().get().TMP_PATH
            full_tmp_path = os.path.join(tmp_path, str(id))
            with open(full_tmp_path, "a") as tmp:
                tmp.write("%s;%s;%s;%s;%s"%(name, path, task_name, 
                                               str(id), str(date)))

    def remove_file(self, name, path):
        """Removes a file

        This method removes the resource_model associated with the given file 
        and then deletes the file itself

        It will do nothing if there is not resource_model associated with the 
        given file

        Args:
        self: The object pointer
        name: The name of the file
        path: The path of the file
        
        See:
        resource_model: avi.models.resource_model
        """
        res = resource_model.objects.filter(name=name).filter(path=path)
        if not res:
            return
        res.delete()
        os.remove(os.path.join(path, name))
                
    def save_file_plain_data(self, data, name, path = None, 
                             id = "", task_name = "", date = ""):
        """Saves a plain data file

        Saves the given data into a file with the given name and creates a 
        resource_model with the file information.

        Args:
        self: The object pointer
        data: The data to be saved
        name: The name of the file
        path: The path of the file
        id: The job id associated with the task that created the file
        task_name: The name of the task that created this file
        date: The date of creation

        Returns:
        The path to the created file

        See:
        resource_model: avi.models.resource_model
        """
        if not path:
            self.log.info("Using default RESULTS_PATH")
            path = wh_global_config().get().RESULTS_PATH

        output_file_name = os.path.join(path, name)
        data = data.encode('utf-8')
        output_file = open(output_file_name, "wb")
        output_file.write(data)
        output_file.close()
        res = os.path.abspath(output_file_name)
        self.log.info("Data saved in: %s", output_file_name)

        try:
            from avi.models import resource_model
            model = resource_model(sort_name = name,
                                   name = name,
                                   path = path,
                                   file_type = task_name,
                                   job_id = id,
                                   date = date)
            model.save()
        except Exception:
            self.log.warning("Something went wrong while updating the db"
                             " saving tmp file to update the db later")
            tmp_path = wh_global_config().get().TMP_PATH
            full_tmp_path = os.path.join(tmp_path, str(id))
            with open(full_tmp_path, "a") as tmp:
                tmp.write("%s;%s;%s;%s;%s"%(name, path, task_name, 
                                               str(id), str(date)))

        return res
        
        # OLD

        self.resources_path = wh_global_config().get().RESOURCES_PATH
        self.log.info("Saving file in %s", self.resources_path)
        outputFileName = os.path.join(self.resources_path, name)
        data = data.encode('utf-8')
        outputFile = open(outputFileName, "wb")
        outputFile.write(data)
        outputFile.close()
        path = os.path.abspath(outputFileName)
        self.log.info("Data saved in: %s", outputFileName)
        return path
    
    def save_file_binary_data(self, data, name):
        """Saves a binary data file (Deprecated)

        Saves the given data into a file with the given name and creates a 
        resource_model with the file information.

        Args:
        self: The object pointer
        data: The data to be saved
        name: The name of the file
        path: The path of the file
        id: The job id associated with the task that created the file
        task_name: The name of the task that created this file
        date: The date of creation

        Returns:
        The path to the created file

        See:
        resource_model: avi.models.resource_model
        """
        if not path:
            self.log.info("Using default RESULTS_PATH")
            path = wh_global_config().get().RESULTS_PATH

        output_file_name = os.path.join(path, name)
        output_file = open(output_file_name, "wb")
        output_file.write(data)
        output_file.close()
        res = os.path.abspath(output_file_name)
        self.log.info("Data saved in: %s", output_file_name)

        try:
            from avi.models import resource_model
            model = resource_model(sort_name = name,
                                   name = name,
                                   path = path,
                                   file_type = task_name,
                                   job_id = id,
                                   date = date)
            model.save()
        except Exception:
            self.log.warning("Something went wrong while updating the db"
                             " saving tmp file to update the db later")
            tmp_path = wh_global_config().get().TMP_PATH
            full_tmp_path = os.path.join(tmp_path, str(id))
            with open(full_tmp_path, "a") as tmp:
                tmp.write("%s;%s;%s;%s;%s"%(name, path, task_name, 
                                               str(id), str(date)))

        return res

        # OLD
        self.resources_path = wh_global_config().get().RESOURCES_PATH
        self.log.info("Saving file in %s", self.resources_path)
        outputFileName = os.path.join(self.resources_path, name)
        outputFile = open(outputFileName, "wb")
        outputFile.write(data)
        outputFile.close()
        path = os.path.abspath(outputFileName)
        self.log.info("Data saved in: %s", outputFileName)
        return path
    
    def save_tar_file(self, source, name, path = None, 
                            id = "", task_name = "", date = ""):
        """Saves a plain data file

        Saves the given data into a file with the given name and creates a 
        resource_model with the file information.

        Args:
        self: The object pointer
        source: The source directory to be saved
        name: The name of the file
        path: The path of the file
        id: The job id associated with the task that created the file
        task_name: The name of the task that created this file
        date: The date of creation

        Returns:
        The path to the created file

        See:
        resource_model: avi.models.resource_model
        """
        if not path:
            self.log.info("Using default RESULTS_PATH")
            path = wh_global_config().get().RESULTS_PATH

        output_file_name = os.path.join(path, name)
        with tarfile.open(output_file_name, "w:gz") as tar:
            tar.add(source, arcname=os.path.basename(source))
        res = os.path.abspath(output_file_name)
        self.log.info("Data saved in: %s", output_file_name)

        try:
            from avi.models import resource_model
            model = resource_model(sort_name = name,
                                   name = name,
                                   path = path,
                                   file_type = task_name,
                                   job_id = id,
                                   date = date)
            model.save()
        except Exception:
            self.log.warning("Something went wrong while updating the db"
                             " saving tmp file to update the db later")
            tmp_path = wh_global_config().get().TMP_PATH
            full_tmp_path = os.path.join(tmp_path, str(id))
            with open(full_tmp_path, "a") as tmp:
                tmp.write("%s;%s;%s;%s;%s"%(name, path, task_name, 
                                               str(id), str(date)))

        return res
