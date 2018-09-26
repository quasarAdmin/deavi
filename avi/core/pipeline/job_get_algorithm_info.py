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

@package avi.core.pipeline.job_get_algorithm_info

--------------------------------------------------------------------------------

This module provides the get_algorithm_info job.
"""
from .job import job as parent

from avi.core.algorithm.algorithm_manager import algorithm_manager
from avi.models import algorithm_info_model
from avi.models import resource_model

from avi.log import logger

class get_algorithm_info(parent):
    """@class get_algorithm_info
    The get_algorithm_info retrieves the algorithm information.

    It implementes the job interface and inherits the job_data attribute.

    @see job @link avi.core.pipeline.job
    @see job_data @link avi.core.pipeline.job_data
    """
    def start(self, data):
        """This method retrieves the algorithm information.

        The data parameter must have the key 'id' containing the algorithm id 
        which info will be retrieved.

        The method will retrieve the algorithm_info_model with the given id and 
        it will will extract the parameters information from the definition 
        file provided by the algorithm_info_model.

        If the algorithm has gaia, herschel or results files in its input, this 
        method will also retrieve the names of thouse files from the 
        resource_model.

        Args:
        self: The object pointer.
        data: A dictorianry containing the input data for the job.

        Returns:
        The job_data attribute. The ok attribute will be True if the algorithm 
        exists, False otherwise.

        @see algorithm_info_model @link avi.models.algorithm_info_model
        @see resource_model @link avi.models.resource_model
        """
        log = logger().get_log('algorithm_manager')

        #log.info(data)
        
        am = algorithm_info_model.objects.get(pk=data['id'])
        
        if not am:
            self.log_data.ok = False
            return self.job_data

        alg_info = algorithm_manager().get_algorithm(am.definition_file)

        inp = alg_info['algorithm']['input']
        
        #inp = {}

        #inp = sorted(inp.items())
        #inp = sorted(inp, key = lambda x: (x.get('group') is None, x))

        self.job_data.data = {}
        self.job_data.data['algorithm'] = alg_info['algorithm']
        
        ms = resource_model.objects.all()

        has_gaia = algorithm_manager().has_param_type(am.definition_file,
                                                     'gaia_table')
        if has_gaia:
            self.job_data.data['gaia'] = []
        has_hsa = algorithm_manager().has_param_type(am.definition_file,
                                                     'hsa_table')
        if has_hsa:
            self.job_data.data['hsa'] = []
        has_results = algorithm_manager().has_param_type(am.definition_file,
                                                     'results_data')
        if has_results:
            self.job_data.data['res'] = []
        has_user = algorithm_manager().has_param_type(am.definition_file,
                                                      'user_data')
        if has_user:
            self.job_data.data['user'] = []
            
        for i in ms:
            log.info("file %s - %s", i.name, i.file_type)
            if has_gaia and i.file_type == 'gaia':
                self.job_data.data['gaia'].extend([i.name])
            if has_hsa and i.file_type == 'hsa':
                self.job_data.data['hsa'].extend([i.name])
            if has_results and i.file_type == 'result':
                self.job_data.data['res'].extend([i.name])
            if has_user and i.file_type == 'user':
                self.job_data.data['user'].extend([i.name])

        #self.job_data.data = alg_info
        self.job_data.ok = alg_info is not None

        return self.job_data
