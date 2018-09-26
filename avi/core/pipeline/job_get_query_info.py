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

@package avi.core.pipeline.job_get_results

--------------------------------------------------------------------------------

This module provides the get_query_info job.
"""
from .job import job as parent

from avi.models import gaia_query_model
from avi.models import herschel_query_model
from avi.models import resource_model

from avi.log import logger

class get_query_info(parent):
    """@class get_query_info
    The get_query_info class retrieves the information of a query execution.

    It implementes the job interface and inherits the job_data attribute.

    @see job @link avi.core.pipeline.job
    @see job_data @link avi.core.pipeline.job_data
    """
    def start(self, data):
        """This method runs the get_query_info job.

        The data parameter must be a tupla of the primary key of the query 
        execution and an identifier of the mission.

        The method will retrieve all the information of the given query.

        Args:
        self: The object pointer.
        data: A dictorianry containing the input data for the job.

        Returns:
        The job_data attribute. The ok attribute will be True if the 
        information was retrieved correctly, False otherwise.

        @see results_model @link avi.models.results_model
        """
        log = logger().get_log("views")
        log.info("%s",str(data))

        cmodel = gaia_query_model
        file_type = 'gaia'
        if data['mission'] == 'gaia':
            cmodel = gaia_query_model
            file_type = 'gaia'
        elif data['mission'] == 'hsa' or data['mission'] == 'herschel':
            cmodel = herschel_query_model
            file_type = 'hsa'

        qq = cmodel.objects.filter(pk=data['id'])
        if not qq:
            log.warning("No valid id provided")
            self.job_data.ok = False
            self.job_data.data = None
            return self.job_data
        query = qq[0]

        ret = {}
        ret['ra'] = query.ra
        ret['dec'] = query.dec
        ret['radius'] = query.radius
        
        ms = resource_model.objects.filter(file_type=file_type). \
             filter(job_id=data['id'])

        if not ms:
            ret['nofile'] = 'No data found'
        else:
            files = {}
            for r in ms:
                files[r.pk] = r.name

            ret['files'] = files

        self.job_data.ok = True
        self.job_data.data = ret
        return self.job_data

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
