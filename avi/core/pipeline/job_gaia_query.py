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
        # TODO: check errors

        if not 'data_release' in data:
            data['data_release'] = 'dr2'

        if data['data_release'] == 'dr1':
            data['table'] = data['table_dr1']
        elif data['data_release'] == 'dr2':
            data['table'] = data['table_dr2']

        m = gaia_query_model(name_coord = data['name_coord'],
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

        self.job_data.data = m
        self.job_data.ok = True
        return self.job_data
