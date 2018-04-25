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
from .job import job as parent

from avi.log import logger
from avi.models import algorithm_model
from avi.models import algorithm_info_model
from avi.core.algorithm.algorithm_manager import algorithm_manager

class algorithm(parent):

    def start(self, data):

        log = logger().get_log("algorithm_task")
        log.info("job %s", data)
        if "algorithm_id" in data:

            mng = algorithm_manager()

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
