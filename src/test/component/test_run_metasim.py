"""
Created on Mar 20, 2012

@author: Erin McKenney
"""

import unittest
import os
from core.component import run_MetaSim
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

    # Parameters to check: model_infile, no_reads, taxon_infile, pdir, wdir=None, filename=None
        # MODEL_INFILE_POSITION = 1
        # NO_READS_POSITION = 2
        # TAXON_INFILE_POSITION = 3
        # OUTFILE_DIRECTORY_POSITION = 4

    def test_init(self):
        model_infile_var = "ErrorModelSolexa36bp.mconf"
        taxon_infile_var = "MetaSim_bint.mprf"
        outfile_var = "wdir_all_reads_out.fasta"
        no_reads_var = 100

        metasim = RunMetaSim(model_file=model_infile_var, no_reads=no_reads_var,
            taxon_infile=taxon_infile_var, pdir=self.data_dir, wdir=self.working_dir,
            filename=outfile_var, check_exist=True)

        expected_model_infile = "-mg%s%s" % (self.working_dir, model_infile_var)
        expected_taxon_infile = self.working_dir + taxon_infile_var
        expected_no_reads = "-r%s" % no_reads_var
        expected_directory = "-d%s" % self.working_dir
        expected = ["cmd", expected_model_infile, expected_no_reads, expected_directory, expected_taxon_infile]
#
        self.assertEqual(metasim.get_all_switches(), expected)

    def test_file_not_exist(self):
        model_infile_var = "file_inexistent.mconf"  # test model_infile
        taxon_infile_var = "MetaSim_bint.mprf"
        outfile_var = "wdir_all_reads_out.fasta"
        no_reads_var = 100

        with self.assertRaises(IOError):
            RunMetaSim(model_file=model_infile_var, no_reads=no_reads_var,
            taxon_infile=taxon_infile_var, pdir=self.data_dir, wdir=self.working_dir,
            filename=outfile_var, check_exist=True)

        model_infile_var = "ErrorModelSolexa36bp.mconf"
        taxon_infile_var = "bad_file.mprf"  # test taxon_infile

        with self.assertRaises(IOError):
            RunMetaSim(model_file=model_infile_var, no_reads=no_reads_var,
                taxon_infile=taxon_infile_var, pdir=self.data_dir, wdir=self.working_dir,
                filename=outfile_var, check_exist=True)

        taxon_infile_var = "incorrect_bint.mprf"
        outfile_var = "incorrect_outfile.fasta"  # test filename

        with self.assertRaises(IOError):
            RunMetaSim(model_file=model_infile_var, no_reads=no_reads_var,
                taxon_infile=taxon_infile_var, pdir=self.data_dir, wdir=self.working_dir,
                filename=outfile_var, check_exist=True)

    def test_no_reads_value(self):
        model_infile_var = "ErrorModelSolexa36bp.mconf"
        taxon_infile_var = "MetaSim_bint.mprf"
        outfile_var = "wdir_all_reads_out.fasta"

        metasim = RunMetaSim(model_file=model_infile_var, no_reads=100,
            taxon_infile=taxon_infile_var, pdir=self.data_dir, wdir=self.working_dir,
            filename=outfile_var, check_exist=True)
        self.assertRaises(ValueError, metasim.set_number_of_reads, 1.9)
        self.assertRaises(ValueError, metasim.set_number_of_reads, -1)
        self.assertRaises(ValueError, metasim.set_number_of_reads, -2.5)
        self.assertRaises(ValueError, metasim.set_number_of_reads, "string")
        self.assertRaises(ValueError, metasim.set_number_of_reads, "3.6")
#        self.assertRaises(TypeError, metasim.set_number_of_reads, "3")
        metasim.set_number_of_reads("3")
        self.assertEqual(metasim.get_all_switches()[run_MetaSim.NO_READS_POSITION - 1], "-r3")

    def test_set_outfile_directory(self):
        model_infile_var = "ErrorModelSolexa36bp.mconf"
        taxon_infile_var = "MetaSim_bint.mprf"
        outfile_var = "wdir_all_reads_out.fasta"

        metasim = RunMetaSim(model_file=model_infile_var, no_reads=100,
            taxon_infile=taxon_infile_var, pdir=self.data_dir, wdir=self.working_dir,
            filename=outfile_var, check_exist=True)

        self.assertEqual(metasim.get_all_switches()[3], "-d%s" % self.working_dir)

        dir_var = self.data_dir
        metasim = RunMetaSim(model_file=model_infile_var, no_reads=100,
            taxon_infile=taxon_infile_var, pdir=self.data_dir, wdir=dir_var,
            filename=outfile_var, check_exist=False)
        metasim.set_outfile_directory()
        self.assertEqual(metasim.get_all_switches()[3], "-d%s" % self.data_dir)

