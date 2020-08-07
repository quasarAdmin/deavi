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

@package avi.core.interface.connection.connection

--------------------------------------------------------------------------------

This module provides connection features to the archives.
"""
import http.client
import urllib.parse
import time
from xml.dom.minidom import parseString

# from risea.utils import config_manager
from avi.utils import config_manager

#from risea.log import logger
from avi.log import logger

import requests

class connection:
    """@class connection
    The connection class provides connection features to the archives.
    """
    # default paths for Gaia
    ## http head
    httphdr = "http://"
    ## host name
    host = "gea.esac.esa.int"
    ## port
    port = 80
    ## path to the tap server
    tap_server = "/tap-server"
    ## path to the info
    pathinfo = "/tap-server/tap/async"
    ## path to the login
    pathlogin = "/tap-server/login"
    ## path to the logout
    pathlogout = "/tap-server/logout"
    ## path to the upload
    pathupload = "/tap-server/Upload"
    ## path to the results
    pathresults = "/results/result"
    ## the job id tag
    jobidtag = "uws:jobId"
    ## the phase tag
    phasetag = "uws:phase"
    ## cookies
    cookie = "cookies.txt"
    ## Deprecated, the connection object 
    connection = None
    ## The session
    session = None
    ## The user
    user = None
    
    ## Number of retries before abort the query
    retry_count = 20
    
    ## The log
    log = None
    
    #def __init__(self):
        
    def init(self, cfg):
        """Initializes the attributes.
        
        This method initializes the attributes with the given configuration

        Args:
        self: The object pointer
        cfg: The configuration to be loaded

        Returns:
        True if everything is initialized correctly, False otherwise
        """
        try:
            self.httphdr = cfg['http-header']
            self.host = cfg['host']
            self.port = cfg['port']
            self.tap_server = cfg['tap-server']
            self.pathinfo = cfg['async-pathinfo']
            self.pathlogin = cfg['login-pathinfo']
            self.pathlogout = cfg['logout-pathinfo']
            self.pathupload = cfg['upload-pathinfo']
            self.pathresults = cfg['results-pathinfo']
            self.jobidtag = cfg['jobid-tag']
            self.phasetag = cfg['phase-tag']
            self.cookie = cfg['cookie']
            self.log = logger().get_log('connection')
            return True
        except KeyError:
            return False
    
    def login(self, user, passwd):
        """Logs in to an archive

        This method logs in to an archive with the given user and password.

        It saves the session in the session attribute

        Args:
        self: The object pointer
        user: The user name
        passwd: The password

        Returns:
        True if the login was done correctly, False otherwise
        """
        params = {"username": user,"password": passwd}
        with requests.Session() as session:
            response = session.post(self.httphdr + self.host + self.pathlogin, data = params)
            if response.status_code != 200: return False
            self.session = session
            self.user = user
            return True
        #response = requests.post("http://" + self._host, data = params)
        #if response.status_code != 200: return False
        #print(response.cookies['Set-Cookie'])
        #print(response.text)
        #return True
        
    def logout(self):
        """Logs out of an archive

        This method logs out of an archive if there is a session active.

        Args:
        self: The object pointer

        Returns:
        True if the logout was done correctly, False otherwise
        """
        if self.session == None: return False
        response = self._session.post(self.httphdr + self.host + self.pathlogout)
        if response.status_code != 200: return False
        self.session = None
        return True
    
    def async_query(self, query):
        """Does a synchronous query to an archive

        Altough the name is async_query this method is actually synchronous. 
        The reason behind this name is because the actual connection to the 
        archive is asynchronous that way the connection is closed after the 
        request but the method will wait until the archives 
        answers the request.

        Args:
        self: The object pointer
        query: The ADQL query

        Returns:
        The data retrieved from the archive if everything goes correctly, 
        None otherwise
        """
        params = {"REQUEST": "doQuery","LANG": "ADQL","FORMAT": "votable","PHASE": "RUN", \
                  "QUERY": query}
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
        
        req = None
        if self.session != None:
            req = self.session
        else:
            req = requests
        response = req.post(self.httphdr + self.host + self.pathinfo, data = params, headers = headers)
        
        self.log.info('Status %s', str(response.status_code))
        if response.status_code != 200: 
            self.log.error('Connection failed!')
            return None
        
        dom = parseString(response.text)
        jobidElement = dom.getElementsByTagName(self.jobidtag)[0]
        jobidValueElement = jobidElement.firstChild
        raw_jobid = jobidValueElement.toxml()
        jobid = raw_jobid[raw_jobid.rfind('[')+1:-3]
        self.log.info('Job ID: %s', jobid)

        retry = self.retry_count
        while True:
            if retry == 0:
                self.log.error("Number of retries exceeded!")
                return None
            response = req.get(self.httphdr + self.host + self.pathinfo + "/" + jobid)
            data = response.text
            self.log.debug('%s',data)
            dom = parseString(data)
            phaseElement = dom.getElementsByTagName(self.phasetag)[0]
            phaseValueElement = phaseElement.firstChild
            phase = phaseValueElement.toxml()
            #print ("Status: " + phase)
            self.log.info('Status %s', phase)
            if phase == 'COMPLETED': break
            elif phase == 'ERROR': retry -= 1
            time.sleep(0.2)
            
        self.log.info("Retrieving results")
            
        response = req.get(self.httphdr + self.host + self.pathinfo + "/" + jobid + self.pathresults)

        self.log.info("Results retrieved")
        
        return response.text
    
    # This method works only with gaia
    def upload_table(self, name, table):
        """Uploads a user table to the archive user space.

        If the archives allows it, this method will upload a user table to the 
        archive user space.

        In order to do it, a login session has to be opened previously.
        
        Args:
        self: The object pointer
        name: The name of the table
        table: The table data

        Returns:
        True if the table is uploaded correctly, False otherwise
        """
        if self.session == None: return False
        
        params = {"TABLE_NAME": name}
        #{"FILE": table, "TABLE_NAME": name}
        files = {'file': open(table, 'rb')}
        response = self.session.post(self.httphdr + self.host + self.pathupload, data = params, files = files)
        if response.status_code != 200: return False
        return True
    
    # ###################################################################################################
    # deprecated
    # ###################################################################################################
    
    def de_anonymous_async_query(self, query):
        """Deprecated"""
        if self._connection != None: self._connection.close()
    
        params = urllib.parse.urlencode({"REQUEST": "doQuery","LANG": "ADQL","FORMAT": "votable","PHASE": "RUN", \
                                   "QUERY": query})
    
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    
        connection = http.client.HTTPConnection(self._host, self._port)
        connection.request("POST", self._pathinfo, params, headers)
    
        response = connection.getresponse()
        print ("Status: " + str(response.status), "Reason: " + str(response.reason))
    
        location = response.getheader("location")
        print ("Location: " + location)
    
        jobid = location[location.rfind('/')+1:]
        print ("Job id: " + jobid)
    
        connection.close()
    
        while True:
            connection = http.client.HTTPConnection(self._host, self._port)
            connection.request("GET", self._pathinfo+"/"+jobid)
            response = connection.getresponse()
            data = response.read()
            dom = parseString(data)
            phaseElement = dom.getElementsByTagName('uws:phase')[0]
            phaseValueElement = phaseElement.firstChild
            phase = phaseValueElement.toxml()
            print ("Status: " + phase)
            if phase == 'COMPLETED': break
            time.sleep(0.2)
    
        connection.close()
            
        connection = http.client.HTTPConnection(self._host, self._port)
        connection.request("GET", self._pathinfo+"/"+jobid+"/results/result")
        response = connection.getresponse()
        data = response.read()
        connection.close()
        return data
    
    def de_async_query(self, query):
        """Deprecated"""
        if self._connection == None: return None
        
        params = urllib.parse.urlencode({"REQUEST": "doQuery","LANG": "ADQL","FORMAT": "votable","PHASE": "RUN", \
                                   "QUERY": query})
    
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    
        self._connection.request("POST", self._pathinfo, params, headers)
    
        response = self._connection.getresponse()
        print ("Status: " + str(response.status), "Reason: " + str(response.reason))
    
        location = response.getheader("location")
        print ("Location: " + location)
    
        jobid = location[location.rfind('/')+1:]
        print ("Job id: " + jobid)
    
        while True:
            self._connection.request("GET", self._pathinfo+"/"+jobid)
            response = self._connection.getresponse()
            data = response.read()
            dom = parseString(data)
            phaseElement = dom.getElementsByTagName('uws:phase')[0]
            phaseValueElement = phaseElement.firstChild
            phase = phaseValueElement.toxml()
            print ("Status: " + phase)
            if phase == 'COMPLETED': break
            time.sleep(0.2)
    
        self._connection.request("GET", self._pathinfo+"/"+jobid+"/results/result")
        response = self._connection.getresponse()
        data = response.read()
        return data
    
    def de_login(self, user, passwd):
        """Deprecated"""
        if self._connection != None: self._connection.close()
        
        connection = http.client.HTTPConnection(self._host, self._port)
        #params = "username=" + user + "&password=" + passwd
        params = urllib.parse.urlencode({"username": user,"password": passwd})
    
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
        connection.request("POST", self._pathlogin, params, headers)
        response = connection.getresponse()
        hdrs = response.getheader('set-cookie')
        self._cookie = {"Cookie": hdrs}
        print ("Status: " + str(response.status), "Reason: " + str(response.reason))
        if response.status != 200: return False
        
        self._connection = connection
        
        return True
    
    def de_logout(self):
        """Deprecated"""
        if self._connection != None: 
        #connection = http.client.HTTPConnection(self._host, self._port)
            params = urllib.parse.urlencode(self._cookie)
            self._connection.request("POST", self._pathlogout,None,params)
            response = self._connection.getresponse()
            print ("Status: " + str(response.status), "Reason: " + str(response.reason))
            self._connection.close()
            self._connection = None
    
    def de_save_table(self, table):
        """Deprecated"""
        return table
