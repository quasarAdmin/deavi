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

@package avi.forms

--------------------------------------------------------------------------------

This module provides the forms for the application.

This module provides the django views for the application.

@see https://docs.djangoproject.com/en/2.0/topics/forms/
"""
# Error control
import os
from django import forms

from enum import Enum

from avi.log import logger

class shape(Enum):
    """@class shape
    The shape class is an enum with all the available shapes.
    """
    ## circle shape
    CIRCLE = 0
    ## rectangle
    RECTANGLE = 1
    ## polygon
    POLYGON = 2

class _query_gaia_form(forms.Form):
    """Deprecated"""
    name = forms.CharField(max_length=100)

class resources_form():
    """Deprecated"""
    post = None
    log = None
    str_log_header = 'resources_manager_form'
 
    def __init__(self, post):
        self.post = post
        self.log = logger().get_log(self.str_log_header)

    def is_valid(self):
        #ToDo all
        if not self.post['go_home']:
            self.post['go_home'] = "home"
        return True 
    

def get_name_coord():
    """This function returns the options to query an archive
    
    Returns:
    A set of tuplas with the options to query the archives
    """
    return (('name','Name'),('equatorial','Equatorial'), ('file','File'), 
            ('adql', 'ADQL'))

def get_shapes():
    """This function returns the shapes to query an archive
    
    Returns:
    A set of tuplas with the shapes to query the archives
    """
    return (('cone','Cone'),('box','Box'),
            ('polygon','Polygon'))

def get_data_releases():
    """This functions returns the gaia data releases

    Returns:
    A set of tuplas with the gaia data releases
    """
    return (('dr1', 'Data Release 1'),('dr2', 'Data Release 2'))

def get_pos_img():
    """This function returns the options to query the herschel archive
    
    Returns:
    A set of tuplas with the options to query the herschel archive
    """
    return (('positional','Positional'),('images','Images'))

def get_hs_instruments():
    """This function returns the instruments to query the herschel archive
    
    Returns:
    A set of tuplas with the instruments to query the hershcel archive
    """
    return (('PACS','PACS'),('SPIRE','SPIRE'),('HIFI','HIFI'))

def get_hs_levels():
    """This function returns the processing levels to query the herschel archive
    
    Returns:
    A set of tuplas with the processing levels to query the herschel archive
    """
    return (('All','All'),('level0','level0'),('level0_5','level0_5'),
            ('level1','level1'),('level2','level2'),('level2_5','level2_5'),
            ('level3','level3'),('browseImageProduct','browseImageProduct'),
            ('browseProduct','browseProduct'),('logObsContext','logObsContext'),
            ('quality','quality'),('qualitySummary','qualitySummary'))
        
def get_hs_tables():
    """This function returns the tables to query the herschel archive
    
    Returns:
    A set of tuplas with the tables to query the herschel archive
    """
    from avi.utils.config_manager import configuration_manager
    cfg = configuration_manager()
    ipath = os.path.join(os.path.dirname(os.path.abspath(__file__)),'config')
    if not cfg.load(os.path.join(ipath, 'config.xml')):
        return (('no_tables','no tables loaded'),)

    tables = cfg.get('hsa_tables')

    ret = ()
    l = []
    for t, v in tables.items():
        l.append((v,t))
    ret = tuple(sorted(l))
    return ret

def get_gaia_dr1_tables():
    """This function returns the tables to query the gaia dr1 archive
    
    Returns:
    A set of tuplas with the tables to query the gaia archive
    """
    from avi.utils.config_manager import configuration_manager
    cfg = configuration_manager()
    ipath = os.path.join(os.path.dirname(os.path.abspath(__file__)),'config')
    if not cfg.load(os.path.join(ipath, 'config.xml')):
        return (('no_tables','no tables loaded'),)

    tables = cfg.get('gaiadr1_tables')

    ret = ()
    l = []
    logger().get_log("views").info(str(tables))
    for t, v in tables.items():
        l.append((v,t))
    ret = tuple(sorted(l))
    return ret

def get_gaia_dr2_tables():
    """This function returns the tables to query the gaia dr2 archive
    
    Returns:
    A set of tuplas with the tables to query the gaia archive
    """
    from avi.utils.config_manager import configuration_manager
    cfg = configuration_manager()
    ipath = os.path.join(os.path.dirname(os.path.abspath(__file__)),'config')
    if not cfg.load(os.path.join(ipath, 'config.xml')):
        return (('no_tables','no tables loaded'),)

    tables = cfg.get('gaiadr2_tables')

    ret = ()
    l = []
    logger().get_log("views").info(str(tables))
    for t, v in tables.items():
        l.append((v,t))
    ret = tuple(sorted(l))
    return ret
        
class query_herschel_form(forms.Form):
    """@class query_herschel_form
    This class defines the form to query the herschel archive
    """
    ## has the query to be done by coordinates or name?
    name_coord = forms.ChoiceField(label='Name  Coordinates',
                                   widget=forms.RadioSelect,
                                   required=True,
                                   choices=get_name_coord())
    ## name of the object to be queried
    name = forms.CharField(label='Name', max_length=255,required=False)
    ## input file containing multiple queries information
    input_file = forms.CharField(label='Input File', max_length=255, 
                                 required=False)
    ## ra
    ra = forms.FloatField(label='ra',required=False)
    ## dec
    dec = forms.FloatField(label='dec',required=False)
    ## shape of the query
    shape = forms.ChoiceField(label='Shape',
                              widget=forms.RadioSelect,
                              required=True,
                              choices=get_shapes())
    ## radius of the query
    radius = forms.FloatField(label='radius',required=False)
    ## width of the query
    width = forms.FloatField(label='width',required=False)
    ## height of the query
    height = forms.FloatField(label='height',required=False)
    ## array containing the vertexes of a polygon
    polygon = forms.CharField(label='polygon', max_length=255,required=False)
    ## is it a positional source catalog query or images?
    positional_images = forms.ChoiceField(label='Positional Images',
                                          widget=forms.RadioSelect,
                                          required=True,
                                          choices=get_pos_img())
    ## table of the archive to be queried
    table = forms.ChoiceField(label='Table',
                              widget=forms.Select,
                              required=False,
                              choices=get_hs_tables())
    ## herschel instrument
    instrument = forms.ChoiceField(label='Instrument',
                                   widget=forms.RadioSelect,
                                   required=False,
                                   choices=get_hs_instruments())
    ## processing level
    level = forms.ChoiceField(label='level',
                              widget=forms.Select,
                              required=False,
                              choices=get_hs_levels())
    ## output file name
    file_name = forms.CharField(label='File Name', max_length=255,required=False)
    ## an ADQL query
    adql = forms.CharField(label='ADQL query', 
                           #max_length=255,
                           required=False,
                           widget=forms.Textarea)

class query_gaia_form(forms.Form):
    """@class query_gaia_form
    This class defines the form to query the gaia archive
    """
    ## has the query to be done by coordinates or name?
    name_coord = forms.ChoiceField(label='Name  Coordinates',
                                   widget=forms.RadioSelect,
                                   required=True,
                                   choices=get_name_coord())
    ## name of the object to be queried
    name = forms.CharField(label='Name', max_length=255,required=False)
    ## input file containing multiple queries information
    input_file = forms.CharField(label='Input File', max_length=255, 
                                 required=False)
    ## ra
    ra = forms.FloatField(label='ra',required=False)
    ## dec
    dec = forms.FloatField(label='dec',required=False)
    ## shape of the query
    shape = forms.ChoiceField(label='Shape',
                              widget=forms.RadioSelect,
                              required=True,
                              choices=get_shapes())
    ## radius of the query
    radius = forms.FloatField(label='radius',required=False)
    ## width of the query
    width = forms.FloatField(label='width',required=False)
    ## height of the query
    height = forms.FloatField(label='height',required=False)
    ## array containing the vertexes of a polygon
    polygon = forms.CharField(label='polygon', max_length=255,required=False)
    data_release = forms.ChoiceField(label='Data Release',
                                     widget=forms.RadioSelect,
                                     required=True,
                                     choices=get_data_releases())
    ## table of the archive to be queried
    table_dr1 = forms.ChoiceField(label='Table',
                                  widget=forms.Select,
                                  required=False,
                                  choices=get_gaia_dr1_tables())
    table_dr2 = forms.ChoiceField(label='Table',
                                  widget=forms.Select,
                                  required=False,
                                  choices=get_gaia_dr2_tables())
    ## output file name
    file_name = forms.CharField(label='File Name', max_length=255,required=False)
    ## an ADQL query
    adql = forms.CharField(label='ADQL query', 
                           #max_length=255,
                           required=False,
                           widget=forms.Textarea)

# deprecated
class _query_gaia_form():

    post = None
    log = None
    str_log_header = 'query_gaia_form'

    ra = None
    dec = None
    shape = None
    table = None
    # FIXME
    radius = None
    width = None
    height = None
    polygon = None
    
    
    def __init__(self, post):
        self.post = post
        self.log = logger().get_log(self.str_log_header)
    
    def is_valid(self):
        if not self.post['query-name-input']:
            # TODO pick proper name
            self.post['query-name-input'] = "TODO"
        if not self.post['query-ra-input']:
            self.log.error("No RA input found!")
            return False
        # TODO check RA
        if not self.post['query-dec-input']:
            self.log.error("No DEC input found!")
            return False
        # TODO check dec
        if not self.post['query-shape-circle-radius-input']:
            if not self.post['query-shape-rectangle-width-input']:
                if not self.post['query-shape-polygon-input']:
                    self.log.error("No shape input found!")
                    return False
                else:
                    # TODO polygon
                    self.log.debug("TODO polygon!")
            elif not self.post['query-shape-rectangle-height-input']:
                self.log.error("Rectangle shape invalid!")
                return False
            else:
                # TODO rectangle
                self.log.debug("TODO rectangle")
        else:
            # TODO circle
            self.log.debug("TODO circle")
            self.shape = shape.CIRCLE

        self.log.debug("Table input - %s", str(self.post.get('gaia-table-input')))
        if not self.post.get('gaia-table-input'):
            self.log.error("No table input found!")
            return False

        # TODO check table
            
        return True

    def validate(self):
        
        self.table = self.post['gaia-table-input']

        try:
            self.ra = float(self.post['query-ra-input'])
            self.dec = float(self.post['query-dec-input'])
            # TODO
            if self.shape == shape.CIRCLE:
                self.radius = float(self.post['query-shape-circle-radius-input'])
                self.log.debug("Radius value %f", self.radius)
                self.log.debug("validation values - %f %f %f %s", self.ra,
                               self.dec, self.radius, self.table)
        except ValueError as e:
            self.log.error("Invalid float argument\n %s", e)
            return False

        return True
    
    def get_dict(self):
        # FIXME:
        ret = {'name': self.post['query-name-input'],
               'ra': self.ra,
               'dec': self.dec,
               'radius': self.radius,
               'table': self.table}
        return ret
