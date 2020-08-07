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

@package avi.utils.coordinates_manager

--------------------------------------------------------------------------------

This module helps with the coordinates transformations
"""
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=DeprecationWarning)
    from astropy import  units as u
    from astropy.coordinates import SkyCoord 

class coordinates_manager:
    """@class coordinates_manager
    This class helps with the coordinates transformations
    """
    def gal_to_icrs(self, l, b):
        """Galactic to equatorial

        Transforms the given galactic coordinates to equatorial

        Args:
        self: The object pointer
        l: longitude
        b: latitude

        Returns:
        A dictionary containing the equatorial coordinates
        """
        coord = {}
        c = SkyCoord(l = l*u.degree, b = b*u.degree, frame='galactic')
        ret = c.transform_to('icrs')
        coord['ra'] = ret.ra.degree
        coord['dec'] = ret.dec.degree
        return coord
    
    def icrs_to_gal(self, r, d):
        """Equatorial to galactic

        Transforms the given equatorial coordinates to galactic

        Args:
        self: The object pointer
        r: RA
        d: DEC
        
        Returns:
        a dictionary containing the galactic coordinates
        """
        coord = {}
        c = SkyCoord(ra = r*u.degree, dec = d*u.degree, frame = 'icrs')
        ret = c.galactic
        coord['l'] = ret.l.degree
        coord['b'] = ret.b.degree
        return coord

    def icrs_degrees(self, r, d):
        """Equatorial represented with Julian days to equatorial represented in 
        degrees

        Transforms the given equatorial coordiantes represented with Julian 
        days to equatorial represented in degrees

        Args:
        self: The object pointer
        r: RA
        d: DEC

        Returns:
        A dictionary containing the equatorial coordinates
        """
        coord = {}
        try:
            c = SkyCoord(r,d, frame='icrs')
        except Exception:
            c = SkyCoord(r+d, unit=(u.hourangle, u.deg))
        coord['ra'] = c.ra.degree
        coord['dec'] = c.dec.degree
        return coord
