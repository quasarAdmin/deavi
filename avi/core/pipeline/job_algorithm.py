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

@package avi.core.pipeline.job_algorithm

--------------------------------------------------------------------------------

This module provides the algorithm job.
"""
from .job import job as parent

from avi.log import logger
from avi.models import algorithm_model
from avi.models import algorithm_info_model
from avi.core.algorithm.algorithm_manager import algorithm_manager

class algorithm(parent):
    """@class algorithm
    The algorithm class starts an algorithm asynchronously.
    
    It implementes the job interface and inherits the job_data attribute.

    @see job @link avi.core.pipeline.job
    @see job_data @link avi.core.pipeline.job_data
    """
    def start(self, data):
        """This method runs the algorithm job.

        This method will start an algorithm asynchronously.

        The data parameter must have the key 'algorithm_id' containing the 
        algorithm id to be started. 

        The method will retrieve an algorithm_info_model with the given id 
        and it will create an algorithm_model and save it. By saving the model 
        a algorithm_task will start asynchronously.

        Args:
        self: The object pointer.
        data: A dictorianry containing the input data for the job.

        Returns:
        The job_data attribute. The ok attribute will be True if the algorithm 
        has started, False otherwise.

        @see algorithm_info_model @link avi.models.algorithm_info_model
        @see algorithm_model @link avi.models.algorithm_model
        @see algorithm_task @link avi.task.algorithm_task
        """
        log = logger().get_log("algorithm_task")
        log.info("job %s", data)
        if "algorithm_id" in data:

            mng = algorithm_manager()
            
            if not data.get('algorithm_id'):
                self.job_data.ok = False
                return self.job_data

            if len(data['algorithm_id']) < 1:
                self.job_data.ok = False
                return self.job_data

            alg = algorithm_info_model.objects.get(pk=data['algorithm_id'][0])

            result = mng.get_algorithm_data(data['algorithm_id'][0],
                                            alg.name,
                                            alg.definition_file,
                                            data)
            
            m = algorithm_model(alg_name = alg.name,
                                params = result,
                                results = result)
            m.save()
            self.job_data.data = m
            self.job_data.ok = True
            return self.job_data
            
        # OLD
        m = algorithm_model(alg_name = data['algorithm']['name'],
                            params = data,
                            results = data)
        m.save()
        #log.info("model %s", str(m))
        self.job_data.data = m
        self.job_data.ok = True
        return self.job_data
