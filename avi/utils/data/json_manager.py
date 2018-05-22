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

@package avi.utils.data.json_manager

--------------------------------------------------------------------------------

This module provides the json files management
"""
import json

from avi.log import logger

class json_manager:
    """@class json_manager
    This class provides the json files management
    """
    ## The json file root
    json_root = None
    
    def __init__(self):
        """Constructor
        
        Initializes the log
        """
        self.log = logger().get_log('json_manager')

    def load(self, file_name):
        """Load a given json file

        Reads a given json file and stores the root into the json_root 
        attribute

        Args:
        self: The object pointer
        file_name: The json file name
        """
        data = open(file_name)
        self.json_root = json.load(data)
        data.close()

    def get(self, key):
        """Retrieves the value of a given key

        If there is not a json loaded returns None. 
        
        If the key does not exists in the json loaded returns None.
        
        Otherwise it will return the value of the given key

        Args:
        self: The object pointer
        key: The key of the value to be returned

        Returns:
        The value of the given key if everything goes correctly, None otherwise
        """
        if not self.json_root:
            self.log.error('There is no json loaded')
            return None
        data = self.json_root.get(key)
        if not data:
            ret = []
            for v in self.json_root:
                self._get_from_dict(key,self.json_root[v], ret)
            return ret
        else:
            return data

    def read_gaia_input(self, file_name):
        """Reads an input file with queries to the Gaia archive.

        This method is used to read an input file containing queries to the 
        Gaia archive. It returns an array with all the queries read

        Args:
        self: The object pointer
        file_name: The name of the input file

        Returns:
        An array with the queries information
        """
        self.load(file_name)
        c = 1
        ret = []
        data = self.get("source_%i"%(c))
        while data != None and data != []:
            ret += data
            c += 1
            data = self.get("source_%i"%(c))
        return ret

    def read_herschel_input(self, file_name):
        """Reads an input file with queries to the Herschel archive.

        This method is used to read an input file containing queries to the 
        Herschel archive. It returns an array with all the queries read

        Args:
        self: The object pointer
        file_name: The name of the input file

        Returns:
        An array with the queries information
        """
        self.load(file_name)
        c = 1
        ret = []
        data = self.get("source_%i"%(c))
        while data != None and data != []:
            ret += data
            c += 1
            data = self.get("source_%i"%(c))
        return ret

    def get_vertexes(self, data):
        """Returns an array of vertexes

        With the give data, this method will read the data and return an array 
        with the vertexes information contained in the data

        Args:
        self: The object pointer
        data: The data to be read

        Returns:
        An array with the vertexes information contained in the given data
        """
        c = 1
        v = data.get("vertex_%i"%(c))
        ret = []
        while v != None:
            c += 1
            ret += [{'ra': v['ra'], 'dec': v['dec']}]
            v = data.get("vertex_%i"%(c))
        return ret
        
    def set_vertexes(self, data, vertexes):
        """Stores the vertexes in a dictionary format
        
        With the given string containing the vertexes information, this method 
        will store them into the given json data

        The vertexes contained in the string must be separeted with the 
        character ', ' and each pair of vertexes must have the separtor ' '

        Args:
        self: The object pointer
        data: The data into which the vertexes are going to be stored
        vertexes: The string containing the vertexes information
        """
        def set_vertex(pair, data, num):
            ps = ' ' # pair separator
            v = {}
            v['ra'] = pair[:pair.find(ps)]
            v['dec'] = pair[pair.find(ps)+len(ps):]
            data["vertex_"+str(num)] = v

        vs = ', ' # vertex separator
        cont = 1
        while (vertexes.find(vs)) > -1:
            pair = vertexes[:vertexes.find(vs)]
            set_vertex(pair, data, cont)
            vertexes = vertexes[vertexes.find(vs)+len(vs):]
            cont += 1
        set_vertex(vertexes, data, cont)
    
    def _get_from_dict(self, key, d = None, ret = None):
        if not d or ret == None:
            return None
        if not isinstance(d,dict):
            self.log.info('This is a leaf')
            return None
        data = d.get(key)
        if not data:
            for v in d:
                self._get_from_dict(key, d[v], ret)
        else:
            ret+=[data]
