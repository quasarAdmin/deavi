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
import json

from avi.log import logger

class json_manager:

    json_root = None
    
    def __init__(self):
        self.log = logger().get_log('json_manager')

    def load(self, file_name):
        data = open(file_name)
        self.json_root = json.load(data)
        data.close()

    def get(self, key):
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
        c = 1
        v = data.get("vertex_%i"%(c))
        ret = []
        while v != None:
            c += 1
            ret += [{'ra': v['ra'], 'dec': v['dec']}]
            v = data.get("vertex_%i"%(c))
        return ret
        
    def set_vertexes(self, data, vertexes):
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
