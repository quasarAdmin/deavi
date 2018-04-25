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
along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
"""
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
