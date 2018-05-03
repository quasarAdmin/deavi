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
"""
from abc import ABCMeta, abstractmethod

class task_exception(Exception):
    def __init__(self, msg):
        self.message = msg

class task_data:
    data = None

class task(object):
    __metaclass__=ABCMeta

    task_data = task_data()
    task_id = None
    
    @abstractmethod
    def output(self):
        pass

    @abstractmethod
    def run(self):
        pass
