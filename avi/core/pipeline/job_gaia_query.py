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

@package avi.core.pipeline.job_gaia_query

--------------------------------------------------------------------------------

This module provides the gaia query job.
"""
from .job import job as parent
#from avi.models import TutorialModel #gaia_query_model

# FIXME:
from avi.log import logger
from avi.models import gaia_query_model

class gaia_query(parent):
    """@class gaia_query
    The gaia_query class provides the gaia query asynchronous job feature.
    
    It implementes the job interface and inherits the job_data attribute.

    @see job @link avi.core.pipeline.job
    @see job_data @link avi.core.pipeline.job_data
    """
    def start(self, data):
        """This method runs the gaia query job.

        This method will start an asynchronous query to gaia.

        The data parameter must have the following keys:

        name_coord -> defines if the query is going to be made by coordenates 
        or name.<br>
        name -> if the query is going to be made by name, the object name.<br>
        input_file -> if the query is going to be made with the input of an 
        input file, this will be the path of that input file.<br>
        ra -> the ra.<br>
        dec -> the dec.<br>
        shape -> the shape of the query.<br>
        radius -> the radius of the query.<br>
        width -> the width of the query.<br>
        height -> the height of the query.<br>
        polygon -> an array of coordinates forming a polygon.<br>
        table -> the table of the Gaia Archive to be queried.<br>
        params -> not used at this moment.<br>
        file_name -> the name of the output file.<br>
        adql -> a string with an ADQL query to the archive.<br>

        The method will create a gaia_query_model and save it. By saving the 
        model a gaia_query_task will start asynchronously.

        Args:
        self: The object pointer.
        data: A dictionary containing the input data for the job.

        Returns:
        The job_data attribute. The ok attribute will be True always.

        @see avi.models.gaia_query_model
        @sa avi.task.gaia_query_task
        """
        # TODO:
        #m, created = TutorialModel.objects.get_or_create(fib_num = int(data))
        #gaia_test.delay(data)
        #self.job_data.data = data
        #self.job_data.ok = True
        #return self.job_data
        if data['data_release'] == 'dr1':
            data['table'] = data['table_dr1']
        elif data['data_release'] == 'dr2':
            data['table'] = data['table_dr2']
        m = gaia_query_model(name_coord = data['name_coord'] == "name",
                             name = data['name'],
                             input_file = data['input_file'],
                             ra = float(data['ra']),
                             dec = float(data['dec']),
                             shape = data['shape'],
                             radius = float(data['radius']),
                             width = data['width'] if data['width'] else 0,
                             height = data['height'] if data['height'] else 0  ,
                             polygon = data['polygon'],
                             table = data['table'],
                             params = "",
                             file_name = data['file_name'],
                             adql = data['adql'])
        m.save()
        #TutorialModel.objects.get_or_create(fib_num = int(data))
        self.job_data.data = m
        self.job_data.ok = True
        return self.job_data
