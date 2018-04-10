
from .job import job as parent

from avi.core.algorithm.algorithm_manager import algorithm_manager
from avi.models import algorithm_info_model
from avi.models import resource_model

from avi.log import logger

class get_algorithm_info(parent):
    def start(self, data):
        log = logger().get_log('algorithm_manager')

        #log.info(data)
        
        am = algorithm_info_model.objects.get(pk=data['id'])
        
        if not am:
            self.log_data.ok = False
            return self.job_data

        alg_info = algorithm_manager().get_algorithm(am.definition_file)

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
                                                     'results_files')
        if has_results:
            self.job_data.data['res'] = []

        for i in ms:
            if has_gaia and i.file_type == 'gaia':
                self.job_data.data['gaia'].extend([i.name])
            if has_hsa and i.file_type == 'hsa':
                self.job_data.data['hsa'].extend([i.name])
            if has_results and i.file_type == 'result':
                self.job_data.data['res'].extend([i.name])

        #self.job_data.data = alg_info
        self.job_data.ok = alg_info is not None

        return self.job_data
