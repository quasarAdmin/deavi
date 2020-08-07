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

@package avi.core.pipeline.job_get_files

--------------------------------------------------------------------------------

This module provides the get_files job.
"""
import re
from .job import job as parent

from avi.log import logger

import collections

from django.core.paginator import Paginator

from avi.warehouse import wh_frontend_config, wh_global_config
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
    valid_directories = {'results', 'sources', 'hsa', 'gaia', 'sim', 'user'}

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
        gwh = wh_global_config().get()
        
        #dirs = data[0]
        #files = data[1]

        sorting_wh = wh.SORTING_RESOURCES_BY
        if sorting_wh[0] == '-': sorting_wh = sorting_wh[1:]
        order_by = ''
        
        all_files = self.discard_files(resources_manager().get_list(wh.CURRENT_PATH))
        #----------------------------------------------------------------------------------------------------
        #log.info("Current path!!" + str(wh.CURRENT_PATH))
        #log.info("all filess: " + str(all_files))

        gaia_files = self.discard_files(resources_manager().get_list("/data/output/sources/gaia"))
        #log.info("gaia filess: " + str(gaia_files))
        gaia = resources_manager().get_info(gaia_files,"/data/output/sources/gaia")
        #log.info("gaia data: " + str(gaia))

        hsa_files = self.discard_files(resources_manager().get_list("/data/output/sources/hsa"))
        #log.info("hsa filess: " + str(hsa_files))
        hsa = resources_manager().get_info(hsa_files,"/data/output/sources/hsa")
        #log.info("hsa data: " + str(hsa))

        sim_files = self.discard_files(resources_manager().get_list("/data/output/sources/sim"))
        #log.info("hsa filess: " + str(hsa_files))
        sim = resources_manager().get_info(sim_files,"/data/output/sources/sim")
        #log.info("hsa data: " + str(hsa))

        results_files = self.discard_files(resources_manager().get_list("/data/output/results"))
        #log.info("results filess: " + str(results_files))
        results_data = resources_manager().get_info(results_files,"/data/output/results")
        #log.info("results data: " + str(results_data))

        user_files = self.discard_files(resources_manager().get_list("/data/output/user"))
        #log.info("user filess: " + str(user_files))
        user_data = resources_manager().get_info(user_files,"/data/output/user")
        #log.info("user data: " + str(user_data))

        #---------------------------------------------------------------------------------------------------
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
        
        log.info(sorting_wh)
        if sorting_wh == 'size':
            f = collections.OrderedDict(sorted(f.items(), key=lambda x: x[1]))
            d = collections.OrderedDict(sorted(d.items(), key=lambda x: x[1]))
        elif sorting_wh == 'name':
            f = collections.OrderedDict(sorted(f.items(), key=lambda x: x[0]))
            d = collections.OrderedDict(sorted(d.items(), key=lambda x: x[0]))

        #Parse for the filemanager breadcrumb
        p = wh.CURRENT_PATH
        path_to_eliminate = gwh.RESOURCES_PATH
        #path_to_eliminate = re.sub("/results", '', path_to_eliminate) fail
        #p = gwh.RESULTS_PATH
        p = re.sub(path_to_eliminate, '', p)
        #p = path_to_eliminate
        #End parse for the filemanager breadcrumb
        p = p.split("/")


        self.job_data.data = [f, d, p, gaia, hsa, sim, results_data, user_data]
        self.job_data.ok = (pg.num_pages, wh.CURRENT_RESOURCES_PAGE, \
                            wh.CURRENT_RESOURCES_PAGE + 1, wh.CURRENT_RESOURCES_PAGE - 1)
        return self.job_data
