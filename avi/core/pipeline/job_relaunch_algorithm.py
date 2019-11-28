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

from avi.warehouse import wh_frontend_config, wh_global_config

from avi.log import logger

class relaunch_algorithm(parent):
    """@class relaunch_algorithm
    The relaunch_algorithm class provides the relaunch_algorithm asynchronous job feature.
    
    It implementes the job interface and inherits the job_data attribute.

    @see job @link avi.core.pipeline.job
    @see job_data @link avi.core.pipeline.job_data
    """
    def start(self, data):
        """This method runs the relaunch_algorithm job.

        This method will relaunch_algorithm the asynchronous job provided in the data 
        parameter.

        The data parameter must have the key 'algorithm' containing all the data of 
        the algorithm to be relaunched.

        It will first parse the data parameter to a dictionary and
        save it into 'qparams' variable, then get the algorithm model
        by the name in the 'qparams' variable and save the 'pk' of the
        algorithm into 'qparams.

        If the algorithm input parameters contains 'Gaia' then
        will set the gaia file, if contains 'HSA' then will
        set the hsa file.

        Args:
        self: The object pointer.
        data: A dictorianry containing the input data for the job.

        Returns:
        The algorithm parameters to be relaunched.
        """
        wh = wh_frontend_config().get()
        gwh = wh_global_config().get()

        log = logger().get_log("relaunch")
        log.info("inside relaunch_algorithm job")
        # data is a string type, transform to dictionary
        qparams = literal_eval(data['pk'])
        # get the model of the algorithm by the name in qparams
        m = algorithm_info_model.objects.get(name=qparams['algorithm']['name'])
        # add the pk of the algorithm
        qparams['algorithm']['pk'] = m.pk
        # get the keys of the algorithm parameters
        keys = qparams['algorithm']['params'].keys()
        # check if Gaia or HSA is one of the parameters to delete de path of the files
        if "Gaia" in keys:
            path_to_eliminate = gwh.SOURCES_PATH
            path_to_eliminate = str(path_to_eliminate) + "/gaia/"
            qparams['algorithm']['params']['Gaia'] = qparams['algorithm']['params']['Gaia'].replace(path_to_eliminate, '')
            log.info(qparams['algorithm']['params']['Gaia'])
            #Delete path
        if "HSA" in keys:
            path_to_eliminate = gwh.SOURCES_PATH
            path_to_eliminate = str(path_to_eliminate) + "/hsa/"
            qparams['algorithm']['params']['HSA'] = qparams['algorithm']['params']['HSA'].replace(path_to_eliminate, '')
            log.info(qparams['algorithm']['params']['HSA'])
            #Delete path


        data = {}

        self.job_data.data = qparams['algorithm']
        log.info("params " + str(qparams['algorithm']))
        return self.job_data
