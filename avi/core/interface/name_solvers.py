
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=DeprecationWarning)
    from astroquery.simbad import Simbad
    from astroquery.ned import Ned

class simbad:

    def get_object_coordinates(self, name):
        obj = Simbad.query_object(name)
        if not obj:
            return None
        coord = {}
        coord['ra'] = obj['RA'][0]
        coord['dec'] = obj['DEC'][0]
        return coord
    
class ned:
    
    def get_object_coordinates(self, name):
        try:
            obj = Ned.query_object(name)
        except Exception:
            return None
        coord = {}
        coord['ra'] = obj['RA(deg)'][0]
        coord['dec'] = obj['DEC(deg)'][0]
        return coord
