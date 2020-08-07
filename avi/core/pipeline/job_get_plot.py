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

@package avi.core.pipeline.job_get_plot

--------------------------------------------------------------------------------

This module provides the get_plot job.
"""
from .job import job as parent

from avi.models import plot_model
from avi.log import logger

class get_plot(parent):
    """@class get_plot
    The get_plot class retrieves the plot with the given id.

    It implementes the job interface and inherits the job_data attribute.

    @see job @link avi.core.pipeline.job
    @see job_data @link avi.core.pipeline.job_data
    """
    def start(self, data):
        """This method runs the get_plot job.

        The data parameter must be the primary key of the plot.

        The method will retrieve the plot with the given pk.

        Args:
        self: The object pointer.
        data: A dictorianry containing the input data for the job.

        Returns:
        The job_data attribute. The ok attribute will be True if the plot was 
        retrieved correctly, False otherwise.

        @see plot_model @link avi.models.plot_model
        """
        ms = plot_model.objects.filter(pk=data)
        if not ms:
            self.job_data.ok = False
            self.job_data.data = None
            return self.job_data
        
        ret = {}
        ret['html'] = ms[0].html
        ret['sc'] = ms[0].script
        self.job_data.ok = True
        self.job_data.data = ret
        return self.job_data
