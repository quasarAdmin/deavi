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

@package avi.core.pipeline.job_get_results

--------------------------------------------------------------------------------

This module provides the get_results job.
"""
from .job import job as parent

from avi.models import results_model
from avi.log import logger

class get_results(parent):
    """@class get_results
    The get_results class retrieves the results of an algorithm execution.

    It implementes the job interface and inherits the job_data attribute.

    @see job @link avi.core.pipeline.job
    @see job_data @link avi.core.pipeline.job_data
    """
    def start(self, data):
        """This method runs the get_results job.

        The data parameter must be the primary key of the algorithm execution.

        The method will retrieve all the resources and plots created by the 
        algorithm execution of the given id.

        Args:
        self: The object pointer.
        data: A dictorianry containing the input data for the job.

        Returns:
        The job_data attribute. The ok attribute will be True if the results 
        were retrieved correctly, False otherwise.

        @see results_model @link avi.models.results_model
        """
        log = logger().get_log("views")
        log.info("%s",str(data))
        ms = results_model.objects.filter(job_id=data)
        if not ms:
            log.info("no results")
            self.job_data.ok = False
            self.job_data.data = None
            return self.job_data
        log.info("results %s",data)
        model = ms[0]
        ret = {}
        plots = {}
        resources = {}
        ret['plots'] = plots
        ret['resources'] = resources
        for p in model.plots.all():
            log.info("%s",str(p.job_id))
            plots[p.pk] = p.pk #(p.script, p.html)
        for r in model.resources.all():
            log.info("%s",str(r.name))
            resources[r.pk] = r.name
        self.job_data.ok = True
        self.job_data.data = ret
        return self.job_data
