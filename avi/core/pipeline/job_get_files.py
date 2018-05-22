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

@package avi.core.pipeline.job_get_files

--------------------------------------------------------------------------------

This module provides the get_files job.
"""
from .job import job as parent

from avi.log import logger

from django.core.paginator import Paginator

from avi.warehouse import wh_frontend_config
from avi.utils.resources_manager import resources_manager
from avi.models import resource_model

class get_files(parent):
    """@class get_files
    The get_files class retrieves the names of the files and directories in the 
    current path.

    It implementes the job interface and inherits the job_data attribute.

    @see job @link avi.core.pipeline.job
    @see job_data @link avi.core.pipeline.job_data
    """
    ## The directories that must not be discarted.
    valid_directories = {'results', 'sources', 'hsa', 'gaia', 'user'}

    def discard_files(self, files):
        """This methods discards or the files and directories that must not be 
        shown.

        If a directory is not in the valid_directories attribute or a file is 
        not a resource_model then it will discarted and it will not be show.

        Args:
        self: The object pointer.
        files: The files and directories of the current path.

        Returns:
        The files and directories to be shown.

        @see resource_model @link avi.models.resource_model
        """
        res = []
        db_resources = resource_model.objects.all()
        for f in files:
            if f in self.valid_directories or resource_model.objects.filter(name=f):
                res.append(f)
        return res

    def start(self, data):
        """This method runs the get_files job.

        This method will retrieve all the allowed files and directories to be 
        shown in the user interface.
        
        It uses the resources_manager to get the path information and then uses 
        the discard_files to discard the ones that should not be shown.

        After that it will paginate the results with the current page retrieved 
        from the wh_frontend_config warehouse.

        Args:
        self: The object pointer.
        data: A dictorianry containing the input data for the job.

        Returns:
        The job_data attribute. The ok attribute provides the pages information.

        @see resources_manager @link avi.utils.resources_manager.resources_manager
        @see wh_frontend_config @link avi.warehouse.wh_frontend_config
        """
        log = logger().get_log("views")
        
        wh = wh_frontend_config().get()
        
        #dirs = data[0]
        #files = data[1]

        sorting_wh = wh.SORTING_RESOURCES_BY
        order_by = ''
        
        all_files = self.discard_files(resources_manager().get_list(wh.CURRENT_PATH))

        all_files.sort()

        pg = Paginator(all_files, wh.MAX_RESOURCES_PER_PAGE)
        page = wh.CURRENT_RESOURCES_PAGE
        if page < 1:
            wh.CURRENT_RESOURCES_PAGE = 1
        elif page > pg.num_pages:
            wh.CURRENT_RESOURCES_PAGE = pg.num_pages

        files = pg.page(wh.CURRENT_RESOURCES_PAGE)

        f, d = resources_manager().get_info(files,wh.CURRENT_PATH)

        log.info(f)
        
        self.job_data.data = [f, d]
        self.job_data.ok = (pg.num_pages, wh.CURRENT_RESOURCES_PAGE, \
                            wh.CURRENT_RESOURCES_PAGE + 1, wh.CURRENT_RESOURCES_PAGE - 1)
        return self.job_data
