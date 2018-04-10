
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=DeprecationWarning)
    from astropy import  units as u
    from astropy.coordinates import SkyCoord 

class coordinates_manager:
    def gal_to_icrs(self, l, b):
        coord = {}
        c = SkyCoord(l = l*u.degree, b = b*u.degree, frame='galactic')
        ret = c.transform_to('icrs')
        coord['ra'] = ret.ra.degree
        coord['dec'] = ret.dec.degree
        return coord
    
    def icrs_to_gal(self, r, d):
        coord = {}
        c = SkyCoord(ra = r*u.degree, dec = d*u.degree, frame = 'icrs')
        ret = c.galactic
        coord['l'] = ret.l.degree
        coord['b'] = ret.b.degree
        return coord

    def icrs_degrees(self, r, d):
        coord = {}
        try:
            c = SkyCoord(r,d, frame='icrs')
        except Exception:
            c = SkyCoord(r+d, unit=(u.hourangle, u.deg))
        coord['ra'] = c.ra.degree
        coord['dec'] = c.dec.degree
        return coord
