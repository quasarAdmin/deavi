
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
    
    # default paths for Gaia
    httphdr = "http://"
    host = "gea.esac.esa.int"
    port = 80
    tap_server = "/tap-server"
    pathinfo = "/tap-server/tap/async"
    pathlogin = "/tap-server/login"
    pathlogout = "/tap-server/logout"
    pathupload = "/tap-server/Upload"
    pathresults = "/results/result"
    jobidtag = "uws:jobId"
    phasetag = "uws:phase"
    cookie = "cookies.txt"
    connection = None
    session = None
    user = None

    retry_count = 20
    
    log = None
    
    #def __init__(self):
        
    def init(self, cfg):
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
        if self.session == None: return False
        response = self._session.post(self.httphdr + self.host + self.pathlogout)
        if response.status_code != 200: return False
        self.session = None
        return True
    
    def async_query(self, query):
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
        if self._connection != None: 
        #connection = http.client.HTTPConnection(self._host, self._port)
            params = urllib.parse.urlencode(self._cookie)
            self._connection.request("POST", self._pathlogout,None,params)
            response = self._connection.getresponse()
            print ("Status: " + str(response.status), "Reason: " + str(response.reason))
            self._connection.close()
            self._connection = None
    
    def de_save_table(self, table):
        return table
