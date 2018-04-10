
from .connection.connection import connection
# from risea.utils.adql_helper import adql_helper
from avi.utils.adql_helper import adql_helper

class archive_interface:
    
    connection = None
    log = None
    
    def __init__(self):
        self.connection = connection()
        
    def init(self, cfg):
        return self.connection.init(cfg)
    
    def get_columns(self, table):
        query = "SELECT top 1 * FROM " + table
        # TODO 
        return self.connection.async_query(query)

    def get_adql(self, query):
        self.log.info("ADQL query sent to the archive")
        data = self.connection.async_query(query)
        self.log.info("Query finished")
        return data
    
    def get_circle(self, ra, dec, radius, table = None, params = None):
        self.log.info("Conical query to the archive with ra: %f, dec: %f, radius: %f",ra, dec, radius)
        columns = "*"
        if params:
            columns = adql_helper().dic_to_str(params)
        query = "SELECT " + columns + " FROM  " + table
        query += " WHERE "+adql_helper().circle_defintion(ra, dec, radius)
        data = self.connection.async_query(query)
        self.log.info("Query finished")
        return data
    
    def get_box(self, ra, dec, width, height, table = None, params = None):
        self.log.info('Entering get_box with ra %f and dec %f',ra, dec)
        columns = "*"
        if params:
            columns = adql_helper().dic_to_str(params)
        query = "SELECT " + columns + " FROM  " + table
        query +=" WHERE "+adql_helper().box_definition(ra, dec, width, height)
        data = self.connection.async_query(query)
        self.log.info('query finished')
        return data

    def get_polygon(self, ra, dec, vertexes, table = None, params = None):
        self.log.info('Entering get_polygon')
        columns = "*"
        if params:
            columns = adql_helper().dic_to_str(params)
        query = "SELECT " + columns + " FROM " + table
        query +=" WHERE " + adql_helper().polygon_definition(ra, dec, vertexes)
        self.log.info(query)
        data = self.connection.async_query(query)
        self.log.info('query finished')
        return data
