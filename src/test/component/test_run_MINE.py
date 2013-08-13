"""
Created on Aug 8, 2012

@author: Erin McKenney
"""

import unittest
import os
from core.component.run_MINE import RunMINE
from core import run_ext_prog
from core.utils import path_utils
from core.component import run_MINE, run_BLAST
import glob



class TestRunMINE(unittest.TestCase):

    platform = run_ext_prog.get_platform()

    def setUp(self):
        self.long_message = True
        self.data_dir = path_utils.get_data_dir() + "MINE/"
        self.working_dir = path_utils.get_data_dir() + "MINE/test_data/"

#        self.Blast_dir = data_dir + "BLAST/"
#        self.infile = data_dir + "AE014075_subTiny5.fasta"  #"AE014075_subSmall100.fasta"
#        self.e_value_cut_off = 1e-15
#        self.record_index = SeqIO.index(self.infile, "fasta")


    def tearDown(self):
        prefix = self.working_dir + "*"
        for ext in run_MINE.ALL_EXTS:
            for name in glob.glob(prefix + ext):
                os.remove(name)

        for name in glob.glob(self.working_dir + 't*.csv'):
            os.remove(name)



        # Parameters to check: infile, pdir, wdir, jobID, comparison='-allPairs', cv=0, c=15
        # INFILE_POSITION = 1
        # COMPARISON_STYLE_POSITION = 2
        # CV_THRESHOLD_POSITION = 3
        # CLUMPS_POSITION = 4
        # JOB_ID_POSITION = 5

    def test_RunMINE_init(self):
        infile_var = "Spellman.csv"
        jobID_var = "tOut"

        mine = RunMINE(infile=infile_var, pdir=self.data_dir, wdir=self.working_dir,
            jobID=jobID_var, comparison='-allPairs', cv=0.0, exp=0.6, clumps=15, check_exist=False)

        expected_infile = "%s%s" % (self.working_dir, infile_var)
        expected_outfile = "id=%s" % jobID_var
        expected = ["-jar", "MINE.jar", expected_infile, '-allPairs', "cv=0.0", "exp=0.6", "c=15", expected_outfile]
#        print expected
        self.assertEqual(mine.get_switch(), expected)

        mine = RunMINE(infile=infile_var, pdir=self.data_dir, wdir=self.working_dir,
                       jobID=jobID_var, comparison='-allPairs', cv=0.0, exp=0.6, clumps=15, check_exist=False,
                       csv_files=["f1", "f2", "f3"])
        self.assertEqual([self.working_dir + "f1", self.working_dir + "f2", self.working_dir + "f3"], mine.csv_files)


#    def test_file_not_exist(self):
#        infile_var = "file_inexistent.mconf"  # test infile
#        jobID_var = "tOut"
#
#        with self.assertRaises(IOError):
#            RunMINE(infile=infile_var, pdir=self.data_dir, wdir=self.working_dir,
#                jobID=jobID_var, comparison='-allPairs', cv=0.0, c=15, check_exist=True)

    def test_parameter_values(self):
        infile_var = "Spellman.csv"
        jobID_var = "tOut"
        mine = RunMINE(infile=infile_var, pdir=self.data_dir, wdir=self.working_dir,
            jobID=jobID_var, comparison='-allPairs', cv=0.0, clumps=15, check_exist=False)

        self.assertRaises(ValueError, mine.set_cv_threshold, 1.1)
        self.assertRaises(ValueError, mine.set_cv_threshold, 0)
        self.assertRaises(ValueError, mine.set_cv_threshold, -1)
        self.assertRaises(ValueError, mine.set_cv_threshold, -2.5)
        self.assertRaises(ValueError, mine.set_cv_threshold, "string")
        try:
            mine.set_cv_threshold("0.3")
        except ValueError as e:
            self.fail(e)

        self.assertRaises(ValueError, mine.set_clumping_factor, 1.1)
        self.assertRaises(ValueError, mine.set_clumping_factor, 0)
        self.assertRaises(ValueError, mine.set_clumping_factor, -1)
        self.assertRaises(ValueError, mine.set_clumping_factor, -2.5)
        self.assertRaises(ValueError, mine.set_clumping_factor, "string")
        try:
            mine.set_clumping_factor("3")
        except ValueError as e:
            self.fail(e)


    def test_outfile_already_exist(self):
        """
        check if out file already exists,
        maybe should not raise error, should
        TODO: maybe it should be handle it at different way, auto rename?
        """
        infile_var = "Spellman2.csv"
        jobID_var = "exist"

        mine = RunMINE(infile=infile_var, pdir=self.data_dir, wdir=self.working_dir,
            jobID=jobID_var, comparison="0", check_exist=False)
        mine.run(debug=0)
        with self.assertRaises(IOError):
            RunMINE(infile=infile_var, pdir=self.data_dir, wdir=self.working_dir,
                jobID=jobID_var, comparison="0", check_exist=True)
