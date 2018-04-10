
from .job import job as parent

from avi.models import herschel_query_model

class herschel_query(parent):
    def start(self,data):
        m = herschel_query_model(name_coord = data['name_coord'] == "name",
                                 name = data['name'], #if data['name'] != "" \
                                 #else None,
                                 input_file = data['input_file'],
                                 ra = data['ra'],
                                 dec = data['dec'],
                                 shape = data['shape'],
                                 radius = data['radius'],
                                 width = data['width'] if data['width'] else 0,
                                 height = data['height'] if data['height'] else 0  ,
                                 polygon = data['polygon'],#if data['polygon']!="" \
                                 #else None,
                                 positional_images = \
                                 data['positional_images'] == "images",
                                 table = data['table'],
                                 instrument = data['instrument'],
                                 level = data['level'],
                                 params = "",
                                 file_name = data['file_name'],
                                 adql = data['adql'])
        m.save()
        self.job_data.data = m
        self.job_data.ok = True
        return self.job_data
