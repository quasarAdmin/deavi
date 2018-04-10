
class test:
    param1 = 0
    param2 = 0
    param3 = 0
    param4 = 0
    res = 0
    def run(self, id):
        f = open('/data/output/test.txt','w')
        self.res = self.param1 + self.param2 + self.param3 + self.param4
        str_res = str(self.res)
        f.write(str_res)
        f.close()
