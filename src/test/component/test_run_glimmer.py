"""
Created on April 9, 2012

@author: Erin McKenney
"""

import unittest
from core.component.run_glimmer import RunGlimmer
from core import run_ext_prog
from core.utils import path_utils
import os
import glob
from core.component import run_glimmer


class TestRunGlimmer(unittest.TestCase):
    """
    TODO: Remove some output files that should be generate from running the program
    maybe separate the name by the nature of the test
    iterated_run             - files ONLY exist after running the program
    iterated_preExistFile    - files exist without running the program 
    
    maybe different prefix as well?!? 
    """
    platform = run_ext_prog.get_platform()

    def setUp(self):
        """
        TODO: add wdir section
        """
        self.maxDiff = None
        self.long_message = True
        self.data_dir = path_utils.get_data_dir() + "Glimmer/"
#        self.working_dir = path_utils.get_data_dir() + "Glimmer/test_data/"

    def tearDown(self):
        prefix = self.data_dir + "*"
        for ext in run_glimmer.ALL_EXTS:
            for name in glob.glob(prefix + ext):
                os.remove(name)


    def test_RunGlimmer_init(self):
        infile_var = "all_reads.fa"

        test_glimmer = RunGlimmer(infile_var, pdir=self.data_dir, check_exist=False)
        self.assertEqual(test_glimmer.get_switch()[0], self.data_dir + infile_var)
        expected = [self.data_dir + infile_var, self.data_dir + "all_reads.glimmer.coords",
                    " > ", self.data_dir + "all_reads.glimmer"]
        self.assertEqual(test_glimmer.get_switch(), expected)


    def test_RunGlimmer_set_infile(self):

        infile_var = "test_infile.fasta"
        outfile_var = "testOutfile"
        extract = RunGlimmer(infile=infile_var, outfile=outfile_var, pdir=self.data_dir, check_exist=False)
        expected = [self.data_dir + infile_var, self.data_dir + outfile_var + ".coords", " > ", self.data_dir + outfile_var]
        self.assertEqual(extract.get_switch(), expected)
#        orf_var = "testORF"
#        extract = RunGlimmer(infile=infile_var, filename=outfile_var, orfs=orf_var, pdir=self.data_dir, check_exist=False)
#        self.assertEqual(3, len(extract.get_switch()))
#        self.assertEqual(extract.get_switch(), [self.data_dir + infile_var, self.data_dir + outfile_var,
#                                                self.data_dir + orf_var])

        infile_var = "VICTORY.fasta"
        extract.set_infile_name(infile_var)
        expected = [ infile_var, self.data_dir + outfile_var + ".coords", " > ", self.data_dir + outfile_var]
        self.assertEqual(extract.get_switch(), expected)

    def test_RunGlimmer_set_outfile(self):

        infile_var = "test_infile.fasta"
        outfile_var = "testOutfile"

        extract = RunGlimmer(infile=infile_var, outfile=outfile_var, pdir=self.data_dir, check_exist=False)
        self.assertEqual(4, len(extract.get_switch()))
        expected = [self.data_dir + infile_var, self.data_dir + outfile_var + ".coords", " > ", self.data_dir + outfile_var]
        self.assertEqual(extract.get_switch(), expected)


        infile_var = "test_infile.xyz.fasta.abc"
        extract = RunGlimmer(infile=infile_var, outfile=outfile_var, pdir=self.data_dir, check_exist=False)
        expected = [self.data_dir + infile_var, self.data_dir + outfile_var + ".coords", " > ", self.data_dir + outfile_var]
        self.assertEqual(extract.get_switch(), expected)

        infile_var = "test_infile"
        extract = RunGlimmer(infile=infile_var, outfile=outfile_var, pdir=self.data_dir, check_exist=False)
        expected = [self.data_dir + infile_var, self.data_dir + outfile_var + ".coords", " > ", self.data_dir + outfile_var]
        self.assertEqual(extract.get_switch(), expected)

    def test_RunGlimmer_set_infile_outfile(self):
        infile_var = "test_infile.fasta"
        outfile_var = "test_outfile.fasta"
        glimmer = RunGlimmer(infile=infile_var, outfile=outfile_var, pdir=self.data_dir, check_exist=False)

        expected = [self.data_dir + infile_var, self.data_dir + outfile_var + ".coords", " > ", self.data_dir + outfile_var]
        self.assertEqual(glimmer.get_switch(), expected)

