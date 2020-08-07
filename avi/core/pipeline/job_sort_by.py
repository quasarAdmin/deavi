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

@package avi.core.pipeline.job_sort_by

--------------------------------------------------------------------------------

This module provides the sort_by job.
"""
from .job import job as parent

from avi.log import logger
from avi.warehouse import wh_frontend_config

class sort_by(parent):
    """@class sort_by
    The sort_by class changes the current sorting method to the given method.
    
    It implementes the job interface and inherits the job_data attribute.

    @see job @link avi.core.pipeline.job
    @see job_data @link avi.core.pipeline.job_data
    """
    def are_equal(self, str1, str2):
        """This method checks if two methods are equal
        
        It ignores the '-' character which defines has to be sorting descending.

        Args:
        self: The object pointer.
        str1: The first sorting method to compare.
        str2: The second sorting method to compare.

        Returns:
        True if str1 and str2 are equal.
        """
        return str1.replace('-','',1) == str2

    def invert(self, string):
        """This method inverts a sorting method.
        
        This method inverts a sorting method from ascending to descending or 
        vice versa.

        Args:
        self: The object pointer.
        string: The method to be inverted.

        Returns:
        The inverted sorting method.
        """
        if string[0] == '-':
            return string[1:]
        else:
            return "-" + string

    def start(self, data):
        """This method runs the sorting_by job.

        This methods changes the current sorting method storaged in the 
        wh_frontend_config warehouse.

        The data parameter must have the key 'page' containing the name of 
        the web page whose sorting method will change. It must have also the 
        key 'sort_by' with the sorting method to be changed with.

        Here we just change the current sorting method in the warehouse, 
        without checking if it is valid or not. Those error controls will be 
        made in other jobs.

        Args:
        self: The object pointer.
        data: A dictorianry containing the input data for the job.

        Returns:
        The job_data attribute. The ok attribute will be True always.

        @see wh_frontend_config @link avi.warehouse.wh_frontend_config
        """
        wh = wh_frontend_config().get()

        if data['page'] == "pipeline_status":
            if self.are_equal(wh.SORTING_EXEC_BY, data['sort_by']):
                wh.SORTING_EXEC_BY = self.invert(wh.SORTING_EXEC_BY)
            else:
                wh.SORTING_EXEC_BY = data['sort_by']

        elif data['page'] == "query_status":
            if self.are_equal(wh.SORTING_QUERY_BY, data['sort_by']):
                wh.SORTING_QUERY_BY = self.invert(wh.SORTING_QUERY_BY)
            else:
                wh.SORTING_QUERY_BY = data['sort_by']

        elif data['page'] == "algorithm":
            if self.are_equal(wh.SORTING_ALG_BY, data['sort_by']):
                wh.SORTING_ALG_BY = self.invert(wh.SORTING_ALG_BY)
            else:
                wh.SORTING_ALG_BY = data['sort_by']

        elif data['page'] == "resources":
            if self.are_equal(wh.SORTING_RESOURCES_BY, data['sort_by']):
                wh.SORTING_RESOURCES_BY = self.invert(wh.SORTING_RESOURCES_BY)
            else:
                wh.SORTING_RESOURCES_BY = data['sort_by']

        elif data['page'] == "results":
            if self.are_equal(wh.SORTING_RESULTS_BY, data['sort_by']):
                wh.SORTING_RESULTS_BY = self.invert(wh.SORTING_RESULTS_BY)
            else:
                wh.SORTING_RESULTS_BY = data['sort_by']

        self.job_data.data = {}
        self.job_data.ok = True
        return self.job_data
