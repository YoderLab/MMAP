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

        metasim = RunMetaSim(model_file=model_infile_var, no_reads=no_reads_var,
            taxon_infile =taxon_infile_var, pdir=self.data_dir, wdir=self.working_dir,
            outfile=outfile_var, check_exist=True)

        expected_model_infile = "-mg %s%s"%(self.working_dir, model_infile_var)
        expected_taxon_infile = self.working_dir + taxon_infile_var
        expected_no_reads = "-r%s" % no_reads_var
        expected_outfile = "-d %s"%self.working_dir + "wdir_all_reads_out.fasta"
        expected = [expected_model_infile, expected_no_reads, expected_taxon_infile, expected_outfile]
#
#        self.assertEqual(metasim.get_switch()[0], "-mg %s%s"%(self.working_dir, model_infile_var))
#        self.assertEqual(metasim.get_switch()[1], expected_no_reads)
#        self.assertEqual(metasim.get_switch()[2], expected_taxon_infile)
#        self.assertEqual(metasim.get_switch()[3], expected_outfile)
        self.assertEqual(metasim.get_switch(), [expected_model_infile, expected_no_reads,expected_taxon_infile,expected_outfile])
        self.assertEqual(metasim.get_switch(), expected)

    def test_file_not_exist(self):
        model_infile_var = "file_inexistent.mconf"
        taxon_infile_var = "MetaSim_bint.mprf"
        outfile_var = "wdir_all_reads_out.fasta"
        no_reads_var = 100

        with self.assertRaises(IOError):
            RunMetaSim(model_file=model_infile_var, no_reads=no_reads_var,
            taxon_infile =taxon_infile_var, pdir=self.data_dir, wdir=self.working_dir,
            outfile=outfile_var, check_exist=True)

        model_infile_var = "ErrorModelSolexa36bp.mconf"
        taxon_infile_var = "bad_file.mprf"

        with self.assertRaises(IOError):
            RunMetaSim(model_file=model_infile_var, no_reads=no_reads_var,
                taxon_infile =taxon_infile_var, pdir=self.data_dir, wdir=self.working_dir,
                outfile=outfile_var, check_exist=True)

        taxon_infile_var = "MetaSim_bint.mprf"
        outfile_var = "incorrect_outfile.fasta"

        with self.assertRaises(IOError):
            RunMetaSim(model_file=model_infile_var, no_reads=no_reads_var,
                taxon_infile =taxon_infile_var, pdir=self.data_dir, wdir=self.working_dir,
                outfile=outfile_var, check_exist=True)

    def test_no_reads_value(self):
        model_infile_var = "ErrorModelSolexa36bp.mconf"
        taxon_infile_var = "MetaSim_bint.mprf"
        outfile_var = "wdir_all_reads_out.fasta"
        no_reads_var = -4

        with self.assertRaises(ValueError):
            RunMetaSim(model_file=model_infile_var, no_reads=no_reads_var,
                taxon_infile =taxon_infile_var, pdir=self.data_dir, wdir=self.working_dir,
                outfile=outfile_var, check_exist=True)

        no_reads_var = 4.782

        with self.assertRaises(ValueError):
            RunMetaSim(model_file=model_infile_var, no_reads=no_reads_var,
                taxon_infile =taxon_infile_var, pdir=self.data_dir, wdir=self.working_dir,
                outfile=outfile_var, check_exist=True)

        no_reads_var = "fourpointseven"

        with self.assertRaises(ValueError):
            RunMetaSim(model_file=model_infile_var, no_reads=no_reads_var,
                taxon_infile =taxon_infile_var, pdir=self.data_dir, wdir=self.working_dir,
                outfile=outfile_var, check_exist=True)

        no_reads_var = -4.782

        with self.assertRaises(ValueError):
            RunMetaSim(model_file=model_infile_var, no_reads=no_reads_var,
                taxon_infile =taxon_infile_var, pdir=self.data_dir, wdir=self.working_dir,
                outfile=outfile_var, check_exist=True)