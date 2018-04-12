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
    hsa_table = ""
    def run(self, id):

        tools = "pan,wheel_zoom,box_zoom,reset,save"

        if self.gaia_table and self.gaia_table != "":
            try:
                gaia_file = parse(self.gaia_table)
                gaia_list = gaia_file.get_first_table().array
                dec_col = gaia_list['dec']
                ra_col = gaia_list['ra']
            
                plot = figure(plot_width=400,tools=tools,
                              plot_height=400, toolbar_location="right")
                plot.circle(dec_col, ra_col, fill_color="red", size=2)
                save_plot(id, "example gaia", plot)
            except Exception:
                pass
            except IsADirectoryError:
                pass

        if self.hsa_table and self.hsa_table != "":

            try:
            
                hsa_file = fits.open(self.hsa_table)
                
                image_data = hsa_file[1].data
            
                from astropy.nddata import block_reduce, block_replicate
                small = block_reduce(image_data, 8)
                
                color_mapper = LogColorMapper(palette="Viridis256", low=10, high=80)
        
                image_data = small
                plot = figure(title="Gaia and HSA", 
                              x_range=(0,small.shape[0]), 
                              y_range=(0,small.shape[1]), toolbar_location="right")
                
                plot.image(image=[small], color_mapper=color_mapper,
                           dh=[small.shape[0]], dw=[small.shape[1]], 
                           x=[0], y=[0])
                save_plot(id, "example", plot)

            except Exception:
                try:
                    hsa_file = parse(self.hsa_table)
                    hsa_list = hsa_file.get_first_table().array
                    dec_col = hsa_list['dec']
                    ra_col = hsa_list['ra']
            
                    plot = figure(plot_width=400,tools=tools,
                                  plot_height=400, toolbar_location="right")
                    plot.circle(dec_col, ra_col, fill_color="red", size=2)
                    save_plot(id, "example hsa", plot)
                except Exception:
                    pass
                except IsADirectoryError:
                    pass
            except IsADirectoryError:
                pass
