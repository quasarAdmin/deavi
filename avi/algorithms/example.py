from avi.log import logger

from astropy.io import fits
from astropy.io.fits import CompImageHDU
from astropy.wcs import WCS
from astropy.io.votable import parse

from bokeh.plotting import figure
from bokeh.models import (LogColorMapper, LogTicker, 
                          ColorBar, LabelSet, ColumnDataSource)

import numpy as np

from avi.utils.plotter import save_plot
from avi.utils.data.data_file import data_file as data

class example:
    gaia_table = ""
    gaia_table2 = ""
    hsa_table = ""
    def run(self, id):
        gaia_file = parse(self.gaia_table)
        # ---------------- Fix me -------------------
        #hsa_file = fits.open(self.hsa_table)
        hsa_file = fits.open(self.hsa_table)
        #hsa_file = fits.open("/data/output/data.fits")

        gaia_list = gaia_file.get_first_table().array
        dec_col = gaia_list['dec']
        ra_col = gaia_list['ra']
        
        image_data = hsa_file[1].data
        #CompImageHDU(hsa_file[1].data,hsa_file[0].header)
        
        ##from astropy.visualization.scripts import fits2bitmap
        ##fits2bitmap.fits2bitmap(filename = self.hsa_table, ext=1, 
                                #stretch = 'asinh',
        ##                        percent = 0.5,
        ##                        asinh_a = 10,
                                #min_percent=0.1, max_percent=100, 
        ##                        cmap='hot',
        ##                        out_fn = '/data/output/test.png')

        tools = "pan,wheel_zoom,box_zoom,reset,save"
        
        from astropy.nddata import block_reduce, block_replicate
        small = block_reduce(image_data, 8)
        
        color_mapper = LogColorMapper(palette="Viridis256", low=10, high=80)
        
        ##from scipy import misc
        ##data = misc.imread('/data/output/test.png')

        ##data = data[:,:,1]
        image_data = small
        plot = figure(title="Gaia and HSA", 
                      #plot_width=data.shape[0],
                      #plot_height=data.shape[1])
                      x_range=(0,small.shape[0]), 
                      y_range=(0,small.shape[1]), toolbar_location="right")
#         plot.add_tools(WheelZoomTool())
        
        plot.image(image=[small], color_mapper=color_mapper,
                  dh=[small.shape[0]], dw=[small.shape[1]], 
                  x=[0], y=[0])
        #plot.image_url(url=['/data/output/test.png'], x=0, y=1, w=100, h=100)
                       #w=image_data.shape[0],h=image_data.shape[1])
        #plot.axis.visible = False
        #from bokeh.io import export_png
        #export_png(plot, filename="/data/output/plot.png")
        save_plot(id, "example", plot)

        plot = figure(title="Gaia and HSA", tools=tools, 
                      #plot_width=data.shape[0],
                      #plot_height=data.shape[1])
                      x_range=(0,small.shape[0]), 
                      y_range=(0,small.shape[1]), toolbar_location="below")
        
        plot.image(image=[small], color_mapper=color_mapper,
                  dh=[small.shape[0]], dw=[small.shape[1]], 
                  x=[0], y=[0])
        #plot.image_url(url=['/data/output/test.png'], x=0, y=1, w=100, h=100)
                       #w=image_data.shape[0],h=image_data.shape[1])
        #plot.axis.visible = False
        #from bokeh.io import export_png
        #export_png(plot, filename="/data/output/plot.png")
        save_plot(id, "example", plot)
        
        plot = figure(plot_width=400,tools=tools,
                      plot_height=400, toolbar_location="right")
        plot.circle(dec_col, ra_col, fill_color="red", size=2)
        save_plot(id, "example gaia", plot)
