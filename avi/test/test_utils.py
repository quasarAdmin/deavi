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
import os
import unittest

try:
    from avi.tests import *
except ImportError:
    import sys, os
    path = os.path.abspath(os.path.dirname(__file__))
    index = path.find("test")
    path = path[:index - 5]
    sys.path.append(path)
    from avi.tests import *
    
import numpy as np
from astropy.io import fits
from astropy.io.votable.tree import VOTableFile, Resource, Table, Field
from bokeh.plotting import figure

from avi.utils.data.data_file import data_file
from avi.utils.plotter import save_plot
from avi.models import results_model
from avi.models import plot_model
from avi.warehouse import wh_global_config as wh

class test_utils(unittest.TestCase):
    def __str__(self): return "test_utils."

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # TEST #####################################################################

    def test_data_file(self):
        wh().get().RESULTS_PATH = os.path.dirname(os.path.realpath(__file__))
        
        test_log("Testing the initialization...", self)
        job_id = 1
        fname = "test_data.dat"
        model = results_model.objects.filter(job_id=job_id)
        self.assertFalse(model)
        d = data_file(1)
        model = results_model.objects.filter(job_id=job_id)
        self.assertEqual(len(model),1)

        test_log("Testing a simple file creation...", self)
        file_name = os.path.join(wh().get().RESULTS_PATH, fname)
        f = d.file(fname)
        f.write("test")
        f.close()
        model = results_model.objects.filter(job_id=job_id)
        self.assertEqual(wh().get().RESULTS_PATH, model[0].resources.all().filter(name=fname)[0].path)
        self.assertEqual(fname, model[0].resources.all().filter(name=fname)[0].name)
        self.assertTrue(os.path.isfile(file_name))
        f = open(file_name)
        fdata = f.read()
        f.close()
        self.assertEqual(fdata,"test")
        os.remove(file_name)

        test_log("Testing a plot addition...", self)
        plot = plot_model.objects.create(name="test_plot",
                                         job_id=job_id,
                                         alg_name="test",
                                         script="",
                                         html="")
        self.assertFalse(model[0].plots.all().filter(name="test_plot"))
        d.add_plot(plot)
        self.assertEqual(len(model[0].plots.all().filter(name="test_plot")), 1)

        test_log("Testing a FITS file storage...", self)
        n = np.arange(100.0)
        hdu = fits.PrimaryHDU(n)
        hdul = fits.HDUList([hdu])
        d.save_fits(fname, hdul)
        self.assertEqual(len(model[0].resources.all().filter(name=fname)),2)
        self.assertTrue(os.path.isfile(file_name))
        os.remove(file_name)

        test_log("Testing a VOTable file storage...", self)
        votable = VOTableFile()
        resource = Resource()
        votable.resources.append(resource)
        table = Table(votable)
        resource.tables.append(table)
        table.fields.extend([
            Field(votable, name="filename", datatype="char", arraysize="*"),
            Field(votable, name="matrix", datatype="double", arraysize="2x2")])
        table.create_arrays(2)
        table.array[0] = ('test_1', [[1, 0], [0, 1]])
        table.array[1] = ('test_2', [[0.5, 0.3], [0.2, 0.1]])
        d.save_vot(fname, votable)
        self.assertEqual(len(model[0].resources.all().filter(name=fname)),3)
        self.assertTrue(os.path.isfile(file_name))
        os.remove(file_name)

    def test_plotter(self):
        test_log("Testing the plotter...", self)
        job_id = 1
        plot = figure(plot_width=400, plot_height=400)
        model = results_model.objects.filter(job_id=job_id)
        self.assertFalse(model[0].plots.all().filter(name="name"))
        save_plot(job_id, "test_plotter", plot)
        self.assertEqual(len(model[0].plots.all().filter(name="name")), 1)
        
        
    def test_file_manager(self):
        pass
        
    def test_resources_manager(self):
        pass

    def test_json_manager(self):
        pass
    
    def test_config_manager(self):
        pass
        
    def test_coordinates_manager(self):
        pass

    def test_adql_helper(self):
        pass

if __name__ == '__main__':
    unittest.main()
