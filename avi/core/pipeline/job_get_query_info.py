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

        ret = []
        if data['mission'] == 'gaia':
            mytuple = ("type", query.name_coord)
            ret.append(mytuple)
            if query.name_coord == 'file':
                mytuple = ("name", query.name_coord)
                ret.append(mytuple)
            elif query.name_coord == 'adql':
                mytuple = ("adql", query.adql)
                ret.append(mytuple)
            else:
                if query.name_coord == 'name':
                    mytuple = ("name", query.name)
                    ret.append(mytuple)
                else:
                    mytuple = ("ra", query.ra)
                    ret.append(mytuple)
                    mytuple = ("dec", query.dec)
                    ret.append(mytuple)
                if query.shape == 'cone':
                    mytuple = ("shape", query.shape)
                    ret.append(mytuple)
                    mytuple = ("radius", query.radius)
                    ret.append(mytuple)
                elif query.shape == 'box':
                    mytuple = ("shape", query.shape)
                    ret.append(mytuple)
                    mytuple = ("width", query.width)
                    ret.append(mytuple)
                    mytuple = ("height", query.height)
                    ret.append(mytuple)
                elif query.shape == 'polygon':
                    mytuple = ("shape", query.shape)
                    ret.append(mytuple)
                    mytuple = ("polygon", query.polygon)
                    ret.append(mytuple)
                mytuple = ("table", query.table)
                ret.append(mytuple)
        elif data['mission'] == 'hsa' or data['mission'] == 'herschel':
            mytuple = ("type", query.name_coord)
            ret.append(mytuple)
            if query.name_coord == 'file':
                mytuple = ("name", query.name_coord)
                ret.append(mytuple)
            elif query.name_coord == 'adql':
                mytuple = ("adql", query.adql)
                ret.append(mytuple)
            else:
                if query.name_coord == 'name':
                    mytuple = ("name", query.name)
                    ret.append(mytuple)
                else:
                    mytuple = ("ra", query.ra)
                    ret.append(mytuple)
                    mytuple = ("dec", query.dec)
                    ret.append(mytuple)
                if query.shape == 'cone':
                    mytuple = ("shape", query.shape)
                    ret.append(mytuple)
                    mytuple = ("radius", query.radius)
                    ret.append(mytuple)
                elif query.shape == 'box':
                    mytuple = ("shape", query.shape)
                    ret.append(mytuple)
                    mytuple = ("width", query.width)
                    ret.append(mytuple)
                    mytuple = ("height", query.height)
                    ret.append(mytuple)
                elif query.shape == 'polygon':
                    mytuple = ("shape", query.shape)
                    ret.append(mytuple)
                    mytuple = ("polygon", query.polygon)
                    ret.append(mytuple)
                if query.positional_images == False:
                    mytuple = ("positional_images", query.positional_images)
                    ret.append(mytuple)
                elif query.positional_images == True:
                    mytuple = ("instrument", query.instrument)
                    ret.append(mytuple)
                    mytuple = ("level", query.level)
                    ret.append(mytuple)
                    mytuple = ("params", query.params)
                    ret.append(mytuple)
                
                mytuple = ("table", query.table)
                ret.append(mytuple)
        '''
        ret = {}
        if data['mission'] == 'gaia':
            if query.name_coord == 'file':
                ret['name'] = query.name_coord
            elif query.name_coord == 'adql':
                ret['adql'] = query.adql
            else:
                if query.name_coord == 'name':
                    ret['name'] = query.name
                else:
                    ret['ra'] = query.ra
                    ret['dec'] = query.dec
                if query.shape == 'cone':
                    ret['radius'] = query.radius
                    ret['shape'] = query.shape
                elif query.shape == 'box':
                    ret['height'] = query.height
                    ret['width'] = query.width
                    ret['shape'] = query.shape
                elif query.shape == 'polygon':
                    ret['polygon'] = query.polygon
                    ret['shape'] = query.shape
                ret['table'] = query.table
        ret['type'] = query.name_coord
        '''
        ms = resource_model.objects.filter(file_type=file_type). \
             filter(job_id=data['id'])

        if not ms:
            #ret['nofile'] = 'No data found'
            mytuple = ("nofile", "No data found")
            ret.append(mytuple)
        else:
            files = {}
            for r in ms:
                files[r.pk] = r.name

            #ret['files'] = files
            mytuple = ("files", files)
            ret.append(mytuple)
        log.info("%s",str(ret))
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
