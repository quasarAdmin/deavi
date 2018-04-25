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
import os
import traceback

from avi.log import logger

from avi.warehouse import wh_global_config
from avi.models import resource_model

class file_manager:
    
    resources_path = ''
    log = None
    def __init__(self):
        self.log = logger().get_log('file_manager')
        #self.date = timezone.now()

    # deprecated
    def __init(self, cfg):
        if not cfg:
            return False
        try:
            self.resources_path = cfg['resources_path']
            return True
        except KeyError:
            return False

    def save(self):
        pass

    def update_db(self):
        pass
    
    def get_file_id(self, path, name):
        resources = resource_model.objects.filter(path=path).filter(name=name)
        if not resources:
            return 0
        self.log.debug(resources[0].id)
        return resources[0].pk

    def save_file_info(self, file_name, id, task_name, date):
        name = os.path.basename(file_name)
        path = os.path.dirname(file_name)
        try:
            from avi.models import resource_model
            model = resource_model(name = name,
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
        res = resource_model.objects.filter(name=name).filter(path=path)
        if not res:
            return
        res.delete()
        os.remove(os.path.join(path, name))
                
    def save_file_plain_data(self, data, name, path = None, 
                             id = "", task_name = "", date = ""):

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
            model = resource_model(name = name,
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
    
    def save_file_binary_data(self, data,name):

        self.resources_path = wh_global_config().get().RESOURCES_PATH
        self.log.info("Saving file in %s", self.resources_path)
        outputFileName = os.path.join(self.resources_path, name)
        outputFile = open(outputFileName, "wb")
        outputFile.write(data)
        outputFile.close()
        path = os.path.abspath(outputFileName)
        self.log.info("Data saved in: %s", outputFileName)
        return path
