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

@package avi.core.pipeline.job_get_resources

--------------------------------------------------------------------------------

This module provides the get_resources job.
"""
from .job import job as parent

from avi.models import resource_model
from avi.warehouse import wh_global_config as wh
from avi.log import logger

class get_resources(parent):
    """@class get_resources
    The get_resources class retrieves the resources.

    It implementes the job interface and inherits the job_data attribute.

    @see job @link avi.core.pipeline.job
    @see job_data @link avi.core.pipeline.job_data
    """
    def start(self, data):
        """This method runs the get_resources job.

        The method will retrieve all the resource_models.

        Args:
        self: The object pointer.
        data: A dictorianry containing the input data for the job.

        Returns:
        The job_data attribute. The ok attribute will be always True.

        @see resource_model @link avi.models.resource_model
        """
        ms = resource_model.objects.all()
        data = {}
        gaia = {}
        hsa = {}
        data['gaia'] = gaia
        data['hsa'] = hsa
        for q in ms:
            if q.file_type == 'gaia':
                gaia[q.name] = q.name
            elif q.file_type == 'hsa':
                hsa[q.name] = q.name
        self.job_data.ok = True
        self.job_data.data = data
        return self.job_data
