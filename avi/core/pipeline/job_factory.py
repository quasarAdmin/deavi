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
            return None
        #return None
        return getattr(mod, name)()
