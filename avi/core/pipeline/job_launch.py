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

@package avi.core.pipeline.launch

--------------------------------------------------------------------------------

This module provides the launch job.
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
    """@class launch
    The launch class provides the launch asynchronous job feature.
    
    It implementes the job interface and inherits the job_data attribute.

    @see job @link avi.core.pipeline.job
    @see job_data @link avi.core.pipeline.job_data
    """
    def start(self, data):
        """This method runs the launch job.

        This method will launch the asynchronous job provided in the data 
        parameter.

        The data parameter must have the key 'id' containing the primary key of 
        the query and the mission to be launched and the key mission unseted.

        It will first split the key 'id' by '-' and save the primary key into
        data 'id' and the mission into data 'mission'.

        Then it will get all the algorithms and take the valid algorithms
        for the query by comparing the data 'mission' and the inputs of
        the algorithms.

        Finally it will set all the parameters to be returned into
        the 'ret' variable.

        Args:
        self: The object pointer.
        data: A dictorianry containing the input data for the job.

        Returns:
        The the mission. The algorithms. The files of the query
        """
        wh = wh_frontend_config().get()
        gwh = wh_global_config().get()
        log = logger().get_log("launch")
        log.info("inside launch job")
        
        ret={}
        cont = 0
        ids = []
        data['mission'] = data['id'].split('-')[1]
        data['id'] = data['id'].split('-')[0]
        ret['mission'] = data['mission']
        ret['algorithms'] = {}
        pk={}
        

        #Take valid alorithms for the query
        m = get_algorithms.start(self, None)
        #for i in range(len(m.data['algorithms'])):
        #    ids.append(m.data['algorithms'][i][0])
        log.info(m.data)
        for group in m.data['algorithms']:
            for i in group['algorithms']:
                ids.append(i[0])
        for j in ids:
            pk['id'] = j
            model = get_algorithm_info.start(self, pk)
            for a in list(model.data['algorithm']['input'].keys()):
                #if ret['mission'].lower() == model.data['algorithm']['input'][a]['view_name'].lower():
                if ret['mission'].lower() in model.data['algorithm']['input'][a]['type'].lower():
                    ret['algorithms'][cont] = {}
                    ret['algorithms'][cont]['pk'] = pk['id']
                    ret['algorithms'][cont]['view_name'] = model.data['algorithm']['view_name']
                    log.info(cont)
                    cont = cont + 1
                    break

        #Set all the return data
        query_info = get_query_info.start(self,data)
        query_info_data = dict(query_info.data)
        if 'files' in query_info_data:
            ret['files'] = query_info_data['files']
        else:
            ret['files'] = 'No data found'
        log.info("return of job_launch: "+str(ret))
        self.job_data.data = ret
        return self.job_data
