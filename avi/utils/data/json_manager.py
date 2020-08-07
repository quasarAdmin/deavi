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
