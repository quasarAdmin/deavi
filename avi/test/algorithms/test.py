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
