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

#This algorithm plots the positions of a certain number of stars in a cluster together with their respective proper motions

class simple_algorithm:
    gaia_file = ""
    hsa_file = ""
    n_stars=0.0
    def run(self, id):
        #Selection of a query of gaia
        gaia_data = parse(self.gaia_file)
        gaia_list = gaia_data.get_first_table().array
        #Parallax obtained from gaia from the different stars changing units from mas to arcseconds
        paralf =gaia_list['parallax']/1000
        #Selection a smaller number of stars (n_stars) from all of the ones of the query
        #paralf=paralf[0:100]
        paralf=paralf[0:self.n_stars]
        
        #Obtention of the coordinates, proper motions and radius of the stars in the cluster
        propermot_de_sf= gaia_list['pmdec']
        propermot_ra_sf= gaia_list['pmra']
        dec_colf = gaia_list['dec']
        ra_colf = gaia_list['ra']
        radiof = gaia_list['radius_val']
        
        #Creation of an array that will contain only  the number of the rows of stars with a known proper motion (DR2)
        elmt=[]
        for l in range (len(paralf)):
            if type(propermot_de_sf[l]) != np.ma.core.MaskedConstant:
                elmt.append(l)

        
        #Creation of vectors with a lenght equal to the number of stars with a known proper motion
        lgtn=len(elmt)
        propermot_de_sf_new = np.zeros(lgtn)
        propermot_ra_sf_new  = np.zeros(lgtn)
        dec_colf_new  = np.zeros(lgtn)
        ra_colf_new  = np.zeros(lgtn)
        paral_new=np.zeros(lgtn)
        radiof_new=np.zeros(lgtn)
        
        #Function that fills the empty vectors with the real data from gaia, including only the stars with a known proper motion 
        for j in range(lgtn):
            #The proper motions are given in arcseconds per year so they are divided by a factor of 3600 to change the units to degrees
            propermot_de_sf_new [j]= propermot_de_sf[elmt[j]]/3600
            propermot_ra_sf_new [j]= propermot_ra_sf[elmt[j]]/3600
            dec_colf_new[j]  = dec_colf[elmt[j]]
            ra_colf_new[j]  = ra_colf[elmt[j]]
            paral_new[j] = paralf[elmt[j]]
            radiof_new[j] = radiof[elmt[j]]
        
        #Distance to the stars in parsecs    
        dist = 1/ abs (paral_new)
        
        #Definition of the variables that will be used to plot the coordinates of the stars in 2D (right ascension and declination in degrees)
        x = ra_colf_new
        y = dec_colf_new
        
        #Definition of the variables that will be used to plot the proper motions of the stars in 2D in degrees per year (they are multiplied by a factor of 10 to make the proportions more visually understandable in the plot)
        u=propermot_ra_sf_new*10
        v=propermot_de_sf_new*10
        #Calculations of the length and angle of the proper motion vector of each star (It is not used in this function but it could have been if another method was used)
        lenght = np.sqrt(u**2 + v**2)
        #Normalization of the vector
        max_lenght = max(lenght)
        leng = lenght / max_lenght
        #Angle in radians
        z = np.arctan2(u,v)
        #angle in degrees
        angl = np.rad2deg(z)
        
        #Normalization of the radius for plotting the stars proportional to their real size
        #max_radi=max(radi)
        #Correction factor to have a proper size for the graph
        #radius = radi/max_radi
        
        #Definition of the graph range and selection of an adequate margin
        margin = 0.07
        max_ra = max(ra_colf_new) + margin
        min_ra = min(ra_colf_new) - margin
        max_de = max(dec_colf_new) + margin
        min_de = min(dec_colf_new) - margin
        
        #Definition of the function that plots the stars and the arrows that represent the proper motions
        def radvel(x,y,max_ra, min_ra, max_de, min_de, u ,v):
            #Creation of the image
            p = figure(title="Proper motions", x_range=(min_ra,max_ra), y_range=(min_de,max_de))
            #Creation of the points that represent the stars and their color
            p.circle(x, y, color="#FFD700", line_color="#FF8C00" ,radius = 0.001)
            #Title of the axis and units
            p.xaxis.axis_label = "Right ascension (Degrees)"
            p.yaxis.axis_label = "Declination (Degrees)"     
            #Creation of the arrows of each star representing their proper motions. The color is chosen too.
            for k in range (len(x)):
                p.add_layout(Arrow(end=VeeHead(size=4), line_color="black", x_start=x[k], y_start=y[k], x_end=x[k]+u[k], y_end=y[k]+v[k]))
            show (p)
            save_plot(id, "gaia", p)  # open a browser
        #The function above is called to obtain the wanted graph
        p = radvel(x,y,max_ra, min_ra, max_de, min_de, u , v)

        res = self.n_stars
        my_file = data(id).file("my_results.txt")
        my_file.write(str(res))
        my_file.close()
        