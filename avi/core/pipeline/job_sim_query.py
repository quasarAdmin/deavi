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

@package avi.core.pipeline.job_sim_query

--------------------------------------------------------------------------------

This module provides the simulation query job.
"""
from .job import job as parent
#from avi.models import TutorialModel #gaia_query_model

# FIXME:
from avi.log import logger
from avi.models import sim_query_model

class sim_query(parent):
    """@class sim_query
    The sim_query class provides the simulations query asynchronous job feature.
    
    It implementes the job interface and inherits the job_data attribute.

    @see job @link avi.core.pipeline.job
    @see job_data @link avi.core.pipeline.job_data
    """
    def start(self, data):
        """This method runs the simulations query job.

        This method will start an asynchronous query to the simulations server.

        The data parameter must have the following keys:

        total_mass -> defines the total mass.<br>
        virial_ratio -> defines the virial ratio.<br>
        half_mass_radius -> defines the half-mass radius.<br>
        fractal_dimension -> defines the fractal dimension.<br>
        mass_segregation_degree -> defines the degree of mass segregation.<br>
        binary_fraction -> defines the binary fraction.<br>

        The method will create a sim_query_model and save it. By saving the 
        model a sim_query_task will start asynchronously.

        Args:
        self: The object pointer.
        data: A dictionary containing the input data for the job.

        Returns:
        The job_data attribute. The ok attribute will be True always.

        @see avi.models.sim_query_model
        @sa avi.task.sim_query_task
        """
        # TODO: check errors
        self.job_data.data = None
        self.job_data.ok = False

        if not 'total_mass' in data:
            return self.job_data
        if not 'virial_ratio' in data:
            return self.job_data
        if not 'half_mass_radius' in data:
            return self.job_data
        if not 'fractal_dimension' in data:
            return self.job_data
        if not 'mass_segregation_degree' in data:
            return self.job_data
        if not 'binary_fraction' in data:
            return self.job_data

        aux = sim_query_model.objects.all()
        if not aux or aux == []:
            mname = 1
        else:
            mname = sim_query_model.objects.latest('pk').pk
        m = sim_query_model(name = str(mname),
                             total_mass = data['total_mass'],
                             virial_ratio = data['virial_ratio'],
                             half_mass_radius = data['half_mass_radius'],
                             fractal_dimension = float(data['fractal_dimension']),
                             mass_segregation_degree = float(data['mass_segregation_degree']),
                             binary_fraction = data['binary_fraction'])
        m.save()

        self.job_data.data = m
        self.job_data.ok = True
        return self.job_data
