"""
Copyright (C) 2016-2018 Quasar Science Resources, S.L.

This file is part of DEAVI.

DEAVI is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

DEAVI is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with DEAVI.  If not, see <http://www.gnu.org/licenses/>.

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

from .forms import query_gaia_form, query_herschel_form, resources_form

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
    if request.method == 'POST':
        log.info("Post %s",str(request.POST))
        data = dict(request.POST)
        log.info("Data %s", str(data))
        risea().get().start_job(wh_names().get().JOB_ALGORITHM,
                                data)
        
        return HttpResponseRedirect(wh_global_config().get().AVI_URL+'avi/status')
    
    template = loader.get_template('avi/pipeline_v2.html')
    res = risea().get().start_job(wh_names().get().JOB_GET_ALGORITHMS, None)
    context = res.data
    context['avi_url'] = wh_global_config().get().AVI_URL
    context['version'] = wh_global_config().get().VERSION
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
            risea().get().start_job(wh_names().get().JOB_DELETE,data)
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
                    'avi_url':wh_global_config().get().AVI_URL}
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
    if request.is_ajax():
        response = risea().get().start_job(wh_names().get().JOB_SAVE_SAMP_DATA,
                                           {'name':request.POST['name'],
                                            'data':request.POST['data']})
        #log.info(request.POST['data'])
    return HttpResponseRedirect(wh_global_config().get().AVI_URL+"avi/resources/filemanager")

def get_results(request):
    """View for the retrieving of the results of an execution.

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
    """View for the retrieving of a plot.

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
            log.debug("cleaned data \n%s",str(form.cleaned_data))
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
                                                'shape':'cone',
                                                'name_coord':'equatorial',
                                                'data_release':'dr1'}),
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
            log.debug("cleaned data \n%s", str(data))
            risea().get().start_job(wh_names().get().JOB_HSA_QUERY,
                                    data)
            
            return HttpResponseRedirect(wh_global_config().get().AVI_URL+'avi/queries/status')
        else:
            log.error("Invalid form")
        
    template = loader.get_template('avi/query_herschel.html')
    context = {'form': query_herschel_form(initial={'ra':'100.2417',
                                                    'dec':'9.895',
                                                    'radius':'0.5',
                                                    'shape':'cone',
                                                    'positional_images':'images',
                                                    'instrument':'PACS',
                                                    'name_coord':'equatorial'}),
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
            risea().get().start_job(wh_names().get().JOB_DELETE,data)
        if request.POST.get('delete_hsa'):
            log.info("Post %s",str(request.POST['delete_hsa']))
            data = {}
            data['type'] = "hsa"
            data['pk'] = request.POST['delete_hsa']
            risea().get().start_job(wh_names().get().JOB_DELETE,data)
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
    queries = risea().get().start_job(wh_names().get().JOB_GET_QUERIES_STATUS,
                                      None)
    template = loader.get_template('avi/query_status.html')
    if queries.ok:
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
                   'avi_url':wh_global_config().get().AVI_URL}
        #log.debug("get_queries_status context: %s", str(context))
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

        #  Delete file post
        if 'delete_file' in request.POST:
            log.debug("There is a delete_file POST")
            log.debug(request.POST)
            risea().get().delete_file(request.POST['delete_file'])
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
    context = {'directories_list': directories_list, 'files_list': files_list,
               'cpage': job.ok[1], 'pages': job.ok[0],
               'npage': job.ok[2], 'ppage': job.ok[3],
               'version':wh_global_config().get().VERSION,
               'avi_url':wh_global_config().get().AVI_URL}

    return HttpResponse(template.render(context,request))

def help_about(request):
    """View for the help/about page.

    This function provides the view for the help/about page.

    Args:
    request: HttpRequest object.
    
    Returns:
    A HttpResponse object of the help_about.html template.

    See:
    HttpRequest: https://docs.djangoproject.com/en/2.0/ref/request-response/#django.http.HttpRequest
    
    See also:
    HttpResponse: https://docs.djangoproject.com/en/2.0/ref/request-response/#httpresponse-objects
    """
    template = loader.get_template('avi/help_about.html')
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
