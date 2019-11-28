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

@package avi.core.interface.herschel

--------------------------------------------------------------------------------

This module provides the interface to the herschel archive 
"""
#from .connection.connection import connection
################################################################################
##################################################################################
import astropy.io.fits as fits
import astropy.io.votable
import urllib, shutil, os, tempfile
import numpy as np

import time
from django.utils import timezone

try:
    from urllib.parse import urlencode
    from urllib.request import Request, urlopen
    url_lib = urllib.request
except ImportError:
    from urllib2 import Request, urlopen
    from urllib import urlencode
    url_lib = urllib2

from .archive_interface import archive_interface
#from risea.log import logger
from avi.log import logger

from avi.utils.data.file_manager import file_manager
from avi.warehouse import wh_global_config

class herschel(archive_interface):
    """@class herschel
    The herschel class provides the interface to the herschel archive.

    It inherits from the archive_interface, this it uses the connection 
    object to access the archive.

    @see avi.core.interface.archive_interface.archive_interface
    @see avi.core.interface.connection.connection.connection
    """
    _metadata_url = 'http://archives.esac.esa.int/hsa/aio/jsp/metadata.jsp'
    _product_url = 'http://archives.esac.esa.int/hsa/aio/jsp/product.jsp'
    _data_url = "/data"
    _download_path = "/data/output/"
    _tmp_path = "/data/output/"
    _files_name = "data"

    ## The id of the job that started the query
    job_id = ""
    
    def __init__(self):
        """The herschel constructor

        The constructor initializes the log and calls the parent class 
        constructor to create the conneciton object.

        Args:
        self: The object pointer

        See:
        connection: avi.core.interface.connection.connection.connection
        """
        super(herschel, self).__init__()
        self.log = logger().get_log('herschel')

    def init(self, cfg):
        """Initializes the herschel interface
        
        This method initializes the herschel archive attributes using the 
        given configuration. Then calls the parent method init to finish the 
        initialization.

        Args:
        self: The object pointer
        cfg: The configuration to be loaded.

        Returns:
        True if the configuration is loaded correctly, False otherwise

        See:
        archive_interface: avi.core.interface.archive_interface.archive_interface
        """
        self._metadata_url = cfg['metadata_url']
        self._product_url = cfg['product_url']
        self._data_url = cfg['data']
        self._download_path = wh_global_config().get().HSA_PATH
        self._tmp_path = wh_global_config().get().HSA_PATH
        return super(herschel, self).init(cfg)
    
    def _herschel_test(self):
        query = "SELECT DISTANCE(POINT('ICRS',ra,dec), " \
                + "POINT('ICRS',266.41683,-29.00781)) AS dist, " \
                + "* FROM hsa.v_active_observation  " \
                + "WHERE 1=CONTAINS(POINT('ICRS',ra,dec), " \
                + "CIRCLE('ICRS',266.41683,-29.00781, 0.08333333)) " \
                + "ORDER BY dist ASC"
        data = self.connection.async_query(query)
        return data
    
    def get_circle(self, ra, dec, radius, table = "hsa.v_active_observation",
                   params = None):
        """Does a conical query to the archive.
        
        This method calls the parent method get_circle to do the query
                
        Args:
        self: The object pointer
        ra: The ra coordinate
        dec: The dec coordinate
        radius: The radius of the query
        table: The table to be queried
        params: Special parameters to the query
                
        Returns:
        The data retrieve from that query if everything was done 
        correctly, None otherwise
                
        See:
        archive_interface: avi.core.interface.archive_interface.archive_interface
        """
        return super(herschel, self).get_circle(ra, dec, radius, table, params)
    
    def get_box(self, ra, dec, width, height, table = "hsa.v_active_observation",
                params = None):
        """Does a box-shaped query to the archive.
        
        This method calls the parent method get_box to do the query
        
        Args:
        self: The object pointer
        ra: The ra coordinate
        dec: The dec coordinate
        width: The width of the box
        height: The height of the box
        table: The table to be queried
        params: Special parameters to the query
        
        Returns:
        The data retrieve from that query if everything was done 
        correctly, None otherwise
                
        See:
        archive_interface: avi.core.interface.archive_interface.archive_interface
        """
        return super(herschel, self).get_box(ra,dec,width,height,table,params)

    def get_polygon(self, ra, dec, vertexes, table = "hsa.v_active_observation",
                    params = None):
        """Does a polygonal-shaped query to the archive.
        
        This method calls the parent method get_polygon to do the query
                
        Args:
        self: The object pointer
        ra: The ra coordinate
        dec: The dec coordinate
        vertexes: An array of vertex forming the polygon
        table: The table to be queried
        params: Special parameters to the query

        Returns:
        The data retrieve from that query if everything was done 
        correctly, None otherwise
                
        See:
        archive_interface: avi.core.interface.archive_interface.archive_interface
        """
        return super(herschel, self).get_polygon(ra,dec,vertexes,table,params)

    def get_images(self, ra, dec, radius, level = "All",
                   instrument = 'PACS',
                   tap_server = False, table = None, name = "data"):
        """Retrieves the herschel images.

        This method retrieves the herschel images found in the area specified 
        by the given coordinates and radius.

        It also filters the retrieved images by the processing level specified 
        and the instrument.

        First it will query the positional sources archive to retrieve the 
        observation ids using the get_circle() method.

        Then with the observation ids retrieved it will call get_images_by_id() 
        to download the images.

        Args:
        self: The object pointer
        ra: The ra coordinate
        dec: The dec coordinate
        radius: The radius of the query
        level: The processing level
        intrument: The instrument
        tap_server: If we are using the new tap server access or not
        table: The table from which the method will extract the observarion ids.
        """
        self.log.info("Getting Herschel images ...")
        self._files_name = name
        if not table:
            #table = "hsa.cat_hppsc_070"
            table = "hsa.v_active_observation"

        vot_data = self.get_circle(ra, dec, radius,  table = table, \
                                   params = {"observation_id" : "observation_id"})

        if not vot_data:
            vot_data = self.get_circle(ra, dec, radius, table = table, \
                                       params = {"obsid" : "obsid"})

        #fp=tempfile.NamedTemporaryFile(prefix="hsa_vot_" mode ='wb',delete=False)
        #fname = fp.name
        #shutil.copyfileobj(vot_data, fp)
        #fp.close()
        outputFileName = self._tmp_path + "temp.vot"
        data = vot_data.encode('utf-8')
        outputFile = open(outputFileName, "wb")
        outputFile.write(data)
        outputFile.close()
        path = os.path.abspath(outputFileName)
        
        self.log.info("Opening VOTable from temporary file...")
        vot = astropy.io.votable.parse_single_table(path, pedantic=False)

        ids = self._get_ids_from_votable(vot)

        self.log.info("Removing temporary file...")
        os.path.exists(path) and os.remove(path)

        if ids == None or ids == []:
            self.log.error("The table has no observation_id key, " \
                           + "no obsids retrieved")
            return

        self.get_images_by_id(ids, level, instrument, tap_server)

    def get_images_box(self, ra, dec, width, height, level = "All",
                   instrument = 'PACS',
                   tap_server = False, table = None, name = "data"):
        """Retrieves the herschel images.

        This method retrieves the herschel images found in the area specified 
        by the given coordinates, width and height.

        It also filters the retrieved images by the processing level specified 
        and the instrument.

        First it will query the positional sources archive to retrieve the 
        observation ids using the get_box() method.

        Then with the observation ids retrieved it will call get_images_by_id() 
        to download the images.

        Args:
        self: The object pointer
        ra: The ra coordinate
        dec: The dec coordinate
        width: The width of the box
        height: The height of the box
        level: The processing level
        intrument: The instrument
        tap_server: If we are using the new tap server access or not
        table: The table from which the method will extract the observarion ids.
        """
        self.log.info("Getting Herschel images ...")
        self._files_name = name
        if not table:
            #table = "hsa.cat_hppsc_070"
            table = "hsa.v_active_observation"

        vot_data = self.get_box(ra, dec, width, height,  table = table, \
                                   params = {"observation_id" : "observation_id"})

        if not vot_data:
            vot_data = self.get_box(ra, dec, width, height, table = table, \
                                       params = {"obsid" : "obsid"})

        #fp=tempfile.NamedTemporaryFile(prefix="hsa_vot_" mode ='wb',delete=False)
        #fname = fp.name
        #shutil.copyfileobj(vot_data, fp)
        #fp.close()
        outputFileName = self._tmp_path + "temp.vot"
        data = vot_data.encode('utf-8')
        outputFile = open(outputFileName, "wb")
        outputFile.write(data)
        outputFile.close()
        path = os.path.abspath(outputFileName)
        
        self.log.info("Opening VOTable from temporary file...")
        vot = astropy.io.votable.parse_single_table(path, pedantic=False)

        ids = self._get_ids_from_votable(vot)

        self.log.info("Removing temporary file...")
        os.path.exists(path) and os.remove(path)

        if ids == None or ids == []:
            self.log.error("The table has no observation_id key, " \
                           + "no obsids retrieved")
            return

        self.get_images_by_id(ids, level, instrument, tap_server)

    def get_images_polygon(self, ra, dec, vertexes, level = "All",
                   instrument = 'PACS',
                   tap_server = False, table = None, name = "data"):
        """Retrieves the herschel images.

        This method retrieves the herschel images found in the area specified 
        by the given coordinates.

        It also filters the retrieved images by the processing level specified 
        and the instrument.

        First it will query the positional sources archive to retrieve the 
        observation ids using the get_polygon() method.

        Then with the observation ids retrieved it will call get_images_by_id() 
        to download the images.

        Args:
        self: The object pointer
        ra: The ra coordinate
        dec: The dec coordinate
        vertexes: An array of vertex forming the polygon
        level: The processing level
        intrument: The instrument
        tap_server: If we are using the new tap server access or not
        table: The table from which the method will extract the observarion ids.
        """
        self.log.info("Getting Herschel images ...")
        self._files_name = name
        if not table:
            #table = "hsa.cat_hppsc_070"
            table = "hsa.v_active_observation"

        vot_data = self.get_polygon(ra, dec, vertexes,  table = table, \
                                   params = {"observation_id" : "observation_id"})

        if not vot_data:
            vot_data = self.get_polygon(ra, dec, vertexes, table = table, \
                                       params = {"obsid" : "obsid"})

        #fp=tempfile.NamedTemporaryFile(prefix="hsa_vot_" mode ='wb',delete=False)
        #fname = fp.name
        #shutil.copyfileobj(vot_data, fp)
        #fp.close()
        if not vot_data:
            self.log.info("There are no observations in that area")
            return
        outputFileName = self._tmp_path + "temp.vot"
        data = vot_data.encode('utf-8')
        outputFile = open(outputFileName, "wb")
        outputFile.write(data)
        outputFile.close()
        path = os.path.abspath(outputFileName)
        
        self.log.info("Opening VOTable from temporary file...")
        vot = astropy.io.votable.parse_single_table(path, pedantic=False)

        ids = self._get_ids_from_votable(vot)

        self.log.info("Removing temporary file...")
        os.path.exists(path) and os.remove(path)

        if ids == None or ids == []:
            self.log.error("The table has no observation_id key, " \
                           + "no obsids retrieved")
            return

        self.get_images_by_id(ids, level, instrument, tap_server)

    def get_images_by_id(self, obids, level = "All", instrument = 'PACS',
                         tap_server = False):
        """This method retrieves the images by id.

        This method will retrieve each and everyone of the products with the 
        given ids.

        Args:
        self: The object pointer
        obids: An array with the observation ids
        level: The processing level
        instrument: The instrument
        tap_server: If we are using the new tap server access or not.
        """
        self.log.info("Getting Herschel images from the observation ids array...")
        for obsid in obids:
            self.log.info("getting obsid: %s, level: %s, instr: %s",
                          obsid, level, instrument)
            if not tap_server:
                self._get_image(obsid, level, instrument)
            else:
                self._get_image_from_tap_server(obsid, level, instrument)

    def _get_image_from_tap_server(self, obsid, level = "All", instrument='PACS'):
        self.log.info("Getting Herschel image from tap-server, " \
                      + "id=%s, level=%s, instru=%s...", \
                      obsid, level, instrument)
        values = { 'retrieval_type': 'OBSERVATION',
                   'observation_id': obsid,
                   'instrument_name': instrument,
                   'level': level,
                   'compress': 'true' }
        data = urlencode(values)
        data = data.encode('utf-8')
        req = Request(self._data_url, data)
        self.log.info("URL: %s %s", self._data_url,data)
        response = None
        try:
            response = urlopen(req)
        except Exception as err:
            self.log.error("Error while retrieving data :%i", err.code)
            return None
        file_name = self._download_path \
                    + "%s_%s_%s_%s.tar.gz"%(obsid.decode('utf-8'),
                                          instrument,
                                          level, self._files_name)
        fp = open(file_name, 'wb')
        shutil.copyfileobj(response,fp)
        self.log.info("File %s saved", fp.name)
        fp.close()
            
    def _get_ids_from_votable(self, vot):
        self.log.info("Getting observation ids from the VOTable...")
        table = vot.to_table()
        try:
            return list(set(table['observation_id']))
        except KeyError as err:
            try:
                return list(set(table['obsid']))
            except KeyError as err:
                return None
            return None
        #return table.get('observation_id')#table['observation_id']

    def _get_image(self, obsid, level = "All", instrument = 'PACS'):
        self.log.info("Getting Herschel image, id=%s, level=%s, instru=%s...", \
                      obsid, level, instrument)
        context_urn = self._get_obs_urn(obsid, instrument)
        if not context_urn:
            self.log.error("No context urn retrieved")
            return
        context_hdu = self._get_fits(context_urn)
        if not context_hdu:
            self.log.error("No context hdu retrieved")
            return
        obs_urn = self._parse_context_hdu(context_hdu)
        if not obs_urn:
            self.log.error("Something went wrong while parsing the context hdu")
            fname = context_hdu.get('filename')
            context_hdu.close()
            os.path.exists(fname) and os.remove(fname)
            return
        # TODO: check error
        if level == "All":
            for l in obs_urn:
                self._download_image(obs_urn, obsid, l, instrument)
        else:
            if not level in obs_urn:
                self.log.warning("Unknown level %s", level)
                return 
            self._download_image(obs_urn, obsid, level, instrument)
        fname = context_hdu.filename()
        context_hdu.close()
        os.path.exists(fname) and os.remove(fname)

    def _download_image(self, obs_urn, obsid, level, instrument):
        self.log.info("Downloading fits image...")
        self.log.info("Retrieving %s with urn %s", level, obs_urn[level])
        hdu = self._get_fits(obs_urn[level])
        # TODO: check obsid001, minobsid, fix hs header
        self.log.debug("hdu bandkey")
#        self.log.debug(hdu[0].header['obsid001'])
        bandkey_urn = self._parse_context_hdu(hdu)
        if not bandkey_urn:
            self.log.info("Skipping level %s", level)
        else:
            for i in bandkey_urn:
                self.log.info("Downloading herschel fits, " + \
                              " obsid=%s, level=%s, bandkey=%s, instrument=%s", \
                              obsid, level, i, instrument)
                # TODO: check path and create sub dirs, proper name, etc
                #file_name = self._download_path + obsid.decode('utf-8')
                #file_name = self._download_path \
                name = "%s_%s_%s_%s_%s.fits"%(obsid.decode('utf-8'),
                                           instrument,
                                           level, i, self._files_name)
                full_name = wh_global_config()\
                    .get().SOURCES_FMT%{"mission":"hsa",
                                        "date":str(round(time.time())),
                                        "name": name}
                file_name = os.path.join(self._download_path, full_name)

                hdulist = self._get_fits(bandkey_urn[i], file_name, True)
                hdulist.close()
    
    def _parse_context_hdu(self, hdu):
        self.log.info("Parsing context hdulist...")
        urn_dict = {}
        if not 'bridges' in hdu:
            return None
        nfields = hdu['bridges'].header['TFIELDS']
        self.log.info("Number of fields: %i", nfields)
        if nfields == 2:
            is_map = True
        elif nfields == 1:
            is_map = False
        else:
            self.log.error("Number of fields in the context table not valid!")
            return None

        table = hdu['bridges'].data
        self.log.debug(table)
        if is_map :
            for i in range(len(table['name'])):
                urn_dict[table['name'][i]] = \
                                    table['urn'][i].replace('urn::','urn:hsa:')
        else:
            for i in range(len(table['urn'])):
                urn_dict[i] = table['urn'][i].replace('urn::','urn:hsa:')
        self.log.debug(urn_dict)
        return urn_dict
    
    def _get_obs_urn(self, obsid, instrument = 'PACS'):
        self.log.info("Getting urn...")
        values = {'RESOURCE_CLASS' : 'PRODUCT', \
                  'OBSERVATION.OBSERVATION_ID' : obsid, \
                  'HCSS_CLASS_TYPE' : 'herschel.ia.obs.ObservationContext', \
                  'QUERY' : "(instrument=='%s')"%(instrument)}
        data = urlencode(values)
        data = data.encode('utf-8')
        self.log.debug(data)
        self.log.debug(self._metadata_url)
        req = Request(self._metadata_url, data)
        response = None

        try:
            response = urlopen(req)
        except url_lib.HTTPError as err:
            self.log.warning("Error while retrieving urn info :%i", err.code)
            return None
        except url_lib.URLError as err:
            self.log.warning("Error while retrieving urn info :%i", err.code)
            return None
        except Exception as err:
            self.log.warning("Error while retrieving urn info :%i", err.code)
            return None
        if not response:
            self.log.warning("Invalid response...")
            return None
        fp = tempfile.NamedTemporaryFile(prefix="hsa_vot_",
                                         mode ='wb', delete = False)
        fname = fp.name
        shutil.copyfileobj(response, fp)
        fp.close()
        vot = astropy.io.votable.parse_single_table(fname, pedantic=False)
        table = vot.to_table()
        if(len(table) > 0):
            table = table[np.where(table['HCSSTrackVersion'] \
                                   == np.max(table['HCSSTrackVersion']))]
            os.path.exists(fname) and os.remove(fname)
            urn = table['URN'].data[0]
            return urn
        return None

    def _get_fits(self, urn, fname = None, save = False):
        self.log.info("Getting fits file from urn=%s...", urn)
        if not urn:
            return None
        values = { 'PRODUCT.HCSS_URN' : urn }
        data = urlencode(values)
        data = data.encode('utf-8')
        req = Request(self._product_url, data)
        response = None
        try:
            response = urlopen(req)
        except url_lib.HTTPError as err:
            self.log.warning("Error while retrieving urn info :%i", err.code)
            return None
        except url_lib.URLError as err:
            self.log.warning("Error while retrieving urn info :%i", err.code)
            return None
        except Exception as err:
            self.log.warning("Error while retrieving urn info :%i", err.code)
            return None
        if not response:
            self.log.warning("Invalid response...")
            return None
        if fname:
            fp = open(fname, 'wb')
            fm = file_manager()
            fm.save_file_info(fname,fname,self.job_id,"hsa",timezone.now())
        else:
            fp = tempfile.NamedTemporaryFile(prefix="hsa_fits_",
                                             mode='wb', delete = False)
            fname = fp.name
        shutil.copyfileobj(response, fp)
        fp.close()
        self.log.info("File %s saved", fname)
        hdu = fits.open(fname)
        
        return hdu
