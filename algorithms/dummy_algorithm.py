
from avi.log import logger

class dummy_algorithm:
    param1 = 0
    param2 = 0
    param3 = 0
    res = 0
    def run(self, id):
        log = logger().get_log('algorithm_task')
        log.info("Result: %f", self.param1 + self.param2)
        f = open('/data/output/dummy_alg.txt', 'w')
        self.res = self.param1 + self.param2 + self.param3
        str_res = str(self.res)
        f.write(str_res)
        f.close()
