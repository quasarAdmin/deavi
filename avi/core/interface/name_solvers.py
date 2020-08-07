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

@package avi.core.interface.name_solvers

--------------------------------------------------------------------------------

This module provides classes to transform space object names to coordenates
"""
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=DeprecationWarning)
    from astroquery.simbad import Simbad
    from astroquery.ned import Ned

class simbad:
    """@class simbad
    This class translates names using simbad

    It uses simbad to transform from space object names to equatorial 
    coordinates
    """
    def get_object_coordinates(self, name):
        """Transforms the name to coordinates
        
        This method transforms from space object names to equatorial 
        coordiantes
        
        Args:
        self: The object pointer
        name: Name of the space object
        """
        obj = Simbad.query_object(name)
        if not obj:
            return None
        coord = {}
        coord['ra'] = obj['RA'][0]
        coord['dec'] = obj['DEC'][0]
        return coord
    
class ned:
    """@class ned
    This class translates names using ned

    It uses ned to transform from space object names to equatorial 
    coordinates
    """
    def get_object_coordinates(self, name):
        """Transforms the name to coordinates
        
        This method transforms from space object names to equatorial 
        coordiantes
        
        Args:
        self: The object pointer
        name: Name of the space object
        """
        try:
            obj = Ned.query_object(name)
        except Exception:
            return None
        coord = {}
        coord['ra'] = obj['RA(deg)'][0]
        coord['dec'] = obj['DEC(deg)'][0]
        return coord
