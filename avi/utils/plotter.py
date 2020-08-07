"""
Copyright (C) 2016-2020 Quasar Science Resources, S.L.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.

@package avi.utils.plotter

--------------------------------------------------------------------------------

This module provides an interface to save plots
"""
import traceback
import os
import pickle

from bokeh.embed import components
from bokeh.resources import CDN

from avi.log import logger
from avi.models import plot_model
from avi.utils.data.data_file import data_file

def save_plot(job_id, alg_name, plot):
    """saves the given plot

    This function saves the given plot an associates it with the given job id

    Args:
    job_id: The job id to be associated with
    alg_name: The name of the algorithm
    plot: A bokeh plot object
    """
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
        log.warning(traceback.format_exc())
        return False
    return True

def load_plot(job_id, alg_name, name):
    """Deprecated, Loads a plot
    This function loads a plot with associated with the given name and job_id

    Args:
    job_id: The job id which the plot is associated with
    alg_name: The name of the algorithm
    name: The name of the plot

    Returns:
    A tuple with the plot script and the plot html
    """
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
        log.warning(traceback.format_exc())
        return False
    return True

def remove_plot(job_id, alg_name, name):
    """Not implemented"""
    pass