#                os.remove(self.working_dir + jobID_var+ "Results.csv")
#                os.remove(self.working_dir + jobID_var+ "Status.txt")

#    def test_check_outfile_exist(self):
#        """
#        want to check to make sure output files DO NOT exist, first (before running the program)
#        then run the program, and check:
#        if ./MINE finished running, should produce 2 out    put files
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
        infile_var = "Spellman2.csv"
        jobID_var = "tOut"

        mine = RunMINE(infile=infile_var, pdir=self.data_dir, wdir=self.working_dir,
        jobID=jobID_var, comparison="-allPairs", check_exist=False)
        mine.run(True)

        self.assertTrue(mine.check_outfiles_with_filetag_exist(self.working_dir + infile_var + "," + jobID_var))




    def test_merge_output_csv_to_MINE(self):
        outfile1 = self.working_dir + "test1.csv"
        outfile2 = self.working_dir + "test2.csv"
        outfile3 = self.working_dir + "test3.csv"
        data = dict({"GO:01": 1,
                     "GO:03": 2,
                     "GO:04": 2,
                     "GO:05": 1, })
        run_BLAST.output_csv(outfile1, "Sample", data)

        data = dict({"GO:01": 7,
                     "GO:02": 9,
                     "GO:04": 2,
                     "GO:05": 8, })
        run_BLAST.output_csv(outfile2, "Species", data)

        data = dict({"GO:01": 3,
                     "GO:02": 1,
                     "GO:03": 2,
                     "GO:04": 2,
                     "GO:05": 2,
                     "GO:06": 1,
                     "GO:07": 1})
        run_BLAST.output_csv(outfile3, "Something", data)

        outfile = self.working_dir + "test12.csv"
        csv_files = [outfile1, outfile2]
        run_MINE.merge_output_csv_to_MINE(outfile, csv_files)

        f = open(outfile, "r")
        expected_header = "Sample_0,Species_1\r\n"
        expected_content = ["1,7\r\n",
                            "2,0\r\n",
                            "2,2\r\n",
                            "1,8\r\n",
                            "0,9\r\n"]

        for i, line in enumerate(f):
            if i == 0:
                self.assertEqual(line, expected_header)
            else:
                self.assertIn(line, expected_content)
        self.assertEqual(i, 5)


        outfile = self.working_dir + "test123.csv"
        csv_files = [outfile1, outfile2, outfile3]
        run_MINE.merge_output_csv_to_MINE(outfile, csv_files, isMINE=False)
        f = open(outfile, "r")
        expected_header = "GOterm,Sample_0,Species_1,Something_2\r\n"
        expected_content = ["GO:01,1,7,3\r\n",
                            "GO:03,2,0,2\r\n",
                            "GO:04,2,2,2\r\n",
                            "GO:05,1,8,2\r\n",
                            "GO:02,0,9,1\r\n",
                            "GO:06,0,0,1\r\n",
                            "GO:07,0,0,1\r\n"]

        for i, line in enumerate(f):
            if i == 0:
                self.assertEqual(line, expected_header)
            else:
                self.assertIn(line, expected_content)
        self.assertEqual(i, 7)

        run_MINE.merge_output_csv_to_MINE(outfile, csv_files, isMINE=True)
        f = open(outfile, "r")
        expected_header = "Sample_0,Species_1,Something_2\r\n"
        expected_content = ["1,7,3\r\n",
                            "2,0,2\r\n",
                            "2,2,2\r\n",
                            "1,8,2\r\n",
                            "0,9,1\r\n",
                            "0,0,1\r\n",
                            "0,0,1\r\n"]

        for i, line in enumerate(f):
            if i == 0:
                self.assertEqual(line, expected_header)
            else:
                self.assertIn(line, expected_content)
        self.assertEqual(i, 7)
