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
along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
"""
from avi.log import logger

class job_factory:

    def __init__(self):
        pass
    
    def get_deavi(self, name):
        return self.get_job(name, 'deavi')

    def get_avi(self, name):
        return self.get_job(name,'avi')

    def get_job(self, name, container):

        # package_str = "avi.core.pipeline." + container + "_job_" + name
        package_str = "avi.core.pipeline.job_" + name
        # module_str = container + "_job_" + name
        module_str = "job_" + name
        
        #package_str = "core.pipeline.job." + container + "_job_" + name
        #package_str = "job.deavi_job_gaia_query"
        logger().get_log('risea').info("Package str : %s - %s",
                                       package_str, module_str)
        mod = __import__(package_str, fromlist=[module_str])
        #mod = __import__("core.pipeline.avi_job_gaia_query",
        #fromlist=['avi_job_gaia_query'])
        if not mod:
            logger().get_log('risea').info("module not loaded")
        #return None
        return getattr(mod, name)()
