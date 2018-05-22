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
