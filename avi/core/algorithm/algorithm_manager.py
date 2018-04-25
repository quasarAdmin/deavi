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
along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
"""
import os

from avi.log import logger
from avi.warehouse import wh_frontend_config, wh_global_config
from avi.utils.data.json_manager import json_manager
from avi.warehouse import wh_global_config as wh
from avi.models import algorithm_info_model

class algorithm_manager:

    str_log_header = 'algorithm_manager'
    log = None

    def __init__(self):
        self.log = logger().get_log(self.str_log_header)

    def __sort_dict(self, d):
        #sorted_index = sorted(d, key=lambda x: data[x][1], reverse=True)
        return d
    
    def update_database(self, path, alg_type):
        # read folder
        alg = {}
        for f in os.listdir(path):
            if not f.endswith(".json"):
                continue
            name, fext = os.path.splitext(f)
            name_src = name+".py"
            if not os.path.isfile(os.path.join(path,name_src)):
                continue
            alg[name] = { "name": name,
                          "name_view": self.get_info(os.path.join(path, f),
                                                     "view_name"),
                          "src": os.path.join(path,name_src),
                          "json": os.path.join(path,f),
                          "type": alg_type }
        # check and add new ones
        #self.log.info(alg)
        for name in alg:
            #self.log.info(str(alg[name]))
            m = algorithm_info_model.objects.all().filter(name=name)
            #self.log.info("after query %s", str(m))
            #self.log.info("after query")
            if not m:
                self.log.info("not m")
                a = alg[name]
                m = algorithm_info_model(name=a["name"],
                                         source_file=a["src"],
                                         name_view=a["name_view"],
                                         definition_file=a["json"],
                                         algorithm_type=a["type"])
                m.save()

    def init(self):
        alg_m = algorithm_info_model.objects.all()
        
        for a in alg_m:
            if a.algorithm_type == "temporal":
                a.delete()

        self.update_database(wh_global_config().get().ALGORITHM_PATH, 
                             "installed")
        self.log.info(wh_global_config().get().UPLOADED_ALGORITHM_PATH)
        self.update_database(wh_global_config().get().UPLOADED_ALGORITHM_PATH,
                             "uploaded")

    def get_algorithm(self, json_file):
        jm = json_manager()
        jm.load(json_file)
        if not self.__check_json(jm.json_root):
            self.log.error("Not valid json file")
            return None
        return jm.json_root

    def get_info(self, json, key):
        jm = json_manager()
        jm.load(json)
        if not self.__check_json(jm.json_root):
            self.log.error("Not algorithm 2")
            return None
        return jm.json_root['algorithm'][key]

    def has_param_type(self, json, param_type):
        jm = json_manager()
        jm.load(json)
        if not self.__check_json(jm.json_root):
            self.log.error("Not valid json file")
            return None
        aux = jm.json_root['algorithm']['input']
        for k in aux:
            input_type = aux[k]['type']
            if input_type == param_type:
                return True
        return False

    def get_algorithm_data(self, alg_id, name, def_file, post):
        
        jm = json_manager()
        if not os.path.isfile(def_file):
            self.log.error("Not algorithm 1")
            return None
        jm.load(def_file)
        if not self.__check_json(jm.json_root):
            self.log.error("Not algorithm 2")
            return None
        ret = {"algorithm":{}}
        alg = ret['algorithm']
        alg['name'] = name
        alg['params'] = {}
        params = alg['params']
        for k, v in jm.json_root['algorithm']['input'].items():
            param_name = v['name']
            post_name = alg_id +"_"+ param_name
            self.log.info("param_name %s post_name %s data %s",
                           param_name,post_name,"")
            params[param_name] = self.__get_data(post[post_name][0],
                                                 v['type'])
        return ret

    def get_algorithm_info(self, data):
        self.log.debug(str(data))
        if not "algorithm" in data.keys():
            self.log.error("Not algorithm")
            return None

        path = wh_global_config().get().ALGORITHM_PATH
        jm = json_manager()
        alg_name = str(data['algorithm'][0])
        self.log.debug("Algoritm name %s", alg_name)
        if not os.path.isfile(path + alg_name + ".json"):
            self.log.error("Not algorithm 1")
            return None
        jm.load(path + alg_name + ".json")
        if not self.__check_json(jm.json_root):
            self.log.error("Not algorithm 2")
            return None

        ret = {"algorithm":{}}
        alg = ret['algorithm']
        alg['name'] = alg_name
        alg['params'] = {}
        params = alg['params']
        for k, v in jm.json_root['algorithm']['input'].items():
            param_name = v['name']
            post_name = alg_name +"_"+ k
            self.log.debug("param_name %s post_name %s data %s",
                           param_name,post_name,"")
            params[param_name] = self.__get_data(data[post_name][0],
                                                 v['type'])
            
        data2 = {"algorithm":{
            "name":"dummy_algorithm",
            "params":{
                "param1": 1.0,#"float",
                "param2": 2.0,#"float",
            },
        }}
        return ret

    def get_algorithm_list(self):
        num_alg = wh_frontend_config().get().MAX_ALG_PER_PAGE
        current_page = wh_frontend_config().get().CURRENT_ALG_PAGE

        path = wh_global_config().get().ALGORITHM_PATH
        self.log.info("Reading algorithms data from %s", path)
        data = {}
        jm = json_manager()
        for f in os.listdir(path):
            if not f.endswith(".json"):
                continue
            self.log.info("File %s", f)
            name, fext = os.path.splitext(f)
            name = name+".py"
            self.log.info("Checking file %s", name)
            if not os.path.isfile(path + name):
                continue
            self.log.info("Algorithm file found, reading data file now")
            jm.load(path + f)
            self.log.info("Data loaded: %s", jm.json_root)
            if not self.__check_json(jm.json_root):
                continue
            self.log.info("JSON checked correctly")
            alg_name = jm.json_root['algorithm']['name']
            data[alg_name] = jm.json_root['algorithm']
        
        data2 = {"alg_data":{
            "alg_1":
            {
                "input":{
                    "input_1":{
                        "name":"table name",
                        "type":"table"
                    },
                    "input_2":{
                        "name":"float name",
                        "type":"float"
                    }
                },
                "name" : "algorithm 1",
            },
            "alg_2":{
                "input":{
                    "input_1":{
                        "name":"bool name",
                        "type":"bool"
                    },
                    "input_2":{
                        "name":"float name",
                        "type":"float"
                    }
                },
                "name": "asdf 2",            
            }
        }}
        ret = {"alg_data": data}
        return ret
        return self.__sort_dict(data)

    def __check_json(self, data):
        if not "algorithm" in data.keys():
            return False

        alg = data['algorithm']
        #self.log.info(str(alg))

        if not "name" in alg.keys():
            return False

        if not "view_name" in alg.keys():
            alg["view_name"] = alg["name"]

        if not "input" in alg.keys():
            return False

        ainput = alg["input"]

        #self.log.info(str(ainput))
        
        for k,v in ainput.items():
            if not "name" in v.keys():
                return False
            if not "view_name" in v.keys():
                v["view_name"] = v["name"]
            if not "type" in v.keys():
                return False
        
        return True

    def __get_data(self, data, data_type):
        ret = ""
        if data_type == "float":
            try:
                ret = float(data)
                return ret
            except ValueError:
                return ""

        if data_type == "string":
            return data
        
        if  data_type == "gaia_table":
            return os.path.join(wh().get().GAIA_PATH, data)

        if data_type == "hsa_table" or data_type == "hsa_fits":
            return os.path.join(wh().get().HSA_PATH, data)

        if data_type == "integer":
            try:
                ret = int(data)
                return ret
            except ValueError:
                return ""

        if data_type == "long":
            try:
                ret = long(data)
                return ret
            except ValueError:
                return ""

        if data_type == "complex":
            try:
                ret = complex(data)
                return ret
            except ValueError:
                return ""
        return ret
