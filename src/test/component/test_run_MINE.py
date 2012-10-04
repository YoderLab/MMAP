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

    def test_RunMINE_init(self):
        infile_var = "Spellman.csv"
        jobID_var = "Spellman.csv_output"

        mine = RunMINE(infile=infile_var, pdir=self.data_dir, wdir=self.working_dir,
            jobID=jobID_var, comparison='-allPairs', cv=0.0, c=15, check_exist=False)

        expected_infile = "%s%s" % (self.working_dir, infile_var)
        expected_outfile = "%s%s" % (self.working_dir, jobID_var)
        expected = ["-jar", "MINE.jar", expected_infile, '-allPairs', "0.0", "15", expected_outfile]
#        print expected
        self.assertEqual(mine.get_switch(), expected)

    def test_file_not_exist(self):
        infile_var = "file_inexistent.mconf"  # test infile
        jobID_var = "Spellman.csv,mv=0,cv=0.0,B=n^0.6,"

        with self.assertRaises(IOError):
            RunMINE(infile=infile_var, pdir=self.data_dir, wdir=self.working_dir,
                jobID=jobID_var, comparison='-allPairs', cv=0.0, c=15, check_exist=True)

    def test_parameter_values(self):
        infile_var = "Spellman.csv"
        jobID_var = "Spellman.csv,mv=0,cv=0.0,B=n^0.6,"
        mine = RunMINE(infile=infile_var, pdir=self.data_dir, wdir=self.working_dir,
            jobID=jobID_var, comparison='-allPairs', cv=0.0, c=15, check_exist=False)

        self.assertRaises(ValueError, mine.set_cv_threshold, 1.1)
        self.assertRaises(ValueError, mine.set_cv_threshold, -1)
        self.assertRaises(ValueError, mine.set_cv_threshold, -2.5)
        self.assertRaises(TypeError, mine.set_cv_threshold, "string")
        self.assertRaises(TypeError, mine.set_cv_threshold, "3")

        self.assertRaises(ValueError, mine.set_clumping_factor, 1.1)
        self.assertRaises(ValueError, mine.set_clumping_factor, 0)
        self.assertRaises(ValueError, mine.set_clumping_factor, -1)
        self.assertRaises(ValueError, mine.set_clumping_factor, -2.5)
        self.assertRaises(TypeError, mine.set_clumping_factor, "string")
        self.assertRaises(TypeError, mine.set_clumping_factor, "3")

    def test_file_already_exist(self):
        """
        check if out file already exists,
        maybe should not raise error, should
        TODO: maybe it should be handle it at different way, auto rename?
        """
        infile_var = "Spellman.csv"
        jobID_var = "Spellman.csv,mv=0,cv=0.0,B=n^0.6,"

        mine = RunMINE(infile=infile_var, pdir=self.data_dir, wdir=self.working_dir,
            jobID=jobID_var, comparison="0", cv=0.0, c=15, check_exist=False)
        mine.run(debug=True)
        with self.assertRaises(IOError):
            RunMINE(infile=infile_var, pdir=self.data_dir, wdir=self.working_dir,
                jobID=jobID_var, comparison='-allPairs', cv=0.0, c=15, check_exist=True)
#                os.remove(self.working_dir + jobID_var+ "Results.csv")
#                os.remove(self.working_dir + jobID_var+ "Status.txt")

#    def test_check_outfile_exist(self):
#        """
#        want to check to make sure output files DO NOT exist, first (before running the program)
#        then run the program, and check:
#        if ./MINE finished running, should produce 2 output files
#        only pass if both exist
#        """
#        infile_var = "Spellman.csv"
#        jobID_var = "Spellman.csv,mv=0,cv=0.0,B=n^0.6,"
#
#        mine = RunMINE(infile=infile_var, pdir=self.data_dir, wdir=self.working_dir,
#            jobID=jobID_var, comparison='-allPairs', cv=0.0, c=15, check_exist=True)
#        self.assertTrue(mine.is_file_exist(self.working_dir + "Spellman.csv,mv=0,cv=0.0,B=n^0.6,Results.csv"))
#        self.assertTrue(mine.is_file_exist(self.working_dir + "Spellman.csv,mv=0,cv=0.0,B=n^0.6,Status.txt"))


#    def test_read_outfile(self):
#        """
#        check if it can "read" .csv
#        TODO: have check what happen in the file format is invalid,
#        assuming its the correct fasta now
#        """
#        ...for now, can only check to make sure output file is not empty.#

    def test_RunMINE_run(self):
        infile_var = "Spellman.csv"
        jobID_var = "Spellman.csv,mv=0,cv=0.0,B=n^0.6,"

        mine = RunMINE(infile=infile_var, pdir=self.data_dir, wdir=self.working_dir,
        jobID=jobID_var, comparison="0", cv=0.0, c=15, check_exist=False)
        mine.run(True)
#        RunMINE(infile=infile_var, pdir=self.data_dir, wdir=self.working_dir,
#            jobID=jobID_var, comparison='-allPairs', cv=0.0, c=15, check_exist=True)
        self.assertTrue(mine.check_outfiles_exist(self.working_dir + jobID_var))
        self.assertTrue(mine.is_file_exist(self.working_dir + jobID_var + "Results.csv"))
        self.assertTrue(mine.is_file_exist(self.working_dir + jobID_var + "Status.txt"))
#        os.remove(self.working_dir + jobID_var+ "Results.csv")
#        os.remove(self.working_dir + jobID_var+ "Status.txt")


    def test_matrix(self):
        m = [[]] * 10
        for i in range(10):
            m[i] = i
        print m