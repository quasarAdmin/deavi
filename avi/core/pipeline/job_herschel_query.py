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

@package avi.core.pipeline.job_herschel_query

--------------------------------------------------------------------------------

This module provides the herschel_query job.
"""
from .job import job as parent

from avi.models import herschel_query_model

class herschel_query(parent):
    """@class herschel_query
    The herschel_query class provides the herschel query asynchronous job 
    feature.
    
    It implementes the job interface and inherits the job_data attribute.

    @see job @link avi.core.pipeline.job
    @see job_data @link avi.core.pipeline.job_data
    """
    def start(self,data):
        """This method runs the heschel_query job.

        This method will start an asynchronous query to herschel.

        The data parameter must have the following keys:
        name_coord -> defines if the query is going to be made by coordenates 
        or name.
        name -> if the query is going to be made by name, the object name.
        input_file -> if the query is going to be made with the input of an 
        input file, this will be the path of that input file.
        ra -> the ra.
        dec -> the dec.
        shape -> the shape of the query.
        radius -> the radius of the query.
        width -> the width of the query.
        height -> the height of the query.
        polygon -> an array of coordinates forming a polygon.
        positional_images -> defines if the query must be done in the 
        positional sources catalog or the images.
        table -> the table of the Gaia Archive to be queried.
        instrument -> defines the instrument.
        level -> defines the processing level.
        params -> not used at this moment.
        file_name -> the name of the output file.
        adql -> a string with an ADQL query to the archive.

        The method will create a hershcel_query_model and save it. By saving 
        the model a herschel_query_task will start asynchronously.

        Args:
        self: The object pointer.
        data: A dictionary containing the input data for the job.

        Returns:
        The job_data attribute. The ok attribute will be True always.

        @see herschel_query_model @link avi.models.herschel_query_model
        @see herschel_query_task @link avi.task.herschel_query_task
        """
        m = herschel_query_model(name_coord = data['name_coord'],
                                 name = data['name'], #if data['name'] != "" \
                                 #else None,
                                 input_file = data['input_file'],
                                 ra = data['ra'],
                                 dec = data['dec'],
                                 shape = data['shape'],
                                 radius = data['radius'],
                                 width = data['width'] if data['width'] else 0,
                                 height = data['height'] if data['height'] else 0  ,
                                 polygon = data['polygon'],#if data['polygon']!="" \
                                 #else None,
                                 positional_images = \
                                 data['positional_images'] == "images",
                                 table = data['table'],
                                 instrument = data['instrument'],
                                 level = data['level'],
                                 params = "",
                                 file_name = data['file_name'],
                                 adql = data['adql'])
        m.save()
        self.job_data.data = m
        self.job_data.ok = True
        return self.job_data
