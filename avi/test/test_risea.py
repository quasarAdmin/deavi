
import unittest

try:
    from avi.core.risea import risea
except ImportError:
    import sys, os
    path = os.path.abspath(os.path.dirname(__file__))
    index = path.find("test")
    #path = path[:index - 1]
    path = path[:index - 5]
    sys.path.append(path)
    from avi.core.risea import risea
    
class test_risea(unittest.TestCase):

    def test_init(self):
        r = risea().get()

if __name__ == '__main__':
    pass
    unittest.main()
