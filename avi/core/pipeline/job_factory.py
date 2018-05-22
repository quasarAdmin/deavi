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

@package avi.core.pipeline.job_factory

--------------------------------------------------------------------------------

This module provides the job factory
"""
from avi.log import logger

class job_factory:
    """@class job_factory
    The job_factory creates a job object from the given name and returns it.
    """
    def __init__(self):
        """job_factory constructor
        """
        pass
    
    def get_deavi(self, name):
        """Deprecated"""
        return self.get_job(name, 'deavi')

    def get_avi(self, name):
        """Deprecated"""
        return self.get_job(name,'avi')

    def get_job(self, name, container):
        """Returns the job object.
        
        This method will return the job object created with the given name.

        Args:
        self: The object pointer.
        name: The name of the job to be created.
        container: Deprecated.

        Returns:
        The job object if it does exist, None otherwise.
        """
        #TODO: return None if it does not exist
        # package_str = "avi.core.pipeline." + container + "_job_" + name
        package_str = "avi.core.pipeline.job_" + name
        # module_str = container + "_job_" + name
        module_str = "job_" + name
        
        #package_str = "core.pipeline.job." + container + "_job_" + name
        #package_str = "job.deavi_job_gaia_query"
        logger().get_log('risea').info("Package str : %s - %s",
                                       package_str, module_str)
        logger().get_log('risea').info(__import__(package_str, fromlist=[module_str]))
        mod = __import__(package_str, fromlist=[module_str])
        #mod = __import__("core.pipeline.avi_job_gaia_query",
        #fromlist=['avi_job_gaia_query'])
        if not mod:
            logger().get_log('risea').info("module not loaded")
        #return None
        return getattr(mod, name)()
