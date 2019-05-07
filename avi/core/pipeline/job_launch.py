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

@package avi.core.pipeline.job_relaunch_algorithm

--------------------------------------------------------------------------------

This module provides the relaunch_algorithm job.
"""
from .job import job as parent

from ast import literal_eval
from avi.models import algorithm_model
from avi.models import gaia_query_model
from avi.models import herschel_query_model
from avi.models import plot_model
from avi.models import results_model
from avi.models import algorithm_info_model
from .job_get_query_info import get_query_info
from .job_get_algorithms import get_algorithms
from .job_get_algorithm_info import get_algorithm_info

from avi.warehouse import wh_frontend_config, wh_global_config

from avi.log import logger

class launch(parent):
    """@class relaunch_algorithm
    The relaunch_algorithm class provides the relaunch_algorithm asynchronous job feature.
    
    It implementes the job interface and inherits the job_data attribute.

    @see job @link avi.core.pipeline.job
    @see job_data @link avi.core.pipeline.job_data
    """
    def start(self, data):
        """This method runs the delete job.

        This method will delete the asynchronous job provided in the data 
        parameter.

        The data parameter must have the key 'pk' containing the primary key of 
        the job to be aborted and the key 'type' containing the type of 
        asynchronous job to be aborted.

        It will first check if the job of the given type and with the given pk 
        exists and if so, it will delete it if the job is aborted or its state 
        is 'SUCCESS' or 'FAILURE'.

        If the type is 'algorithm' it will also delete all the results and 
        plots associated with it.

        Args:
        self: The object pointer.
        data: A dictorianry containing the input data for the job.

        Returns:
        The job_data attribute. The ok attribute will be True if the job has 
        been deleted, False otherwise.
        """
        wh = wh_frontend_config().get()
        gwh = wh_global_config().get()
        log = logger().get_log("views")
        log.info("inside launch job")
        
        
        ret={}
        cont = 0
        ids = []
        data['mission'] = data['id'].split('-')[1]
        data['id'] = data['id'].split('-')[0]
        ret['mission'] = data['mission']
        ret['algorithms'] = {}
        pk={}
        

        #Sacar algorithms
        m = get_algorithms.start(self, None)
        #log.info("bbbbbbbbbbbbbbbbbbbbbbbb"+ str(m.data['algorithms'][1][2]))
        #log.info("bbbbbbbbbbbbbbbbbbbbbbbb"+ str(m.data['algorithms'][1][0]))
        #log.info("bbbbbbbbbbbbbbbbbbbbbbbb"+ str(len(m.data['algorithms'])))
        for i in range(len(m.data['algorithms'])):
            ids.append(m.data['algorithms'][i][0])
        #log.info("bbbbbbbbbbbbbbbbbbbbbbbb"+ str(ids))
        for j in ids:
            pk['id'] = j
            model = get_algorithm_info.start(self, pk)
            #log.info("aaaaaaaaaaaaa"+str(list(model.data['algorithm']['input'].keys())))
            log.info("aaaaaaaaaaaaa"+str(model.data))
            for a in list(model.data['algorithm']['input'].keys()):
                #log.info("cccccccccccccc"+ str(model.data['algorithm']['input'][a]))
                #log.info("cccccccccccccc"+ str(model.data['algorithm']))
                if ret['mission'].lower() == model.data['algorithm']['input'][a]['view_name'].lower():
                    #log.info("cccccccccccccc es HSA")
                    ret['algorithms'][cont] = {}
                    ret['algorithms'][cont]['pk'] = pk['id']
                    ret['algorithms'][cont]['view_name'] = model.data['algorithm']['view_name']
                    log.info(cont)
                    cont = cont + 1

        #Datos para el ret
        data2 = get_query_info.start(self,data)
        data3 = dict(data2.data)
        if 'files' in data3:
            ret['files'] = data3['files']
        else:
            ret['files'] = 'No data found'
        #log.info(data3)
        log.info("return of job_launch: "+str(ret))
        self.job_data.data = ret
        return self.job_data
