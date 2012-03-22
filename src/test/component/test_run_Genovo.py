"""
Created on Mar 20, 2012

@author: Steven Wu
"""
import unittest
from core.component.run_Genovo import RunGenovo
from core import run_ext_prog
from core.utils import path_utils

class TestRunGenovo(unittest.TestCase):

    platform = run_ext_prog.get_platform()
        
    def setUp(self):
        self.data_dir = path_utils.get_data_dir()


    def tearDown(self):
        pass

    def test_RunGenovo_init(self):
        self.infile = "all_reads.fa"
        self.g1 = RunGenovo(self.infile, pdir=self.data_dir)
        self.assertEqual(self.g1.getSwitch()[0], self.infile)
#        self.assertEqual(self.g1.getSwitch(), [self.infile, 3])