#    def test_file_already_exist(self):
#        """
#        check if out file already exists,
#        maybe should not raise error, should
#        TODO: Should we just delete this, now that it names outfiles with version numbers?
#            - MetaSim has auto rename function, need to check filename
#        """
#        model_infile_var = "ErrorModelSolexa36bp.mconf"
#        taxon_infile_var = "MetaSim_bint.mprf"
#        outfile_var = self.working_dir + "MetaSim_bint-454.fna"
#        with self.assertRaises(IOError):
#            RunMetaSim(model_file=model_infile_var, no_reads=100,
#                taxon_infile=taxon_infile_var, pdir=self.data_dir, wdir=self.working_dir,
#                filename=outfile_var, check_exist=True)

    def test_check_outfile_exist(self):
        """
        check if ./MetaSim finished running, should produce 2 output files
        only pass if both exist
        TODO: need to check -d outfile_dir. MetaSim automatically change the filename name
        """
        model_infile_var = "ErrorModelSolexa36bp.mconf"
        taxon_infile_var = "MetaSim_bint.mprf"
        outfile_var = "MetaSim_bint-454.20e39f4c.fna"

        metasim = RunMetaSim(model_file=model_infile_var, no_reads=100,
            taxon_infile=taxon_infile_var, pdir=self.data_dir, wdir=self.working_dir,
            filename=outfile_var, check_exist=True)
        metasim.run()
        self.assertTrue(metasim.is_file_exist(self.working_dir + "MetaSim_bint-Empirical.fna"))


        # test for an additional run: able to append subsequent versions?
        metasim.run()
        self.assertTrue(metasim.is_file_exist(self.working_dir + "MetaSim_bint-Empirical.1.fna"))

        metasim.run()
        self.assertTrue(metasim.is_file_exist(self.working_dir + "MetaSim_bint-Empirical.2.fna"))

        os.remove(self.working_dir + "MetaSim_bint-Empirical.fna")
        os.remove(self.working_dir + "MetaSim_bint-Empirical.1.fna")
        os.remove(self.working_dir + "MetaSim_bint-Empirical.2.fna")

    def test_read_outfile(self):
        """
        check if it can "read" .fna
        TODO: have check what happen in the file format is invalid,
        assuming its the correct fasta now
        """
        model_infile_var = "ErrorModelSolexa36bp.mconf"
        taxon_infile_var = "MetaSim_bint.mprf"
        outfile_var = "MetaSim_bint-Empirical.fna"
        metasim = RunMetaSim(model_file=model_infile_var, no_reads=100,
            taxon_infile=taxon_infile_var, pdir=self.data_dir, wdir=self.working_dir,
            filename=outfile_var, check_exist=True)
        metasim.run()
        result = metasim.read_outfile()
        self.assertEqual(len(result), 2)
        self.assertEqual(result.keys(), ["1", "2"])

        expected = [170, 60]
        for i, key in enumerate(result):
        #            print key, i, type(result[key]), result[key]
            self.assertEqual(len(result[key]), expected[i])


    def test_RunMetaSim_run(self):
        model_infile_var = "ErrorModelSolexa36bp.mconf"
        taxon_infile_var = "MetaSim_bint.mprf"
        outfile_var = "MetaSim_bint-Empirical"
        metasim = RunMetaSim(model_file=model_infile_var, no_reads=100,
                             taxon_infile=taxon_infile_var, pdir=self.data_dir,
                             wdir=self.working_dir, filename=outfile_var, check_exist=True)
        self.assertFalse(metasim.is_file_exist(self.working_dir + "test_outfile.fasta", False))
        metasim.run(debug=True)
#        print "7777777", self.working_dir,outfile_var
        self.assertTrue(metasim.check_outfiles_with_filetag_exist(self.working_dir + outfile_var))
        self.assertTrue(metasim.is_file_exist(self.working_dir + outfile_var + ".fna", True))
        os.remove(self.working_dir + outfile_var + ".fna")
