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

@package avi.forms

--------------------------------------------------------------------------------

This module provides the forms for the application.

This module provides the django views for the application.

@see https://docs.djangoproject.com/en/2.0/topics/forms/
"""
# Error control
import os
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

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
    return (('positional','Point Sources'),('images','Images'))

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
           ('level3','level3'))
           # ('browseProduct','browseProduct'),('logObsContext','logObsContext'),
           # ('quality','quality'),('qualitySummary','qualitySummary'))
           # #(('All','All'),('level0','level0'),('level0_5','level0_5'),
           # ('level1','level1'),('level2','level2'),('level2_5','level2_5'),
           # ('level3','level3'),('browseImageProduct','browseImageProduct'),
           # ('browseProduct','browseProduct'),('logObsContext','logObsContext'),
           # ('quality','quality'),('qualitySummary','qualitySummary'))
        
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
    name_coord = forms.ChoiceField(label='Name  Coordinates',help_text='Search by target name,Search by equatorial coordinates,Select a file,Search by ADQL querie',
                                   widget=forms.RadioSelect,
                                   required=True,
                                   choices=get_name_coord())
    ## name of the object to be queried
    name = forms.CharField(label='Name', max_length=255,help_text='Search by target name.',required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    ## input file containing multiple queries information
    input_file = forms.CharField(label='Search by File. Query by using an uploaded file. Select a file to be uploaded.',help_text='Input File', max_length=255, 
                                 required=False)
    ## ra
    ra = forms.FloatField(label='ra',help_text='Right Ascension',required=False,widget=forms.NumberInput(attrs={'class': 'form-control'}))
    ## dec
    dec = forms.FloatField(label='dec',help_text='Declination',required=False,widget=forms.NumberInput(attrs={'class': 'form-control'}))
    ## shape of the query
    shape = forms.ChoiceField(label='Shape', help_text='Target in Cone,Target in Box,Target in Polygon',
                              widget=forms.RadioSelect,
                              required=True,
                              choices=get_shapes())
    ## radius of the query
    radius = forms.FloatField(label='radius',help_text='Radius',required=False,widget=forms.NumberInput(attrs={'class': 'form-control'}))
    ## width of the query
    width = forms.FloatField(label='width',help_text='Width',required=False,widget=forms.NumberInput(attrs={'class': 'form-control'}))
    ## height of the query
    height = forms.FloatField(label='height',help_text='Height',required=False,widget=forms.NumberInput(attrs={'class': 'form-control'}))
    ## array containing the vertexes of a polygon
    polygon = forms.CharField(label='polygon',help_text='Polygon: RA DEC,RA DEC, ...', max_length=255,required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    ## is it a positional source catalog query or images?
    positional_images = forms.ChoiceField(label='Point Sources Images',help_text="Point Sources,Instrument Image",
                                          widget=forms.RadioSelect,
                                          required=True,
                                          choices=get_pos_img())
    ## table of the archive to be queried
    table = forms.ChoiceField(label='Table',help_text="Table to be queried",
                              widget=forms.Select(attrs={'class': 'form-control'}),
                              required=False,
                              choices=get_hs_tables())
    ## herschel instrument
    instrument = forms.ChoiceField(label='Instrument',help_text="Photodetector Array Camera and Spectrometer,Spectral and Photometric Imaging Receiver,Heterodyne Instrument for the Far Infrared",
                                   widget=forms.RadioSelect,
                                   required=False,
                                   choices=get_hs_instruments())
    ## processing level
    level = forms.ChoiceField(label='level',help_text="Level",
                              widget=forms.Select(attrs={'class': 'form-control'}),
                              required=False,
                              choices=get_hs_levels())
    ## output file name
    file_name = forms.CharField(label='File Name',help_text='File Name', max_length=255,required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    ## an ADQL query
    adql = forms.CharField(label='ADQL query', help_text='Search by ADQL. Use ADQL query syntax.',
                           #max_length=255,
                           required=False,
                           widget=forms.Textarea(attrs={'class': 'form-control'}))

class query_gaia_form(forms.Form):
    """@class query_gaia_form
    This class defines the form to query the gaia archive
    """
    ## has the query to be done by coordinates or name?
    name_coord = forms.ChoiceField(label='Name  Coordinates',help_text='Search by target name,Search by equatorial coordinates,Select a file,Search by ADQL querie',
                                   widget=forms.RadioSelect,
                                   required=True,
                                   choices=get_name_coord())
    ## name of the object to be queried
    name = forms.CharField(label='Name',help_text='Search by targe name', max_length=255,required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    ##name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}))
    ## input file containing multiple queries information
    input_file = forms.CharField(label='Input File',help_text='Search by File. Query by using an uploaded file. Select a file to be uploaded.', max_length=255, 
                                 required=False)
    ## ra
    ra = forms.FloatField(label='ra',required=False,help_text='Right Ascension',widget=forms.NumberInput(attrs={'class': 'form-control'}))
    ##ra = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}))
    ## dec
    dec = forms.FloatField(label='dec',required=False,help_text='Declination',widget=forms.NumberInput(attrs={'class': 'form-control'}))
    ##dec = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}))
    ## shape of the query
    shape = forms.ChoiceField(label='Shape', help_text='Target in Cone,Target in Box,Target in Polygon',
                              widget=forms.RadioSelect,
                              required=True,
                              choices=get_shapes())
    ## radius of the query
    radius = forms.FloatField(label='radius',help_text='The radius of the search cone.',required=False,widget=forms.NumberInput(attrs={'class': 'form-control'}))
    ##radius = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}))
    ## width of the query
    width = forms.FloatField(label='width',help_text='The width of the search Box.',required=False,widget=forms.NumberInput(attrs={'class': 'form-control'}))
    ##width = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}))
    ## height of the query
    height = forms.FloatField(label='height',help_text='The height of the search Box.',required=False,widget=forms.NumberInput(attrs={'class': 'form-control'}))
    ##height = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}))
    ## array containing the vertexes of a polygon
    polygon = forms.CharField(label='polygon',help_text='Polygon: RA DEC, RA DEC, ...', max_length=255,required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    ##polygon = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}))
    data_release = forms.ChoiceField(label='Data Release',help_text="Data Release 1,Data Release 2",
                                     widget=forms.RadioSelect,
                                     required=True,
                                     choices=get_data_releases())
    ## table of the archive to be queried
    table_dr1 = forms.ChoiceField(label='Table',help_text='Data Release 1 Tables',
                                  widget=forms.Select(attrs={'class': 'form-control'}),
                                  required=False,
                                  choices=get_gaia_dr1_tables())
    table_dr2 = forms.ChoiceField(label='Table',help_text='Data Release 2 Tables',
                                  widget=forms.Select(attrs={'class': 'form-control'}),
                                  required=False,
                                  choices=get_gaia_dr2_tables())
    ## output file name
    file_name = forms.CharField(label='File Name',help_text='File Name', max_length=255,required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    ##file_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}))
    ## an ADQL query
    adql = forms.CharField(label='ADQL query', help_text='ADQL Query',
                           #max_length=255,
                           required=False,
                           widget=forms.Textarea(attrs={'class': 'form-control'}))

class query_sim_form(forms.Form):
    """@class query_sim_form
    This class defines the form to query the simulations
    """
    ## Total mass (solar-mass)
    total_mass = forms.FloatField(validators=[MinValueValidator(1000), MaxValueValidator(10000)],
                                    help_text="Total Mass", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    ## virial ratio
    virial_ratio = forms.FloatField(validators=[MinValueValidator(0.3), MaxValueValidator(0.5)],
                                    help_text="Virial Ratio", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    ## Half-mass radius (pc) 0.1, 0.5, 1.0
    half_mass_radius = forms.FloatField(validators=[MinValueValidator(0.1), MaxValueValidator(1.0)],
                                    help_text="Half-Mass Radius", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    ## Fractal dimension
    fractal_dimension = forms.FloatField(validators=[MinValueValidator(2.0), MaxValueValidator(3.0)],
                                    help_text="Fractal Dimension", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    ## Degree of mass-segregation
    mass_segregation_degree = forms.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
                                    help_text="Degree of mass-segregation", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    ## Binary fraction (%)
    binary_fraction = forms.FloatField(validators=[MinValueValidator(0), MaxValueValidator(50)],
                                    help_text="Binary Fraction", widget=forms.NumberInput(attrs={'class': 'form-control'}))

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
