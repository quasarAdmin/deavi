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

@package avi.views

--------------------------------------------------------------------------------

This module provides the main views.

This module provides the main django views for the user interface.

@see https://docs.djangoproject.com/en/2.0/topics/http/views/
"""
import json
import random
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.template.defaulttags import register

from .forms import query_gaia_form, query_herschel_form, resources_form, query_sim_form

import sys, os
from .utils.resources_manager import resources_manager
from .log import logger
from .utils.config_manager import configuration_manager
from .core.risea import risea
from .warehouse import wh_names, wh_frontend_config, wh_global_config

@register.filter
def get_item(data, key):
    return data.get(key)

@register.filter(name='getkey')
def getkey(value, arg):
    for k,v in value.items():
        if k == arg:
            return k
    return ""

def index(request):
    """View for the index page.

    This function provides the view for the index page.

    Args:
    request: HttpRequest object.
    
    Returns:
    A HttpResponse object of the index.html template.

    See:
    HttpRequest: https://docs.djangoproject.com/en/2.0/ref/request-response/#django.http.HttpRequest
    
    See also:
    HttpResponse: https://docs.djangoproject.com/en/2.0/ref/request-response/#httpresponse-objects
    """
    template = loader.get_template('avi/index.html')
    context = {'version':wh_global_config().get().VERSION,
               'avi_url':wh_global_config().get().AVI_URL,
               'portal_url':wh_global_config().get().PORTAL_URL} #RequestContext(request)
    return HttpResponse(template.render(context,request))

def create(request, fib):
    """Deprecated function.
    """
    #tutmod, created = TutorialModel.objects.get_or_create(fib_num = fib)

    res = risea().get().start_gaia_query(fib)
    tutmod = res.data
    logger().get_log("query_gaia").info("pk %s",str(tutmod.pk))
    
    context = { "tutmod": tutmod, "fib": fib }
    return render(request, 'avi/create.html', context)

def queries(request):
    """Deprecated function.
    """
    template = loader.get_template('avi/queries.html')
    context = {} #RequestContext(request)
    return HttpResponse(template.render(context,request))

def algorithm(request,alg_id):
    """Deprecated function.
    """
    log = logger().get_log("views")
    log.info('algorithm %s', str(alg_id))
    data = {}
    data['id'] = alg_id
    data['name'] = alg_id
    res = risea().get().start_job(wh_names().get().JOB_GET_ALGORITHM, data)
    res.data['id'] = alg_id
    res.data['avi_url'] = wh_global_config().get().AVI_URL
    res.data['version'] = wh_global_config().get().VERSION
    return render(request, 'avi/algorithm.html', res.data)
    template = loader.get_template('avi/algorithm.html')
    context = {} #RequestContext(request)
    return HttpResponse(template.render(context,request))

def pipeline_v2(request):
    """View for the pipeline v2 page.

    This function provides the view for the version 2 pipeline page.
    If recieves a POST request it will start an algorithm job with the given 
    parameters from the POST.

    Args:
    request: HttpRequest object.

    Returns:
    A HttpResponse object of the pipeline_v2.html template. If recieves a POST 
    request it will return a HttpResponseRedirect object to the avi/status url.
    
    See:
    HttpRequest: https://docs.djangoproject.com/en/2.0/ref/request-response/#django.http.HttpRequest

    See also:
    HttpResponse: https://docs.djangoproject.com/en/2.0/ref/request-response/#httpresponse-objects

    See also:
    HttpResponseRedirect: https://docs.djangoproject.com/en/2.0/ref/request-response/#httpresponse-objects
    
    @see job_algorithm @link avi.core.pipeline.job_algorithm
    """
    log = logger().get_log("views")
    log.info('url %s', request.get_full_path())
    log.info('host %s', request.build_absolute_uri())
    log.info('base %s', wh_global_config().get().AVI_URL)
    log.info('base %s', wh_global_config().get().PORTAL_URL)
    loading = {}
    loading['state'] = 'False'
    if request.method == 'POST':
        log.info("Post %s",str(request.POST))
        data = dict(request.POST)
        log.info("Data %s", str(data))
        if type(data) == dict:
            log.info("Im in!!!!!!!!!!!")
            if 'table' in data:
                log.info("hsa query")
                f = query_herschel_form(request.POST)
                log = logger().get_log("views")
                log.debug("Post \n%s",str(request.POST))
                if f.is_valid():
                    log.info("Valid form")
                    loading['algorithm_flag'] = data["algorithm_pk_hsa_form"]
                    data = f.cleaned_data
                    if request.FILES.get('input_file'):
                        log.info("There is a file %s", request.FILES['input_file'].name)
                        from django.core.files.storage import FileSystemStorage
                        fs = FileSystemStorage()
                        f = request.FILES['input_file']
                        full_name = os.path.join(wh_global_config().get().TMP_PATH, f.name)
                        filename = fs.save(full_name, f)
                        data['input_file'] = full_name
                        log.info(full_name)
                    log.debug("cleaned data %s", str(data))
                    job_data = risea().get().start_job(wh_names().get().JOB_HSA_QUERY,
                                            data)
                    
                    #return HttpResponseRedirect(wh_global_config().get().AVI_URL+'avi/queries/status')
                    loading['state'] = 'True'
                    loading['table'] = 'hsa'
                    loading['pk'] = job_data.data.pk
                else:
                    log.error("Invalid form")
            elif 'table_dr2' in data:
                log.info("gaia query")
                form = query_gaia_form(request.POST)

                if form.is_valid():
                    log.info("Valid query gaia form!")
                    loading['algorithm_flag'] = data["algorithm_pk_gaia_form"]
                    data = form.cleaned_data
                    if request.FILES.get('input_file'):
                        log.info("There is a file")
                        from django.core.files.storage import FileSystemStorage
                        fs = FileSystemStorage()
                        f = request.FILES['input_file']
                        full_name = os.path.join(wh_global_config().get().TMP_PATH, f.name)
                        filename = fs.save(full_name, f)
                        data['input_file'] = full_name
                    
                    log.debug("cleaned data %s",str(data))
                    job_data = risea().get().start_job(wh_names().get().JOB_GAIA_QUERY,
                                                      data)   
                    #return HttpResponseRedirect(wh_global_config().get().AVI_URL+'avi/queries/status')
                    loading['state'] = 'True'
                    loading['table'] = 'gaia'
                    loading['pk'] = job_data.data.pk
                    #log.info("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa: " + str(job_data.data.name))
                else:
                    log.error("Invalid form")
            else:
                risea().get().start_job(wh_names().get().JOB_ALGORITHM,data)
                return HttpResponseRedirect(wh_global_config().get().AVI_URL+'avi/status')
    template = loader.get_template('avi/pipeline_v2.html')
    res = risea().get().start_job(wh_names().get().JOB_GET_ALGORITHMS, None)
    gaia_query = {'form': query_gaia_form(initial={'ra':'100.2417',
                                                'dec':'9.895',
                                                'radius':'0.5',
                                                'height':'10',
                                                'width':'10',
                                                'polygon':'10 10,20 20',
                                                'shape':'cone',
                                                'name_coord':'equatorial',
                                                'data_release':'dr2',
                                                'adql':"SELECT source_id,ra,ra_error,dec,dec_error,parallax,parallax_error,phot_g_mean_mag,bp_rp,radial_velocity,radial_velocity_error,phot_variable_flag,teff_val,a_g_val FROM gaiadr2.gaia_source  WHERE CONTAINS(POINT('ICRS',gaiadr2.gaia_source.ra,gaiadr2.gaia_source.dec),CIRCLE('ICRS',COORD1(EPOCH_PROP_POS(100.2417,9.895,0,-.6300,-3.8800,17.6800,2000,2015.5)),COORD2(EPOCH_PROP_POS(100.2417,9.895,0,-.6300,-3.8800,17.6800,2000,2015.5)),0.001388888888888889))=1"})}
    hsa_query = {'form': query_herschel_form(initial={'ra':'100.2417',
                                                    'dec':'9.895',
                                                    'radius':'0.5',
                                                    'height':'10',
                                                    'width':'10',
                                                    'polygon':'10 10,20 20',
                                                    'shape':'cone',
                                                    'positional_images':'images',
                                                    'instrument':'PACS',
                                                    'name_coord':'equatorial',
                                                    'adql':"SELECT * FROM  hsa.pacs_point_source_100 WHERE 1= CONTAINS(POINT('ICRS',ra,dec), CIRCLE('ICRS', 100.2417, 9.895, 0.5))"})}
    context = res.data
    context['avi_url'] = wh_global_config().get().AVI_URL
    context['version'] = wh_global_config().get().VERSION
    context['gaia_query'] = gaia_query
    context['hsa_query'] = hsa_query
    context['loading'] = loading
    log.info(str(context))
    return HttpResponse(template.render(context,request))

def get_alg_info(request):
    """View for the retrieving of the algorithm information.

    This function is used by an ajax script to retrieve 
    the algorithm information. If the request is an ajax request,
    it will start a get_algorithm_info job.

    Args:
    request: HttpRequest object.
    
    Returns:
    A HttpResponse object with a json containing all the algorithm information.

    See:
    django http HttpRequest: https://docs.djangoproject.com/en/2.0/ref/request-response/#django.http.HttpRequest

    See also:
    HttpResponse: https://docs.djangoproject.com/en/2.0/ref/request-response/#httpresponse-objects

    @see job_get_algorithm_info @link avi.core.pipeline.job_get_algorithm_info
    """
    log = logger().get_log("views")
    log.info(request.POST)
    if request.is_ajax():
        data = {}
        #data['name'] = request.POST['name']
        data['id'] = request.POST['id']
        response = risea().get().start_job(wh_names().get().\
                                           JOB_GET_ALGORITHM_INFO,data)
        log.info(response.data)
        return HttpResponse(json.dumps(response.data))#['algorithm']))
                            #({"id":request.POST['id']}))
    return HttpResponse(json.dumps({"error":"error"}))

def pipeline(request):
    """Deprecated function.
    """
    log = logger().get_log("views")
    if request.method == 'POST':
        log.info("Post %s",str(request.POST))
        template = loader.get_template('avi/pipeline.html')
        context = risea().get().get_algorithm_list()

        data = risea().get().get_algorithm(dict(request.POST))
        log.info("Data %s", str(data))
        risea().get().start_job(wh_names().get().JOB_ALGORITHM,
                                data)
        
        return HttpResponseRedirect(wh_global_config().get().AVI_URL+'avi/status')
        
    template = loader.get_template('avi/pipeline.html')
    context = risea().get().get_algorithm_list()
    resources = risea().get().start_job(wh_names().get().JOB_GET_RESOURCES,
                                        None)
    context['resources'] = resources.data
    context['avi_url'] = wh_global_config().get().AVI_URL
    context['version'] = wh_global_config().get().VERSION
    log.info(str(context))
    return HttpResponse(template.render(context,request))

def status(request):
    """View for the pipeline status page.

    This function returns the pipeline status page.

    If it recieves a POST request containing the 'abort' message, it will start 
    the abort job.
    
    If it recieves a POST request containing the 'delete' message, it will 
    start the delete job.

    If it recieves a POST request containing the 'page' message, it will start 
    the change_page job with the given page provided by the POST.

    If it recieves a POST request containing the 'sort_by' message, it will 
    start the sort_by job with the given page provided by the POST.

    Then it will start a get_pipeline_status job.

    Args:
    request: HttpRequest object.
    
    Returns:
    A HttpResponse object of the status.html template.

    See:
    django http HttpRequest: https://docs.djangoproject.com/en/2.0/ref/request-response/#django.http.HttpRequest

    See also:
    HttpResponse: https://docs.djangoproject.com/en/2.0/ref/request-response/#httpresponse-objects

    @see job_get_pipeline_status @link avi.core.pipeline.job_get_pipeline_status

    @see job_abort @link avi.core.pipeline.job_abort

    @see job_delete @link avi.core.pipeline.job_delete

    @see job_change_page @link avi.core.pipeline.job_change_page
    
    @see job_sort_by @link avi.core.pipeline.job_sort_by
    """
    log = logger().get_log("views")
    rel = None
    if request.method == 'POST':
        if request.POST.get('abort'):
            log.info("Abort %s",str(request.POST['abort']))
            data = {}
            data['type'] = "algorithm"
            data['pk'] = request.POST['abort']
            risea().get().start_job(wh_names().get().JOB_ABORT,data)
        if request.POST.get('delete'):
            log.info("Delete %s",str(request.POST['delete']))
            data = {}
            data['type'] = "algorithm"
            data['pk'] = request.POST['delete']
            #if request.POST.get('delete_data'):
            #    data['delete-data'] = request.POST['delete_data']
            risea().get().start_job(wh_names().get().JOB_DELETE,data)
        if request.POST.get('delete_all'):
            log.info("Delete %s",str(request.POST['delete_all']))
            data = {}
            data['type'] = "algorithm"
            data['pk'] = request.POST['delete_all']
            #if request.POST.get('delete_data'):
            #    data['delete-data'] = request.POST['delete_data']
            data['delete-data'] = "yes"
            risea().get().start_job(wh_names().get().JOB_DELETE,data)
        if request.POST.get('relaunch'):
            log.info("Relaunch %s",str(request.POST['relaunch']))
            data = {}
            data['type'] = "algorithm"
            data['pk'] = request.POST['relaunch']
            aux_rel = risea().get().start_job(wh_names().get().JOB_RELAUNCH_ALGORITHM,data)
            #log.info("ret: %s", str(ret.data))
            rel = {}
            rel['ok'] = aux_rel.ok
            rel['data'] = aux_rel.data
        if request.POST.get('algorithm_id'):
            log.info("Algorithm_relaunch %s",str(request.POST['algorithm_id']))
            data = dict(request.POST)
            log.info("Data %s", str(data))
            risea().get().start_job(wh_names().get().JOB_ALGORITHM, data)
        if request.POST.get('page'):
            log.info("Page %s",str(request.POST['page']))
            data = {}
            data['page'] = 'pipeline_status'
            data['number'] = request.POST['page']
            risea().get().start_job(wh_names().get().JOB_CHANGE_PAGE, data)
        if request.POST.get('sort_by'):
            log.info("Sort by %s",str(request.POST['sort_by']))
            data = {}
            data['page'] = 'pipeline_status'
            data['sort_by'] = request.POST['sort_by']
            risea().get().start_job(wh_names().get().JOB_SORT_BY, data)

    template = loader.get_template('avi/status.html')
    jobs = risea().get().start_job(wh_names().get().JOB_GET_PIPELINE_STATUS,
                                   None)
    if jobs.ok:
        context = { 'jobs': jobs.data, 
                    'cpage': jobs.ok[1], 'pages': jobs.ok[0],
                    'npage': jobs.ok[2], 'ppage': jobs.ok[3],
                    'version':wh_global_config().get().VERSION,
                    'avi_url':wh_global_config().get().AVI_URL,
                    'alljobs': jobs.ok[4], 'ordby':jobs.ok[5]}
        if rel is not None and rel['ok']:
            context['relaunch'] = rel['data']
            log.info("context: %s", context)
    else:
        context = {'version':wh_global_config().get().VERSION,
                   'avi_url':wh_global_config().get().AVI_URL} #RequestContext(request)
    return HttpResponse(template.render(context,request))

def send_samp_data(request):
    """View for the saving of samp data from the client.

    This function is used by an ajax script to send data through samp from the 
    client.

    Args:
    request: HttpRequest object.
    
    Returns:
    A HttpResponse object with a json containing all the results information.

    See:
    django http HttpRequest: https://docs.djangoproject.com/en/2.0/ref/request-response/#django.http.HttpRequest

    See also:
    HttpResponse: https://docs.djangoproject.com/en/2.0/ref/request-response/#httpresponse-objects

    @see job_get_results @link avi.core.pipeline.job_get_results
    """
    #log = logger().get_log("views")
    #log.info("send_samp")
    #log.info(request.POST['data'])
    template = loader.get_template('avi/resources_filemanager.html')
    context = {'version':wh_global_config().get().VERSION,
               'avi_url':wh_global_config().get().AVI_URL}
    if request.is_ajax():
        log = logger().get_log("views")
        log.info("ajaxxxxxxxxxxxxxx")
        response = risea().get().start_job(wh_names().get().JOB_SAVE_SAMP_DATA,
                                           {'name':request.POST['name'],
                                            'data':request.POST['data']})
        #log.info(request.POST['data'])
        log.info(response.data)
        context["samp"] = response.data
        log.info(context)
    return HttpResponse(json.dumps(context))
    return HttpResponseRedirect(wh_global_config().get().AVI_URL+"avi/resources/filemanager")

def get_results(request):
    """View for the retrievement of the results of an execution.

    This function is used by an ajax script to retrieve 
    the results of an algorithm execution. If the request is an ajax request,
    it will start a get_results job.

    Args:
    request: HttpRequest object.
    
    Returns:
    A HttpResponse object with a json containing all the results information.

    See:
    django http HttpRequest: https://docs.djangoproject.com/en/2.0/ref/request-response/#django.http.HttpRequest

    See also:
    HttpResponse: https://docs.djangoproject.com/en/2.0/ref/request-response/#httpresponse-objects

    @see job_get_results @link avi.core.pipeline.job_get_results
    """
    log = logger().get_log("views")
    log.info(request.POST)
    if request.is_ajax():
        response = risea().get().start_job(wh_names().get().JOB_GET_RESULTS,
                                           request.POST['id'])
        log.info(response.data)
        return HttpResponse(json.dumps(response.data))

def get_plot(request):
    """View for the retrievement of a plot.

    This function is used by an ajax script to retrieve 
    a plot created as a result of an algorithm execution. 
    If the request is an ajax request,
    it will start a get_plot job.

    Args:
    request: HttpRequest object.
    
    Returns:
    A HttpResponse object with a json containing all the algorithm information.

    See:
    django http HttpRequest: https://docs.djangoproject.com/en/2.0/ref/request-response/#django.http.HttpRequest

    See also:
    HttpResponse: https://docs.djangoproject.com/en/2.0/ref/request-response/#httpresponse-objects

    @see job_get_plot @link avi.core.pipeline.job_get_plot
    """
    log = logger().get_log("views")
    log.info(request.POST)
    if request.is_ajax():
        response = risea().get().start_job(wh_names().get().JOB_GET_PLOT,
                                           request.POST['id'])
        log.info(request.POST['id'])
        #log.info(response.data)
        return HttpResponse(json.dumps(response.data))

def get_query_info(request):
    """View for the retrievement of the information of a query.

    This function is used by an ajax script to retrieve 
    the information of an query execution. If the request is an ajax request,
    it will start a get_query_info job.

    Args:
    request: HttpRequest object.
    
    Returns:
    A HttpResponse object with a json containing all the results information.

    See:
    django http HttpRequest: https://docs.djangoproject.com/en/2.0/ref/request-response/#django.http.HttpRequest

    See also:
    HttpResponse: https://docs.djangoproject.com/en/2.0/ref/request-response/#httpresponse-objects

    @see job_get_query_info @link avi.core.pipeline.job_get_query_info
    """
    log = logger().get_log("views")
    log.info(request.POST)
    if request.is_ajax():
        response = risea().get().start_job(wh_names().get().JOB_GET_QUERY_INFO,
                                           {'id':request.POST['id'],
                                            'mission': request.POST['mission']})
        return HttpResponse(json.dumps(response.data))
def get_query_status(request):
    """View for the retrievement of the status of a query.

    This function is used by an ajax script to retrieve 
    the status of an query execution. If the request is an ajax request,
    it will start a get_query_statsus job.

    Args:
    request: HttpRequest object.
    
    Returns:
    A HttpResponse object with a json containing all the results information.

    See:
    django http HttpRequest: https://docs.djangoproject.com/en/2.0/ref/request-response/#django.http.HttpRequest

    See also:
    HttpResponse: https://docs.djangoproject.com/en/2.0/ref/request-response/#httpresponse-objects

    @see job_get_query_status @link avi.core.pipeline.job_get_query_status
    """
    log = logger().get_log("views")
    if request.is_ajax():
        response = risea().get().start_job(wh_names().get().JOB_GET_QUERY_STATUS,
                                            {'id':request.POST['id'],
                                            'mission': request.POST['mission']})
        return HttpResponse(json.dumps(response.data))
def query_gaia(request):
    """View for the gaia query page.

    This function provides the view for the gaia query page.
    If it recieves a POST request it will start a gaia_query job with the given 
    parameters from the POST after checking them.

    Args:
    request: HttpRequest object.

    Returns:
    A HttpResponse object of the query_gaia.html template. If recieves a POST 
    request it will return a HttpResponseRedirect object to the 
    avi/queries/status url.
    
    See:
    HttpRequest: https://docs.djangoproject.com/en/2.0/ref/request-response/#django.http.HttpRequest

    See also:
    HttpResponse: https://docs.djangoproject.com/en/2.0/ref/request-response/#httpresponse-objects

    See also:
    HttpResponseRedirect: https://docs.djangoproject.com/en/2.0/ref/request-response/#httpresponse-objects
    
    @see job_gaia_query @link avi.core.pipeline.job_gaia_query
    """
    if request.method=='POST':
        form = query_gaia_form(request.POST)
        
        log = logger().get_log("query_gaia")
        log.debug("post \n%s", str(request.POST))

        if form.is_valid():
            log.info("Valid query gaia form!")
            data = form.cleaned_data
            if request.FILES.get('input_file'):
                log.info("There is a file")
                from django.core.files.storage import FileSystemStorage
                fs = FileSystemStorage()
                f = request.FILES['input_file']
                full_name = os.path.join(wh_global_config().get().TMP_PATH, f.name)
                filename = fs.save(full_name, f)
                data['input_file'] = full_name
            #if not form.validate():
            #    logger().get_log("query_gaia") \
            #            .error("Something went wrong with the validation!")
            #else:
            #    risea().get().start_job(wh_names().get().JOB_GAIA_QUERY,
            #form.get_dict())
                #risea().get().start_gaia_query(form.get_dict())
            #    logger().get_log("query_gaia").info("Query to the gaia "
            #                                        + "archive sent...")
            log.debug("cleaned data %s",str(data))
            risea().get().start_job(wh_names().get().JOB_GAIA_QUERY,
                                    data)
            return HttpResponseRedirect(wh_global_config().get().AVI_URL+'avi/queries/status')
        else:
            log.error("Invalid form")

    # form = query_gaia_form()
    template = loader.get_template('avi/query_gaia.html')
    #context = {} #RequestContext(request)
    #r = risea().get()
    #gaia_tables = r.get_gaia_tables()
    #context = {'tables' : sorted(gaia_tables)}
    context = {'form': query_gaia_form(initial={'ra':'100.2417',
                                                'dec':'9.895',
                                                'radius':'0.5',
                                                'height':'10',
                                                'width':'10',
                                                'polygon':'10 10,20 20',
                                                'shape':'cone',
                                                'name_coord':'equatorial',
                                                'data_release':'dr2',
                                                'adql':"SELECT source_id,ra,ra_error,dec,dec_error,parallax,parallax_error,phot_g_mean_mag,bp_rp,radial_velocity,radial_velocity_error,phot_variable_flag,teff_val,a_g_val FROM gaiadr2.gaia_source  WHERE CONTAINS(POINT('ICRS',gaiadr2.gaia_source.ra,gaiadr2.gaia_source.dec),CIRCLE('ICRS',COORD1(EPOCH_PROP_POS(100.2417,9.895,0,-.6300,-3.8800,17.6800,2000,2015.5)),COORD2(EPOCH_PROP_POS(100.2417,9.895,0,-.6300,-3.8800,17.6800,2000,2015.5)),0.001388888888888889))=1"}),
               'version':wh_global_config().get().VERSION,
               'avi_url':wh_global_config().get().AVI_URL}
    return HttpResponse(template.render(context,request))

def query_herschel(request):
    """View for the herschel query page.

    This function provides the view for the herschel query page.
    If it recieves a POST request it will start a hsa_query job with the given 
    parameters from the POST after checking them.

    Args:
    request: HttpRequest object.

    Returns:
    A HttpResponse object of the query_herschel.html template. 
    If recieves a POST request it will return a HttpResponseRedirect object to 
    the avi/queries/status url.
    
    See:
    HttpRequest: https://docs.djangoproject.com/en/2.0/ref/request-response/#django.http.HttpRequest

    See also:
    HttpResponse: https://docs.djangoproject.com/en/2.0/ref/request-response/#httpresponse-objects

    See also:
    HttpResponseRedirect: https://docs.djangoproject.com/en/2.0/ref/request-response/#httpresponse-objects
    
    @see job_hsa_query @link avi.core.pipeline.job_hsa_query
    """
    if request.method == 'POST':
        f = query_herschel_form(request.POST)
        log = logger().get_log("views")
        log.debug("Post \n%s",str(request.POST))
        if f.is_valid():
            log.info("Valid form")
            data = f.cleaned_data
            if request.FILES.get('input_file'):
                log.info("There is a file %s", request.FILES['input_file'].name)
                from django.core.files.storage import FileSystemStorage
                fs = FileSystemStorage()
                f = request.FILES['input_file']
                full_name = os.path.join(wh_global_config().get().TMP_PATH, f.name)
                filename = fs.save(full_name, f)
                data['input_file'] = full_name
                log.info(full_name)
            log.debug("cleaned data %s", str(data))
            risea().get().start_job(wh_names().get().JOB_HSA_QUERY,
                                    data)
            
            return HttpResponseRedirect(wh_global_config().get().AVI_URL+'avi/queries/status')
        else:
            log.error("Invalid form")
        
    template = loader.get_template('avi/query_herschel.html')
    context = {'form': query_herschel_form(initial={'ra':'100.2417',
                                                    'dec':'9.895',
                                                    'radius':'0.5',
                                                    'height':'10',
                                                    'width':'10',
                                                    'polygon':'10 10,20 20',
                                                    'shape':'cone',
                                                    'positional_images':'images',
                                                    'instrument':'PACS',
                                                    'name_coord':'equatorial',
                                                    'adql':"SELECT * FROM  hsa.pacs_point_source_100 WHERE 1= CONTAINS(POINT('ICRS',ra,dec), CIRCLE('ICRS', 100.2417, 9.895, 0.5))"}),
               'version':wh_global_config().get().VERSION,
               'avi_url':wh_global_config().get().AVI_URL}
    return HttpResponse(template.render(context,request))

def query_simulations(request):
    """View for the simulations query page.

    This function provides the view for the simulations query page.
    If it recieves a POST request it will start a sim_query job with the given 
    parameters from the POST after checking them.

    Args:
    request: HttpRequest object.

    Returns:
    A HttpResponse object of the query_simulations.html template. 
    If recieves a POST request it will return a HttpResponseRedirect object to 
    the avi/queries/status url.
    
    See:
    HttpRequest: https://docs.djangoproject.com/en/2.0/ref/request-response/#django.http.HttpRequest

    See also:
    HttpResponse: https://docs.djangoproject.com/en/2.0/ref/request-response/#httpresponse-objects

    See also:
    HttpResponseRedirect: https://docs.djangoproject.com/en/2.0/ref/request-response/#httpresponse-objects
    
    @see job_sim_query @link avi.core.pipeline.job_sim_query
    """
    if request.method == 'POST':
        f = query_sim_form(request.POST)
        log = logger().get_log("views")
        log.debug("Post \n%s",str(request.POST))
        if f.is_valid():
            log.info("Valid form")
            data = f.cleaned_data
            log.debug("cleaned data %s", str(data))
            risea().get().start_job(wh_names().get().JOB_SIM_QUERY,
                                    data)
            
            return HttpResponseRedirect(wh_global_config().get().AVI_URL+'avi/queries/status')
        else:
            log.error("Invalid form")
        
    template = loader.get_template('avi/query_sim.html')
    context = {'form': query_sim_form(initial={'total_mass':'1000',
                                                    'virial_ratio':'0.3',
                                                    'half_mass_radius':'0.1',
                                                    'fractal_dimension':'3.0',
                                                    'mass_segregation_degree':'0.0',
                                                    'binary_fraction':'0'
                                                    }),
               'version':wh_global_config().get().VERSION,
               'avi_url':wh_global_config().get().AVI_URL}
    return HttpResponse(template.render(context,request))

def query_status(request):
    """View for the query status page.

    This function returns the query status page.

    If it recieves a POST request containing the 'abort_gaia' or 'abort_hsa' 
    message, it will start the abort job.
    
    If it recieves a POST request containing the 'delete_gaia' or 'delete_hsa' 
    message, it will start the delete job.

    If it recieves a POST request containing the 'page' message, it will start 
    the change_page job with the given page provided by the POST.

    If it recieves a POST request containing the 'sort_by' message, it will 
    start the sort_by job with the given page provided by the POST.

    Then it will start a get_queries_status job.

    Args:
    request: HttpRequest object.
    
    Returns:
    A HttpResponse object of the query_status.html template.

    See:
    django http HttpRequest: https://docs.djangoproject.com/en/2.0/ref/request-response/#django.http.HttpRequest

    See also:
    HttpResponse: https://docs.djangoproject.com/en/2.0/ref/request-response/#httpresponse-objects

    @see job_get_queries_status @link avi.core.pipeline.job_get_queries_status

    @see job_abort @link avi.core.pipeline.job_abort

    @see job_delete @link avi.core.pipeline.job_delete

    @see job_change_page @link avi.core.pipeline.job_change_page
    
    @see job_sort_by @link avi.core.pipeline.job_sort_by
    """
    log = logger().get_log("views")
    ret = None
    if request.method == 'POST':
        if request.POST.get('abort_gaia'):
            log.info("Post %s",str(request.POST['abort_gaia']))
            data = {}
            data['type'] = "gaia"
            data['pk'] = request.POST['abort_gaia']
            risea().get().start_job(wh_names().get().JOB_ABORT,data)
        if request.POST.get('abort_hsa'):
            log.info("Post %s",str(request.POST['abort_hsa']))
            data = {}
            data['type'] = "hsa"
            data['pk'] = request.POST['abort_hsa']
            risea().get().start_job(wh_names().get().JOB_ABORT,data)
        if request.POST.get('delete_gaia'):
            log.info("Post %s",str(request.POST['delete_gaia']))
            data = {}
            data['type'] = "gaia"
            data['pk'] = request.POST['delete_gaia']
            if request.POST.get('delete_data'):
                data['delete-data'] = request.POST['delete_data']
            risea().get().start_job(wh_names().get().JOB_DELETE,data)
        if request.POST.get('delete_all_gaia'):
            log.info("Post %s",str(request.POST['delete_all_gaia']))
            data = {}
            data['type'] = "gaia"
            data['pk'] = request.POST['delete_all_gaia']
            data['delete-data'] = "yes"
            risea().get().start_job(wh_names().get().JOB_DELETE,data)
        if request.POST.get('delete_hsa'):
            log.info("Post %s",str(request.POST['delete_hsa']))
            data = {}
            data['type'] = "hsa"
            data['pk'] = request.POST['delete_hsa']
            if request.POST.get('delete_data'):
                data['delete-data'] = request.POST['delete_data']
            risea().get().start_job(wh_names().get().JOB_DELETE,data)
        if request.POST.get('delete_all_hsa'):
            log.info("Post %s",str(request.POST['delete_all_hsa']))
            data = {}
            data['type'] = "hsa"
            data['pk'] = request.POST['delete_all_hsa']
            data['delete-data'] = "yes"
            risea().get().start_job(wh_names().get().JOB_DELETE,data)
        if request.POST.get('abort_sim'):
            log.info("Post %s",str(request.POST['abort_sim']))
            data = {}
            data['type'] = "sim"
            data['pk'] = request.POST['abort_sim']
            risea().get().start_job(wh_names().get().JOB_ABORT,data)
        if request.POST.get('delete_sim'):
            log.info("Post %s",str(request.POST['delete_sim']))
            data = {}
            data['type'] = "sim"
            data['pk'] = request.POST['delete_sim']
            if request.POST.get('delete_data'):
                data['delete-data'] = request.POST['delete_data']
            risea().get().start_job(wh_names().get().JOB_DELETE,data)
        if request.POST.get('delete_all_sim'):
            log.info("Post %s",str(request.POST['delete_all_sim']))
            data = {}
            data['type'] = "sim"
            data['pk'] = request.POST['delete_all_sim']
            data['delete-data'] = "yes"
            risea().get().start_job(wh_names().get().JOB_DELETE,data)
        if request.POST.get('launch'):
            log.info("Post %s",str(request.POST['launch']))
            data = {}
            data['mission'] = ""
            data['id'] = request.POST['launch']
            ret = risea().get().start_job(wh_names().get().JOB_LAUNCH,data)
            log.info("ret: %s", str(ret.data))
            ret = ret.data
        if request.POST.get('algorithm_id'):
            log.info("Algorithm_relaunch %s",str(request.POST['algorithm_id']))
            data = dict(request.POST)
            log.info("Data %s", str(data))
            risea().get().start_job(wh_names().get().JOB_ALGORITHM, data)
        if request.POST.get('page'):
            log.info("Page %s",str(request.POST['page']))
            data = {}
            data['page'] = 'query_status'
            data['number'] = request.POST['page']
            risea().get().start_job(wh_names().get().JOB_CHANGE_PAGE, data)
        if request.POST.get('sort_by'):
            log.info("Sort by %s",str(request.POST['sort_by']))
            data = {}
            data['page'] = 'query_status'
            data['sort_by'] = request.POST['sort_by']
            risea().get().start_job(wh_names().get().JOB_SORT_BY, data)
        #return HttpResponseRedirect('avi/query_status.html')
    log.info("queries status start")
    try:
        queries = risea().get().start_job(wh_names().get().JOB_GET_QUERIES_STATUS,
                                          None)
    except Exception as e:
        log.info(e)
        queries = None
    log.info("queries status end")
    template = loader.get_template('avi/query_status.html')
    if queries is not None and queries.ok:
        #if request.POST:
            #log.debug("queries post: %s", str(request.POST))
        #log.info("queries %s", str(queries.data))
        #log.debug(queries.data[0])
        #if queries.data[0]:
        #    return HttpResponseRedirect('avi/query_status.html')
        context = {'queries': queries.data[1], 'update': queries.data[0], 
                   'cpage': queries.ok[1], 'pages': queries.ok[0],
                   'npage': queries.ok[2], 'ppage': queries.ok[3],
                   'version':wh_global_config().get().VERSION,
                   'avi_url':wh_global_config().get().AVI_URL,
                   'allqueries': queries.ok[4], 'ordby':queries.ok[5]}
        #log.debug("get_queries_status context: %s", str(context))
        if ret:
            #log.info("context ret: %s", str(ret))
            context['launch'] = ret
            #log.info("context: %s", context)
    else:
        context = {'version':wh_global_config().get().VERSION,
                   'avi_url':wh_global_config().get().AVI_URL} #RequestContext(request)
    return HttpResponse(template.render(context,request))

def query_saved(request):
    """Deprecated function.
    """
    template = loader.get_template('avi/query_saved.html')
    context = {} #RequestContext(request)
    request.session['menu_queries'] = " in"
    return HttpResponse(template.render(context,request))

def resources_filemanager(request):
    """View for the resources manager page.

    This function returns the resources manager page.

    First it will start the get_files job to retrieve the current path's 
    files and directories.

    If it recieves a POST request containing the 'go_home' message, it will 
    move the current directory to the home path and it will redirect again 
    to the avi/resources/filemanager url.

    If it recieves a POST request containing the 'up_directory' message, 
    it will move the current directory to the parent directory and it will 
    redirect again to the avi/resources/filemanager url.

    If it recieves a POST request containing the 'page' message, it will start 
    the change_page job with the given page provided by the POST and it will 
    redirect again to the avi/resources/filemanager url.

    If it recieves a POST request containing the 'sort_by' message, it will 
    start the sort_by job with the given page provided by the POST and it will 
    redirect again to the avi/resources/filemanager url.

    If it recieves a POST request containing a directory name, it will 
    move the current directory to that directory after checking if it is a 
    valid directory with directories retrieved by the get_files job and it will 
    redirect again to the avi/resources/filemanager url.

    If there is not POST then it will return a HttpResponse object of the 
    resources_filemanager.html template.

    Args:
    request: HttpRequest object.

    Returns:
    A HttpResponse object of the resources_filemanager.html template.
    If recieves a POST request it will return a HttpResponseRedirect object to 
    the avi/resources/filemanager url.
    
    See:
    django http HttpRequest: https://docs.djangoproject.com/en/2.0/ref/request-response/#django.http.HttpRequest

    See also:
    HttpResponse: https://docs.djangoproject.com/en/2.0/ref/request-response/#httpresponse-objects

    See also:
    HttpResponseRedirect: https://docs.djangoproject.com/en/2.0/ref/request-response/#httpresponse-objects

    @see job_get_files @link avi.core.pipeline.job_get_files

    @see job_change_page @link avi.core.pipeline.job_change_page
    
    @see job_sort_by @link avi.core.pipeline.job_sort_by
    """
    from avi.warehouse import wh_frontend_config

    log = logger().get_log("resources_manager")
    #log = logger().get_log("views")

    log.info("resourcesssss")

    #directories_list, files_list = risea().get().get_file_list()

    #data = [directories_list, files_list]
    job = risea().get().start_job(wh_names().get().JOB_GET_FILES, None)

    directories_list = job.data[0] 
    files_list = job.data[1]
    paths = job.data[2]
    gaia_files = job.data[3]
    hsa_files = job.data[4]
    sim_files = job.data[5]
    results_files = job.data[6]
    user_files = job.data[7]
#     current_path_files = risea().get().get_current_path()
    
    if request.method=='POST':
        log.debug("There is a POST method")        

        # home post
        if request.POST.get('go_home') == "home":
            log.debug("There is a go_home POST")
            home_site = risea().get().move_default_directory()
            return HttpResponseRedirect(wh_global_config().get().AVI_URL+"avi/resources/filemanager")
        else:
            log.debug("There is nothing")

        #  Create directory post 
        if 'directory_namee' in request.POST:
            # NOT ALLOWING THIS ANYMORE
            log.debug("There is a new_directory_pop_up POST")
            value_new_directory = request.POST['directory_name']
            log.debug(request.POST)
            risea().get().create_directory(value_new_directory)
            return HttpResponseRedirect(wh_global_config().get().AVI_URL+"avi/resources/filemanager")
        else:
            log.debug("There is nothing")

        #  Delete directory post
        if 'delete_folderr' in request.POST:
            # NOT ALLOWING THIS ANYMORE
            log.debug("There is a delete_directory POST")
            log.debug(request.POST)
            risea().get().delete_directory(request.POST['delete_folder'])
            log.debug("The directory has been deleted")
            return HttpResponseRedirect(wh_global_config().get().AVI_URL+"avi/resources/filemanager")
        else:
            log.debug("There is nothing")

        #  rename directory post
        if 'rename_folderr' in request.POST:
            # NOT ALLOWING THIS ANYMORE
            log.debug("There is a rename_directory POST")
            log.debug(request.POST)
            risea().get().rename_directory(request.POST['rename_folder'],\
                                            request.POST['directory_new_name'])
            log.debug("The directory has been renamed")
            return HttpResponseRedirect(wh_global_config().get().AVI_URL+"avi/resources/filemanager")
        else:
            log.debug("There is nothing")
       
        # Up post
        if request.POST.get('up_directory') == "up_directory":
            log.debug("There is a up_directory POST")
            directory_up = risea().get().directory_up()
            return HttpResponseRedirect(wh_global_config().get().AVI_URL+"avi/resources/filemanager")
        else:
            log.debug("There is nothing")
            
        # Enter POST
        log.debug(request.POST)
        for key, value in directories_list.items():
            if request.POST.get(key) == key:
                new_folder_risea = risea().get().directory_down(key)
                return HttpResponseRedirect(wh_global_config().get().AVI_URL+"avi/resources/filemanager")
            else:
                log.debug("There is nothing")
        if 'upload_file' in request.POST:
            log.debug("There is a upload_file POST")
            if request.FILES.get('input_file'):
                log.info("There is a file %s", request.FILES['input_file'].name)
                data = {}
                data['file'] = request.FILES['input_file']
                data['name'] = request.FILES['input_file'].name
                response = risea().get().start_job(wh_names().get().JOB_SAVE_USER_DATA,data)
                return HttpResponseRedirect(wh_global_config().get().AVI_URL+"avi/resources/filemanager")

        #  Delete file post
        if 'delete_file' in request.POST:
            log.debug("There is a delete_file POST")
            log.debug(request.POST)
            log.info("hellooooooooooo: " + str(request.POST))
            #risea().get().delete_file(request.POST['delete_file'])
            data = {}
            data['pk'] = request.POST['delete_file']
            risea().get().start_job(wh_names().get().JOB_DELETE_FILE, data)
            log.debug("The file has been deleted")
            return HttpResponseRedirect(wh_global_config().get().AVI_URL+"avi/resources/filemanager")
        else:
            log.debug("There is nothing")

        #  rename file post
        if 'rename_filee' in request.POST:
            # NOT ALLOWING THIS ANYMORE
            log.debug("There is a delete_file POST")
            log.debug(request.POST)
            risea().get().rename_file(request.POST['rename_file'],\
                                            request.POST['file_new_name'])
            log.debug("The file has been renamed")
            return HttpResponseRedirect(wh_global_config().get().AVI_URL+"avi/resources/filemanager")
        else:
            log.debug("There is nothing")

        if request.POST.get('page'):
            log.info("Page %s",str(request.POST['page']))
            data = {}
            data['page'] = 'resources'
            data['number'] = request.POST['page']
            risea().get().start_job(wh_names().get().JOB_CHANGE_PAGE, data)
            return HttpResponseRedirect(wh_global_config().get().AVI_URL+"avi/resources/filemanager")
        if request.POST.get('sort_by'):
            log.info("Sort by %s",str(request.POST['sort_by']))
            data = {}
            data['page'] = 'resources'
            data['sort_by'] = request.POST['sort_by']
            risea().get().start_job(wh_names().get().JOB_SORT_BY, data)
            return HttpResponseRedirect(wh_global_config().get().AVI_URL+"avi/resources/filemanager")
    
    else:
        log.debug("There is not POST method!")
    
  
    template = loader.get_template('avi/resources_filemanager.html')
    context = {'directories_list': directories_list, 'files_list': files_list,'paths': paths, 'gaia_files':gaia_files,
                'hsa_files':hsa_files, 'results_files':results_files, 'user_files':user_files,
               'cpage': job.ok[1], 'pages': job.ok[0],
               'npage': job.ok[2], 'ppage': job.ok[3],
               'version':wh_global_config().get().VERSION,
               'avi_url':wh_global_config().get().AVI_URL}

    return HttpResponse(template.render(context,request))

def about(request):
    """View for the about page.

    This function provides the view for the about page.

    Args:
    request: HttpRequest object.
    
    Returns:
    A HttpResponse object of the about.html template.

    See:
    HttpRequest: https://docs.djangoproject.com/en/2.0/ref/request-response/#django.http.HttpRequest
    
    See also:
    HttpResponse: https://docs.djangoproject.com/en/2.0/ref/request-response/#httpresponse-objects
    """
    template = loader.get_template('avi/about.html')
    context = {'version':wh_global_config().get().VERSION,
               'avi_url':wh_global_config().get().AVI_URL} #RequestContext(request)
    return HttpResponse(template.render(context,request))

def help(request):
    """View for the help page.

    This function provides the view for the help page.

    Args:
    request: HttpRequest object.
    
    Returns:
    A HttpResponse object of the help.html template.

    See:
    HttpRequest: https://docs.djangoproject.com/en/2.0/ref/request-response/#django.http.HttpRequest
    
    See also:
    HttpResponse: https://docs.djangoproject.com/en/2.0/ref/request-response/#httpresponse-objects
    """
    template = loader.get_template('avi/help.html')
    context = {'version':wh_global_config().get().VERSION,
               'avi_url':wh_global_config().get().AVI_URL} #RequestContext(request)
    return HttpResponse(template.render(context,request))

def contact(request):
    """View for the contact page.

    This function provides the view for the contact page.

    Args:
    request: HttpRequest object.
    
    Returns:
    A HttpResponse object of the help.html template.

    See:
    HttpRequest: https://docs.djangoproject.com/en/2.0/ref/request-response/#django.http.HttpRequest
    
    See also:
    HttpResponse: https://docs.djangoproject.com/en/2.0/ref/request-response/#httpresponse-objects
    """
    template = loader.get_template('avi/contact.html')
    context = {'version':wh_global_config().get().VERSION,
               'avi_url':wh_global_config().get().AVI_URL} #RequestContext(request)
    return HttpResponse(template.render(context,request))

def deavi_structure(request):
    """View for the deavi structure page.

    This function provides the view for the deavi structure page.

    Args:
    request: HttpRequest object.
    
    Returns:
    A HttpResponse object of the deavi structure.html template.

    See:
    HttpRequest: https://docs.djangoproject.com/en/2.0/ref/request-response/#django.http.HttpRequest
    
    See also:
    HttpResponse: https://docs.djangoproject.com/en/2.0/ref/request-response/#httpresponse-objects
    """
    template = loader.get_template('avi/deavi_structure.html')
    context = {'version':wh_global_config().get().VERSION,
               'avi_url':wh_global_config().get().AVI_URL} #RequestContext(request)
    return HttpResponse(template.render(context,request))

def tutorial(request):
    """View for the tutorial page.

    This function provides the view for the tutorial page.

    Args:
    request: HttpRequest object.
    
    Returns:
    A HttpResponse object of the tutorial.html template.

    See:
    HttpRequest: https://docs.djangoproject.com/en/2.0/ref/request-response/#django.http.HttpRequest
    
    See also:
    HttpResponse: https://docs.djangoproject.com/en/2.0/ref/request-response/#httpresponse-objects
    """
    template = loader.get_template('avi/tutorial.html')
    context = {'version':wh_global_config().get().VERSION,
               'avi_url':wh_global_config().get().AVI_URL} #RequestContext(request)
    return HttpResponse(template.render(context,request))


def vr(request):
    """Deprecated function.
    """
    stars = {}
    log = logger().get_log("views")
    for i in range(0,10000):
        x = random.uniform(-1000,1000)
        y = random.uniform(-1000,1000)
        z = random.uniform(-1000,1000)
        stars[i] = (x, y , z)
    #stars[0] = ( -6, 4, 2)
    #stars[1] = ( -4, 1, 5)
    #stars[2] = ( 6, 2, 1)
    log.info(stars)
    context = { 'stars': json.dumps(stars) }
    template = loader.get_template('avi/vr_debug.html')
    return HttpResponse(template.render(context, request))

def debug(request):  
    """View for the debug page.

    This function provides the view for the debug page.

    Args:
    request: HttpRequest object.
    
    Returns:
    A HttpResponse object of the index.html template.

    See:
    HttpRequest: https://docs.djangoproject.com/en/2.0/ref/request-response/#django.http.HttpRequest
    
    See also:
    HttpResponse: https://docs.djangoproject.com/en/2.0/ref/request-response/#httpresponse-objects
    """
    log = logger().get_log("views")
    if request.method == 'POST':
        log.info("Post %s",str(request.POST))
        log.info("file %s",str(request))
        if request.FILES['myfile']:
            log.info("There is a file")
            from django.core.files.storage import FileSystemStorage
            fs = FileSystemStorage()
            f = request.FILES['myfile']
            full_name = "/data/output/" + f.name
            filename = fs.save(full_name, f)
    context = {'version':wh_global_config().get().VERSION,
               'avi_url':wh_global_config().get().AVI_URL}
    template = loader.get_template('avi/debug.html')
    return HttpResponse(template.render(context, request))
    
    if request.method == 'POST':
        log = logger().get_log("views")
        log.info("Post %s",str(request.POST)) 
        template = loader.get_template('avi/debug.html')
        context = { "render_input_form" : True,
                    "alg" : request.POST['alg']}
        return HttpResponse(template.render(context, request))
    
    from bokeh.plotting import figure, output_file, save
    from bokeh.embed import components
    from bokeh.resources import CDN
    
    x = [1,2,3,4,5]
    y = [6,7,2,4,5]
    #output_file("lines.html")
    p = figure(title="simple", x_axis_label='x',y_axis_label='y')
    p.line(x,y, legend="temp", line_width = 2)
    #path = save(p, filename="/home/sfm/deavi/avi/templates/avi/plot.html")
    plot = figure()
    plot.circle([1,2],[3,4])
    
    from avi.utils.plotter import load_plot
    sc, div = load_plot(3,"dummy","name")
    
    from django.utils.safestring import mark_safe

    sc = mark_safe(sc)
    div = mark_safe(div)

    #sc, div = components(plot, CDN)
    
    log = logger().get_log("views")
    log.info("Plot path %s",sc)
    log.info("Plot path %s",div)
    context = { "sc": sc, "pdiv": div }
    template = loader.get_template('avi/debug.html')
#    context = RequestContext(request)
    return HttpResponse(template.render(context, request))