#        orf_var = "testORF"
#        glimmer = RunGlimmer(infile=infile_var, filename=outfile_var, orfs=orf_var, pdir=self.data_dir, check_exist=False)
#        self.assertEqual(3, len(glimmer.get_switch()))
#        self.assertEqual(glimmer.get_switch(), [self.data_dir + infile_var, self.data_dir + outfile_var,
#                                                self.data_dir + orf_var])
        infile_var = "test_infile2.fasta"
        glimmer.set_infile_name(infile_var)
        expected = [infile_var, self.data_dir + outfile_var + ".coords", " > ", self.data_dir + outfile_var]
        self.assertEqual(glimmer.get_switch(), expected)

        outfile_var = "test_outfile2.fasta"
        glimmer.set_outfile(outfile_var)
        expected = [infile_var, outfile_var + ".coords", " > ", outfile_var]
        self.assertEqual(glimmer.get_switch(), expected)




    def test_RunGlimmer_check_directory_name(self):
        """
        check if directory name is valid
        """
        infile_var = "pIn"
        outfile_var = "pOut"
        wrong_dir = self.data_dir[:-1]
        glimmer = RunGlimmer(infile=infile_var, outfile=outfile_var, pdir=wrong_dir, check_exist=False)
        self.assertEqual(glimmer.pdir, self.data_dir)


    def test_RunGlimmer_infile_not_exist(self):
        """
        check if infile and/or file directory exist
        """

        infile_var = "fileDoesNotExist"
        outfile_var = "testOutfile"
        with self.assertRaises(IOError):
            RunGlimmer(infile=infile_var, outfile=outfile_var, pdir=self.data_dir, check_exist=True)

        infile_var = "anyFile"
        invalid_dir = "/RandomDirThatDoesNotExist/"
        with self.assertRaises(IOError):
            RunGlimmer(infile=infile_var, outfile=outfile_var, pdir=invalid_dir, check_exist=True)



    def test_RunGlimmer_outfile_already_exist(self):
        """
        check if out file already exists,
        maybe should not raise error, should
        TODO: maybe it should be handle it at different way, auto rename?
        """
        infile_var = "pIn"
        outfile_var = "pOut"
        with self.assertRaises(IOError):
            RunGlimmer(infile=self.data_dir + infile_var, outfile=self.data_dir + outfile_var, pdir=self.data_dir, check_exist=True)


    def test_RunGlimmer_check_outfiles_exist(self):
        """
        check if ./g3iterated.csh finished running, should produce 10 output files
        only pass if all 10 exist
        """
        infile_var = "tIn.fasta"
        outfile_var = "tOut"
        glimmer = RunGlimmer(infile=infile_var, outfile=outfile_var, pdir=self.data_dir, check_exist=False)
        print(glimmer.pdir)
        self.assertFalse(glimmer.check_outfiles_with_filetag_exist(self.data_dir + outfile_var))
        glimmer.run(True)
        self.assertTrue(glimmer.check_outfiles_with_filetag_exist(self.data_dir + outfile_var))

        # negative test, outfiles are not suppose to exist
        outfile_var = "fileNotExist"
        glimmer = RunGlimmer(infile=infile_var, outfile=outfile_var, pdir=self.data_dir, check_exist=False)
        self.assertFalse(glimmer.check_outfiles_with_filetag_exist(self.data_dir + outfile_var))


    def test_RunGlimmer_run(self):
        """
        with debug=True
        should be able to see all 8 steps
        debug - output message:
        Step 1 of 8:  Finding long orfs for training
        Step 2 of 8:  Extracting training sequences
        Step 3 of 8:  Building ICM
        Step 4 of 8:  Running first Glimmer3
        Step 5 of 8:  Getting training coordinates
        Step 6 of 8:  Making PWM from upstream regions
        Step 7 of 8:  Getting start-codon usage
        Step 8 of 8:  Running second Glimmer3
        """

        infile_var = "tIn.fasta"
        outfile_var = "tOut"
        glimmer = RunGlimmer(infile=infile_var, outfile=outfile_var, pdir=self.data_dir, check_exist=False)
        self.assertFalse(glimmer.check_outfiles_with_filetag_exist(self.data_dir + outfile_var))
        glimmer.run(debug=1)
        self.assertTrue(glimmer.check_outfiles_with_filetag_exist(self.data_dir + outfile_var))

