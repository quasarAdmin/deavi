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
"""
class test:
    p1 = 0
    p2 = 0
    p3 = 0
    p4 = 0
    p5 = ""
    p6 = ""
    p7 = ""
    def run(self, id):
        if self.p5 == "SLEEP":
            import time
            time.sleep(20)
        elif self.p5 == "WAIT_ABORT":
            while True:
                continue
        elif self.p5 == "CRASH":
            notvalidpython
        elif self.p5 == "EXEC":
            f = open(self.p6,'w')
            f.write(str(self.p1))
            f.write("\n")
            f.write(str(self.p2))
            f.write("\n")
            f.write(str(self.p3))
            f.write("\n")
            f.write(str(self.p4))
            f.write("\n")
            f.write(self.p5)
            f.write("\n")
            f.write(self.p6)
            f.write("\n")
            f.write(self.p7)
            f.close()
