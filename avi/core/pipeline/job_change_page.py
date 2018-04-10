
from .job import job as parent

from avi.log import logger
from avi.warehouse import wh_frontend_config

class change_page(parent):
    def start(self, data):
        #log = logger().get_log('get_queries_status')
        wh = wh_frontend_config().get()
        if data['page'] == "pipeline_status":
            wh.CURRENT_EXEC_PAGE = int(data['number'])
            
        if data['page'] == "query_status":
            wh.CURRENT_QUERY_PAGE = int(data['number'])

        if data['page'] == "algorithm":
            wh.CURRENT_ALG_PAGE = int(data['number'])

        if data['page'] == "resources":
            wh.CURRENT_RESOURCES_PAGE = int(data['number'])

        if data['page'] == "results":
            wh.CURRENT_RESULTS_PAGE = int(data['number'])

        self.job_data.data = {}
        self.job_data.ok = True
        return self.job_data
