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

@package avi.core.pipeline.job

--------------------------------------------------------------------------------

This module provides the job and job_data classes.
"""
from abc import ABCMeta, abstractmethod

class job_data:
    """@class job_data
    The job_data is an internal class used by the job class to store all kind 
    of data
    """
    ## The data
    data = None
    ## True if the job was started correctly, False otherwise
    ok = False

class job(object):
    """@class job
    An abstract class from which all jobs will inheritance.
    
    It uses the job_data class to store data.

    @see job_data @link avi.core.pipeline.job.job_data
    """
    __metaclass__=ABCMeta

    ## the job data
    job_data = job_data()
    
    @abstractmethod
    def start(self, data):
        """Abstract method that all the jobs must implement.
        """
        pass
