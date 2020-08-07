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

        log.info(data)
        
        am = algorithm_info_model.objects.get(pk=data['id'])
        
        if not am:
            self.log_data.ok = False
            return self.job_data

        alg_info = algorithm_manager().get_algorithm(am.definition_file)

        inp = alg_info['algorithm']['input']
        
        #inp = {}

        #inp = sorted(inp.items())
        #inp = sorted(inp, key = lambda x: (x.get('group') is None, x))

        self.job_data.data = dict()
        self.job_data.data['algorithm'] = alg_info['algorithm']
        inp = []
        for _, i in alg_info['algorithm']['input'].items():
            log.info(i)
            inp.append(i)
        inp.sort(key=lambda x: x['position'], reverse=False)
        # self.job_data.data['algorithm_input'] = inp
        self.job_data.data.update({'algorithm_input':inp})
        
        ms = resource_model.objects.all()

        has_gaia = algorithm_manager().has_param_type(am.definition_file,
                                                     'gaia_table')
        if has_gaia:
            # self.job_data.data['gaia'] = []
            self.job_data.data.update({'gaia':[]})
        has_hsa = algorithm_manager().has_param_type(am.definition_file,
                                                     'hsa_table')
        if has_hsa:
            # self.job_data.data['hsa'] = []
            self.job_data.data.update({'hsa':[]})
        log.info(am.definition_file)
        has_results = algorithm_manager().has_param_type(am.definition_file,
                                                     'results_data')
        if has_results:
            # self.job_data.data['res'] = []
            self.job_data.data.update({'res':[]})
        has_user = algorithm_manager().has_param_type(am.definition_file,
                                                      'user_data')
        if has_user:
            # self.job_data.data['user'] = []
            self.job_data.data.update({'user':[]})
            
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
