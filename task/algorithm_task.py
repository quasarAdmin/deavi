
import ast

from .task import task as parent
from .task import task_exception as err
from avi.log import logger

class algorithm_task(parent):
    def output(self):
        pass

    def __get_data(self, raw):
        if not raw or raw == "":
            return None
        ret = None
        try:            
            ret = ast.literal_eval(raw)
        except ValueError:
            return None
        except SyntaxError:
            return None
        return ret
    
    def run(self):
        log = logger().get_log("algorithm_task")
        log.info("running algorithm")

        data = self.__get_data(self.task_data.data)

        if not data:
            log.error("Invalid data provided")
            return
        
        alg_name = data['algorithm']['name']

        package_str = "avi.algorithms." + alg_name
        module_str = alg_name

        log.info("from %s import %s",package_str,module_str)

        mod = __import__(package_str, fromlist=[module_str])

        log.info("Getting algorithm obj")
        
        alg = getattr(mod, alg_name)()

        log.info("Filling algorithm params")
        
        for k, v in data['algorithm']['params'].items():
            setattr(alg, k, v)

        log.info("Running algorithm %i", self.task_id)
            
        alg.run(self.task_id)

        log.info("Saving results")

        res = {'results':{'result': 10}}
        
        #for k, v in data['algorithm']['results'].items():
        #    res['results'][k] = getattr(alg,k)

        self.results = res
