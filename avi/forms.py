# Error control
import os
from django import forms

from enum import Enum

from avi.log import logger

class shape(Enum):
    CIRCLE = 0
    RECTANGLE = 1
    POLYGON = 2

class _query_gaia_form(forms.Form):
    name = forms.CharField(max_length=100)

class resources_form():
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
    return (('name','Name'),('equatorial','Equatorial'), ('file','File'))

def get_shapes():
    return (('cone','Cone'),('box','Box'),
            ('polygon','Polygon'))
def get_pos_img():
    return (('positional','Positional'),('images','Images'))

def get_hs_instruments():
    return (('PACS','PACS'),('SPIRE','SPIRE'),('HIFI','HIFI'))

def get_hs_levels():
    return (('All','All'),('level0','level0'),('level0_5','level0_5'),
            ('level1','level1'),('level2','level2'),('level2_5','level2_5'),
            ('level3','level3'),('browseImageProduct','browseImageProduct'),
            ('browseProduct','browseProduct'),('logObsContext','logObsContext'),
            ('quality','quality'),('qualitySummary','qualitySummary'))
        
def get_hs_tables():
    from avi.utils.config_manager import configuration_manager
    cfg = configuration_manager()
    ipath = os.path.join(os.path.dirname(os.path.abspath(__file__)),'config')
    if not cfg.load(os.path.join(ipath, 'config.xml')):
        return (('no_tables','no tables loaded'),)

    tables = cfg.get('hsa_tables')

    ret = ()
    l = []
    for t in tables:
        l.append((t,t))
    ret = tuple(sorted(l))
    return ret

def get_gaia_tables():
    from avi.utils.config_manager import configuration_manager
    cfg = configuration_manager()
    ipath = os.path.join(os.path.dirname(os.path.abspath(__file__)),'config')
    if not cfg.load(os.path.join(ipath, 'config.xml')):
        return (('no_tables','no tables loaded'),)

    tables = cfg.get('gaiadr1_tables')

    ret = ()
    l = []
    for t in tables:
        l.append((t,t))
    ret = tuple(sorted(l))
    return ret
        
class query_herschel_form(forms.Form):
    name_coord = forms.ChoiceField(label='Name  Coordinates',
                                   widget=forms.RadioSelect,
                                   required=True,
                                   choices=get_name_coord())
    name = forms.CharField(label='Name', max_length=255,required=False)
    input_file = forms.CharField(label='Input File', max_length=255, 
                                 required=False)
    ra = forms.FloatField(label='ra',required=False)
    dec = forms.FloatField(label='dec',required=False)
    shape = forms.ChoiceField(label='Shape',
                              widget=forms.RadioSelect,
                              required=True,
                              choices=get_shapes())
    radius = forms.FloatField(label='radius',required=False)
    width = forms.FloatField(label='width',required=False)
    height = forms.FloatField(label='height',required=False)
    polygon = forms.CharField(label='polygon', max_length=255,required=False)
    positional_images = forms.ChoiceField(label='Positional Images',
                                          widget=forms.RadioSelect,
                                          required=True,
                                          choices=get_pos_img())
    table = forms.ChoiceField(label='Table',
                              widget=forms.Select,
                              required=False,
                              choices=get_hs_tables())
    instrument = forms.ChoiceField(label='Instrument',
                                   widget=forms.RadioSelect,
                                   required=False,
                                   choices=get_hs_instruments())
    level = forms.ChoiceField(label='level',
                              widget=forms.Select,
                              required=False,
                              choices=get_hs_levels())
    file_name = forms.CharField(label='File Name', max_length=255,required=False)
    adql = forms.CharField(label='ADQL query', 
                           #max_length=255,
                           required=False,
                           widget=forms.Textarea)

class query_gaia_form(forms.Form):
    name_coord = forms.ChoiceField(label='Name  Coordinates',
                                   widget=forms.RadioSelect,
                                   required=True,
                                   choices=get_name_coord())
    name = forms.CharField(label='Name', max_length=255,required=False)
    input_file = forms.CharField(label='Input File', max_length=255, 
                                 required=False)
    ra = forms.FloatField(label='ra',required=False)
    dec = forms.FloatField(label='dec',required=False)
    shape = forms.ChoiceField(label='Shape',
                              widget=forms.RadioSelect,
                              required=True,
                              choices=get_shapes())
    radius = forms.FloatField(label='radius',required=False)
    width = forms.FloatField(label='width',required=False)
    height = forms.FloatField(label='height',required=False)
    polygon = forms.CharField(label='polygon', max_length=255,required=False)
    table = forms.ChoiceField(label='Table',
                              widget=forms.Select,
                              required=False,
                              choices=get_gaia_tables())
    file_name = forms.CharField(label='File Name', max_length=255,required=False)
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
