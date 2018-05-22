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
