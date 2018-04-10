
class adql_helper:
    def dic_to_str(self, dic):
        ret = ""
        for val in dic:
            ret += str(val) + ", "
        return ret[:-2]
    
    def circle_defintion(self, x, y, radius, coord_system = "ICRS"):
        return "1= CONTAINS(POINT('"+coord_system+"',ra,dec), CIRCLE('"+coord_system+"', " + str(x) + ", " + str(y) + ", " + str(radius) + "))"
    
    def box_definition(self, x, y, width, height, coord_system = 'ICRS'):
        return "(1= CONTAINS(POINT('ICRS',ra,dec), BOX('ICRS', " + str(x) + ", " + str(y) + ", " + str(width) + " , " + str(height) + ")))"

    def polygon_definition(self, x, y, vertexes, coord_system = "ICRS"):
        str_ver = str(x) + ", " + str(y)
        for i in vertexes:
            str_ver += ", " + str(i['ra']) + ", " + str(i['dec'])
        return "1= CONTAINS(POINT('"+coord_system+"',ra,dec), " \
            "POLYGON('"+coord_system+"', "+str_ver+"))"
