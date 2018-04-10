
from .job import job as parent

from django.core.paginator import Paginator

from avi.warehouse import wh_global_config as wh
from avi.warehouse import wh_frontend_config
from avi.log import logger

class get_algorithms(parent):
    def start(self, data):
        log = logger().get_log('algorithm_manager')

        wh_f = wh_frontend_config().get()

        if not wh().get().ALGORITHMS_LOADED:
            from avi.core.algorithm.algorithm_manager import algorithm_manager
            algorithm_manager().init()
            wh().get().ALGORITHMS_LOADED = True

        from avi.models import algorithm_info_model
        all_ms = algorithm_info_model.objects.all().order_by('name_view',
                                                          'name','pk')
        
        self.job_data.data = {}
        self.job_data.ok = all_ms is not None
        if not all_ms:
            return self.job_data

        pg = Paginator(all_ms, wh_f.MAX_ALG_PER_PAGE)
        page = wh_f.CURRENT_ALG_PAGE
        if page < 1:
            wh_f.CURRENT_ALG_PAGE = 1
        elif page > pg.num_pages:
            wh_f.CURRENT_ALG_PAGE = pg.num_pages

        ms = pg.page(wh_f.CURRENT_ALG_PAGE)
        data = {}
        i = 0
        for j in ms:
            data[i] = (j.pk,
                       j.name,
                       j.name_view,
                       j.algorithm_type)
            i += 1
            
        res = {}
        res["algorithms"] = data
        res["max_pages"] = pg.num_pages
        res["current_page"] = wh_f.CURRENT_ALG_PAGE
        res["next_page"] = wh_f.CURRENT_ALG_PAGE + 1
        res["prev_page"] = wh_f.CURRENT_ALG_PAGE - 1
        self.job_data.data = res
        return self.job_data
