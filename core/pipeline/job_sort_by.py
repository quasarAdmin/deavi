
from .job import job as parent

from avi.log import logger
from avi.warehouse import wh_frontend_config

class sort_by(parent):
    
    def are_equal(self, str1, str2):
        return str1.replace('-','',1) == str2

    def invert(self, string):
        if string[0] == '-':
            return string[1:]
        else:
            return "-" + string

    def start(self, data):
        wh = wh_frontend_config().get()

        if data['page'] == "pipeline_status":
            if self.are_equal(wh.SORTING_EXEC_BY, data['sort_by']):
                wh.SORTING_EXEC_BY = self.invert(wh.SORTING_EXEC_BY)
            else:
                wh.SORTING_EXEC_BY = data['sort_by']

        elif data['page'] == "query_status":
            if self.are_equal(wh.SORTING_QUERY_BY, data['sort_by']):
                wh.SORTING_QUERY_BY = self.invert(wh.SORTING_QUERY_BY)
            else:
                wh.SORTING_QUERY_BY = data['sort_by']

        elif data['page'] == "algorithm":
            if self.are_equal(wh.SORTING_ALG_BY, data['sort_by']):
                wh.SORTING_ALG_BY = self.invert(wh.SORTING_ALG_BY)
            else:
                wh.SORTING_ALG_BY = data['sort_by']

        elif data['page'] == "resources":
            if self.are_equal(wh.SORTING_RESOURCES_BY, data['sort_by']):
                wh.SORTING_RESOURCES_BY = self.invert(wh.SORTING_RESOURCES_BY)
            else:
                wh.SORTING_RESOURCES_BY = data['sort_by']

        elif data['page'] == "results":
            if self.are_equal(wh.SORTING_RESULTS_BY, data['sort_by']):
                wh.SORTING_RESULTS_BY = self.invert(wh.SORTING_RESULTS_BY)
            else:
                wh.SORTING_RESULTS_BY = data['sort_by']

        self.job_data.data = {}
        self.job_data.ok = True
        return self.job_data
