"""
Created on Aug 8, 2012

@author: Erin McKenney
"""

import unittest
import os
from core.component.run_MINE import RunMINE
from core import run_ext_prog
from core.utils import path_utils

class TestRunMINE(unittest.TestCase):

    platform = run_ext_prog.get_platform()

    def setUp(self):
        self.long_message = True
        self.data_dir = path_utils.get_data_dir() + "MINE/"
        self.working_dir = path_utils.get_data_dir() + "MINE/test_data/"

    def tearDown(self):
        pass

        # Parameters to check: infile, pdir, wdir, jobID, comparison='-allPairs', cv=0, c=15
        # INFILE_POSITION = 1
        # COMPARISON_STYLE_POSITION = 2
        # CV_THRESHOLD_POSITION = 3
        # CLUMPS_POSITION = 4
        # JOB_ID_POSITION = 5

    MINE = "java -jar MINE.jar" # MINE command call





