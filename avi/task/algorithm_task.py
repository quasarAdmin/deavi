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

@package avi.task.algorithm_task

--------------------------------------------------------------------------------

This module manages the execution of scientific algorithms.

The module manages the execution of python scripts containing the scientific 
algorithms.
"""
import ast

import os
from avi.models import algorithm_info_model

from .task import task as parent
from .task import task_exception as err
from avi.log import logger

class algorithm_task(parent):
    """@class algorithm_task
    The algorithm_task class manages the execution of algorithms.

    It implementes the task interface and inherits the task_data attribute.

    @see task @link avi.task.task.task
    @see task_data @link avi.task.task.task_data
    """
    def output(self):
        """Deprecated"""
        pass

    def __get_data(self, raw):
        """Evalues a raw data structure.
        
        This method is used to evaluate the task_data.data dictionary 
        containing all the input parameters for the algorithm.

        Args:
        self: The object pointer.
        raw: The raw data structure.

        Returns:
        The evaluated structure or None if the raw input is not valid.
        """
        if not raw or raw == "":
            return None
        ret = None
        try:            
            ret = ast.literal_eval(raw)
        except ValueError:
            return None
        except SyntaxError:
            return None
        return ret
    
    def _get_package_str(self, path):
        head, tail = os.path.split(os.path.normpath(path))
        
        if tail == 'avi':
            return 'avi.'
        else:
            return self._get_package_str(head) + tail + "." 

    def run(self):
        """Runs the scientific algorithm.
        
        Loads the scientific algorithm and sets its input parameters contained 
        in the task_data
        
        Args:
        self: The object pointer.
        """
        log = logger().get_log("algorithm_task")
        log.info("running algorithm")

        data = self.__get_data(self.task_data.data)

        if not data:
            log.error("Invalid data provided")
            raise err("Invalid data provided")
            return
        
        try:
            alg_name = data['algorithm']['name']
        except Exception:
            raise err("No algorithm name provided")

        try:
            alg_info = algorithm_info_model.objects.get(name=alg_name)
        except Exception:
            raise err("Inconsistent database")

        try:
            sc_path = alg_info.source_file
        except Exception:
            raise err("No algorithm_info could have been retrieved")

        log.info(sc_path)

        #log.info(os.path.basename(os.path.normpath(sc_path)))
        head, tail = os.path.split(os.path.normpath(sc_path)) 
        #log.info(head)
        #log.info(self._get_package_str(head))

        #package_str = "avi.algorithms." + alg_name
        package_str = self._get_package_str(head) + alg_name
        module_str = alg_name

        log.info("from %s import %s", package_str,module_str)

        # FIXME: 
        mod = __import__(package_str, fromlist=[module_str]) 

        log.info("Getting algorithm obj")
        
        alg = getattr(mod, alg_name)()

        log.info("Filling algorithm params")
        
        for k, v in data['algorithm']['params'].items():
            setattr(alg, k, v)

        log.info("Running algorithm %i", self.task_id)
            
        try:
            alg.run(self.task_id)
        except Exception:
            raise err("Script has issues")
