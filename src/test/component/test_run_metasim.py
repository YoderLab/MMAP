"""
Created on Mar 20, 2012

@author: Erin McKenney
"""

import unittest
import os
from core.component.run_MetaSim import RunMetaSim
from core import run_ext_prog
from core.utils import path_utils

class TestRunMetaSim(unittest.TestCase):

    platform = run_ext_prog.get_platform()

    def setUp(self):
        self.long_message = True
        self.data_dir = path_utils.get_data_dir() + "MetaSim/"
        self.working_dir = path_utils.get_data_dir() + "MetaSim/test_data/"

    def tearDown(self):
        pass

    # Parameters to check: model_infile, no_reads, taxon_infile, pdir, wdir=None, outfile=None
        # MODEL_INFILE_POSITION = 1
        #NO_READS_POSITION = 2
        #TAXON_INFILE_POSITION = 3
        #OUTFILE_DIRECTORY_POSITION = 4

    def test_RunMetaSim_init(self):
        model_infile_var = "ErrorModelSolexa36bp.mconf"
        taxon_infile_var = "MetaSim_bint.mprf"
        outfile_var = "wdir_all_reads_out.fasta"
        no_reads_var = 100

        metasim = RunMetaSim(model_infile_var, no_reads_var,
            taxon_infile =self.working_dir + taxon_infile_var, pdir=self.data_dir, wdir=self.working_dir,
            outfile=self.working_dir+outfile_var, check_exist=False)

        expected_model_infile = self.working_dir + model_infile_var
        expected_taxon_infile = self.working_dir + taxon_infile_var

        expected = [expected_model_infile, "100", expected_taxon_infile, self.working_dir + "wdir_all_reads_out.fasta"]

        self.assertEqual(metasim.get_switch()[0], self.working_dir + model_infile_var)
        self.assertEqual(metasim.get_switch(), [expected_model_infile, "1"])
        self.assertEqual(metasim.get_switch(), expected)

