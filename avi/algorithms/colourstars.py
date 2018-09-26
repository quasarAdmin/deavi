import itertools
import numpy as np
from numpy import *

from astropy.io.votable.tree import VOTableFile, Resource, Table, Field
from astropy.io import fits
from astropy.io.votable import parse

from avi.utils.plotter import save_plot
from avi.log import logger
from avi.utils.plotter import save_plot
from avi.utils.data.data_file import data_file as data

from bokeh.plotting import figure
from bokeh.palettes import Category10
from bokeh.plotting import figure, output_file, show
from bokeh.models import Arrow, OpenHead, NormalHead, VeeHead

class colourstars:
    gaia_file = ""
    n_stars=0.0
    def run(self, id):
        gaia_data = parse(self.gaia_file)
        gaia_list = gaia_data.get_first_table().array
        paralf=gaia_list['parallax']/1000
        paralf=paralf[0:self.n_stars]
        elmt=[]
        dec_colf = gaia_list['dec']
        ra_colf = gaia_list['ra']
        radiof = gaia_list['radius_val']
        temp= gaia_list['teff_val']
        for l in range (len(paralf)):
            if type(temp[l]) != np.ma.core.MaskedConstant:
                elmt.append(l)
        dec_colf_new  = np.zeros(len(elmt))
        ra_colf_new  = np.zeros(len(elmt))
        paral_new=np.zeros(len(elmt))
        radiof_new=np.zeros(len(elmt))
        tempf_new=np.zeros(len(elmt))
        for j in range(len(elmt)):
            dec_colf_new[j]  = dec_colf[elmt[j]]
            ra_colf_new[j]  = ra_colf[elmt[j]]
            paral_new[j] = paralf[elmt[j]]
            radiof_new[j] = radiof[elmt[j]]
            tempf_new[j] = temp[elmt[j]]
        dist = 1/ abs (paral_new)
        x = ra_colf_new
        y = dec_colf_new
        max_ra = max(ra_colf_new)+0.25
        min_ra = min(ra_colf_new)-0.25
        max_de = max(dec_colf_new)+0.25
        min_de = min(dec_colf_new)-0.25
        
        def colourstars(x, y, tempf_new, min_ra, max_ra, min_de, max_de):
             p=figure(title="Color stars", x_range=(min_ra,max_ra), y_range=(min_de,max_de))
             p.xaxis.axis_label = "Right ascension (degrees)"
             p.yaxis.axis_label = "Declination (degrees)"
             for k in range(len(elmt)):
                 if tempf_new[k]>10000:
                     p.circle(x, y, radius =0.008,color="#00BFFF")#blue
                 if tempf_new[k]<10000 and tempf_new[k]>6000:
                     p.circle(x, y, radius =0.008,color="#E0FFFF")#white-blue
                 if tempf_new[k]<6000 and tempf_new[k]>4900:
                     p.circle(x, y, radius =0.008,color="#FFFF00")#yellow
                 if tempf_new[k]<4900 and tempf_new[k]>3500:
                     p.circle(x, y, radius =0.008,color="#FFA500")#orange
                 if tempf_new[k]<3500:
                     p.circle(x, y, radius =0.008,color="#FF0000")#red
             p.xaxis.axis_label = "Right ascension (degrees)"
             p.yaxis.axis_label = "Declination (degrees)"
             save_plot(id, "gaia", p)
        p=colourstars(x, y, tempf_new, min_ra, max_ra, min_de, max_de)