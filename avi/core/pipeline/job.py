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
