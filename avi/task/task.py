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

@package avi.task.task

--------------------------------------------------------------------------------

This module provides the task, task_data and task_exception classes 
used by all the tasks.
"""
from abc import ABCMeta, abstractmethod

class task_exception(Exception):
    """@class task_exception
    The task_exception class inherits from the Exception class.
    """
    def __init__(self, msg):
        """The task_exception constructor
        
        Args:
        self: The object pointer.
        msg: The exception message.
        """
        self.message = msg

class task_data:
    """@class task_data
    The task_data is an interfal class used by the task class to store all kind 
    of data
    """
    ## The data
    data = None

class task(object):
    """@class task
    An abstract class from which all tasks will inheritance.

    It uses the task_data class to store data.

    @see task_data @link avi.task.task.task_data
    """
    __metaclass__=ABCMeta
    
    ## The task data
    task_data = task_data()
    ## The task id
    task_id = None
    
    @abstractmethod
    def output(self):
        """Deprecated"""
        pass

    @abstractmethod
    def run(self):
        """Abstract method that all the tasks must implement."""
        pass
