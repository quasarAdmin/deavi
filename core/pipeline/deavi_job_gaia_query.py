
from .job import job as parent
#from avi.models import TutorialModel #gaia_query_model

# FIXME:
from avi.models import gaia_query_model

class gaia_query(parent):

    def start(self, data):
        # TODO:
        #m, created = TutorialModel.objects.get_or_create(fib_num = int(data))
        #gaia_test.delay(data)
        #self.job_data.data = data
        #self.job_data.ok = True
        #return self.job_data
        m = gaia_query_model(name = data['name'],
                             ra = float(data['ra']),
                             dec = float(data['dec']),
                             radius = float(data['radius']),
                             table = data['table'],
                             params = "")
        m.save()
        #TutorialModel.objects.get_or_create(fib_num = int(data))
        self.job_data.data = m
        self.job_data.ok = True
        return self.job_data
