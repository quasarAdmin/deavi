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
import time
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
    
from avi.models import algorithm_info_model
from avi.models import algorithm_model

from avi.core.algorithm.algorithm_manager import algorithm_manager

class test_pipeline(unittest.TestCase):
    def __str__(self): return "test_pipeline."

    @classmethod
    def setUpClass(cls):
        pass
        """
        #test_info("Setting up the enviroment...", cls)
        input_dir = os.path.join(os.path.abspath(os.path.dirname(__file__))
                                 ,'input')
        alg_dir = os.path.join(os.path.abspath(os.path.dirname(__file__))
                               ,'algorithms')
        test_log("Input path: %s"%(input_dir),cls)
        test_log("Algorithms path: %s"%(alg_dir),cls)
        algorithm_info_model.objects.create(name="test",
                                            source_file=alg_dir + "/test.py",
                                            name_view="Test View",
                                            definition_file=alg_dir + 
                                            "/test.json",
                                            algorithm_type="installed")
        """
    @classmethod
    def tearDownClass(cls):
        """
        test_log("teardownclass",cls)
        alg_info = algorithm_info_model.objects.all()
        for i in alg_info:
            i.delete()
        """

    def setUp(self):
        test_log("setup",self)

    def tearDown(self):
        test_log("teardown",self)

    # AUX ######################################################################

    def _post_exec_algorithm(self, pk = 1, name = "test", p1 = 0, 
                             p2 = 0, p3 = 0, p4 = 0, p5 = "" , p6 = "" , 
                             p7 = ""):
        ret = {str(pk)+"_p1": [p1],
               str(pk)+"_p2": [p2],
               str(pk)+"_p3": [p3],
               str(pk)+"_p4": [p4],
               str(pk)+"_p5": [p5],
               str(pk)+"_p6": [p6],
               str(pk)+"_p7": [p7]}
        return ret
        
    def _post_abort(self, type='algorithm', pk = 1):
        ret = {'type': type,
               'pk': pk}
        return ret

    def _delete_algorithm_info(self):
        alg_info = algorithm_info_model.objects.all()
        for i in alg_info:
            i.delete()

    # TESTS ####################################################################

    def test_job_abort_start_ok(self):
        input_dir = os.path.join(os.path.abspath(os.path.dirname(__file__))
                                 ,'input')
        alg_dir = os.path.join(os.path.abspath(os.path.dirname(__file__))
                               ,'algorithms')
        test_log("Input path: %s"%(input_dir),self)
        test_log("Algorithms path: %s"%(alg_dir),self)
        algorithm_info_model.objects.create(name="test",
                                            source_file=alg_dir + "/test.py",
                                            name_view="Test View",
                                            definition_file=alg_dir + 
                                            "/test.json",
                                            algorithm_type="installed")
        #test_info("Starting...",self)
        pk = 1
        try:
            alg_info = algorithm_info_model.objects.get(pk=pk)
        except algorithm_info_model.DoesNotExist:
            #test_info("[FAILED]",self)
            self.assertTrue(False)
        
        mng = algorithm_manager()
        self.assertIsNotNone(mng)
        
        post = self._post_exec_algorithm(pk, alg_info.name, p5="WAIT_ABORT")

        alg_input = mng.get_algorithm_data(str(pk),
                                           alg_info.name,
                                           alg_info.definition_file,
                                           post)
        alg_exec = algorithm_model.objects.create(alg_name = alg_info.name,
                                                  params = alg_input,
                                                  results = {})
        alg_exec.save()

        while alg_exec.request.pipeline_state.state != 'PENDING': #'STARTED':
            try:
                alg_exec = algorithm_model.objects.get(pk=pk)
            except algorithm_model.DoesNotExist:
                #test_info("[FAILED]", self)
                self.assertTrue(False)
            #test_info(alg_exec.request.pipeline_state.state)
            time.sleep(1)
        status = alg_exec.request.pipeline_state.state
        self.assertNotEqual(status, 'FAILURE')
        self.assertNotEqual(status, 'SUCCESS')
        self.assertFalse(alg_exec.is_aborted)

        from avi.core.pipeline.job_abort import abort
        res = abort().start(self._post_abort('algorithm', pk))
        
        self.assertTrue(res.ok)

        try:
            alg_exec = algorithm_model.objects.get(pk=pk)
        except algorithm_model.DoesNotExist:
            #test_info("[FAILED]", self)
            self.assertTrue(False)

        #test_info(str(res.data.params))

        #test_info(str(alg_exec.params))

        #while alg_exec.request.pipeline_state.state != 'FAILURE':
        #test_info(alg_exec.request.pipeline_state.state)
        #    time.sleep(1)
        
        status = alg_exec.request.pipeline_state.state
        self.assertEqual(status, 'FAILURE')
        self.assertTrue(alg_exec.is_aborted)
                                                  
        #test_info("[DONE]",self)
        #self._delete_algorithm_info()

    def test_job_abort_start_nok(self):
        pass
        #test_info("Starting...",self)
        #test_info("[DONE]",self)

if __name__ == '__main__':
    unittest.main()
