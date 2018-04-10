import traceback
import os
import pickle

from bokeh.embed import components
from bokeh.resources import CDN

from avi.log import logger
from avi.models import plot_model
from avi.utils.data.data_file import data_file

def save_plot(job_id, alg_name, plot):
    log = logger().get_log('plotter')
    try:
        sc_path = '/data/output/sc'
        html_path ='/data/output/html'
        sc , html = components(plot)#, CDN)
        #pickle.dump(sc, open(sc_path,'wb'))
        #pickle.dump(html, open(html_path,'wb'))
        model = plot_model(name = "name",
                           job_id = job_id,
                           alg_name = alg_name,
                           script = sc,
                           html = html)
        model.save()
        df = data_file(job_id)
        df.add_plot(model)
    except Exception:
        # TODO handle the exception
        log.warning(traceback.format_exc())
        pass

def load_plot(job_id, alg_name, name):
    log = logger().get_log('plotter')
    try:
        query = \
        plot_model.objects.filter(name=name).filter(job_id=job_id).filter(alg_name=alg_name)
        if not query:
            return None
        model = query[0]
        #sc = pickle.load(open(model.script,"rb"))
        #html = pickle.load(open(model.html,"rb"))
        sc = model.script
        html = model.html
        
        return (sc , html)
    except Exception:
        # TODO handle the exception
        log.warning(traceback.format_exc())
        pass

def remove_plot(job_id, alg_name, name):
    pass
