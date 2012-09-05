"""
Created on April 9, 2012

@author: Erin McKenney
"""

import unittest
from core.component.run_glimmer import RunGlimmer
from core import run_ext_prog
from core.utils import path_utils


class TestRunGlimmer(unittest.TestCase):

    platform = run_ext_prog.get_platform()

    def setUp(self):
        """
        TODO: add wdir section
        """
        self.long_message = True
        self.data_dir = path_utils.get_data_dir() + "Glimmer/"
#        self.working_dir = path_utils.get_data_dir() + "Glimmer/test_data/"

    def tearDown(self):
        pass

    def test_RunGlimmer_init(self):
        infile_var = "all_reads.fa"

        test_glimmer = RunGlimmer(infile_var, pdir=self.data_dir, check_exist=False)
        self.assertEqual(test_glimmer.get_switch()[0], self.data_dir + infile_var)
        self.assertEqual(test_glimmer.get_switch(), [self.data_dir + infile_var, self.data_dir + "all_reads_out"])
#

    def test_RunGlimmer_setInfile(self):

        infile_var = "test_infile.fasta"
        outfile_var = "testOutfile"
        glimmer = RunGlimmer(infile=infile_var, outfile=outfile_var, pdir=self.data_dir, check_exist=False)
#        self.assertEqual(2, len(glimmer.get_switch()))
#        self.assertEqual(glimmer.get_switch(), [self.data_dir + "test_infile.fasta", self.data_dir + outfile_var])

        orf_var = "testORF"
        extract = RunGlimmer(infile=infile_var, outfile=outfile_var, orfs=orf_var, pdir=self.data_dir, check_exist=False)
#        self.assertEqual(3, len(extract.get_switch()))
        self.assertEqual(extract.get_switch(), [self.data_dir + "test_infile.fasta", self.data_dir + outfile_var,
                                                self.data_dir + "testOutfile_orf"])
#
#        infile_var = "VICTORY.fasta"
#        glimmer.set_infile_name(infile_var)
#        self.assertEqual(glimmer.get_switch(), ["VICTORY.fasta", self.data_dir + outfile_var])
#
#        extract.set_infile_name(infile_var)
#        self.assertEqual(extract.get_switch(), ["VICTORY.fasta", self.data_dir + outfile_var,
#                                                self.data_dir + "testOutfile_orf"])


    def test_RunGlimmer_set_outfile(self):

        infile_var = "test_infile.fasta"
        outfile_var = "testOutfile"

        glimmer = RunGlimmer(infile=infile_var, outfile=outfile_var, pdir=self.data_dir, check_exist=False)
        self.assertEqual(2, len(glimmer.get_switch()))
        self.assertEqual(glimmer.get_switch(), [ self.data_dir + "test_infile.fasta", self.data_dir + "testOutfile"])

        infile_var = "test_infile.xyz.fasta.abc"
        glimmer = RunGlimmer(infile=infile_var, outfile=outfile_var, pdir=self.data_dir, check_exist=False)
        self.assertEqual(glimmer.get_switch(), [self.data_dir + "test_infile.xyz.fasta.abc", self.data_dir + outfile_var])

        infile_var = "test_infile"
        glimmer = RunGlimmer(infile=infile_var, outfile=outfile_var, pdir=self.data_dir, check_exist=False)
        self.assertEqual(glimmer.get_switch(), [self.data_dir + "test_infile", self.data_dir + outfile_var])


    def test_RunGlimmer_set_infile_outfile(self):
        infile_var = "test_infile.fasta"
        outfile_var = "test_outfile.fasta"
        glimmer = RunGlimmer(infile=infile_var, outfile=outfile_var, pdir=self.data_dir, check_exist=False)
        self.assertEqual(glimmer.get_switch(), [self.data_dir + infile_var, self.data_dir + "test_outfile.fasta"])
        infile_var = "test_infile2.fasta"
        glimmer.set_infile_name(infile_var)
        self.assertEqual(glimmer.get_switch(), ["test_infile2.fasta", self.data_dir + "test_outfile.fasta"])

        outfile_var = "test_outfile2.fasta"
        glimmer.set_outfile_tag(outfile_var)
        self.assertEqual(glimmer.get_switch(), ["test_infile2.fasta", "test_outfile2.fasta"])




    def test_RunGlimmer_check_directory_name(self):
        """
        check if directory name is valid
        """
        infile_var = "test_infile.fasta"
        outfile_var = "testOutfile"
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
        infile_var = "tpall.fna"
        outfile_var = "iterated"
        with self.assertRaises(IOError):
            RunGlimmer(infile=self.data_dir + infile_var, outfile=self.data_dir + outfile_var, pdir=self.data_dir, check_exist=True)


    def test_RunGlimmer_check_outfiles_exist(self):
        """
        check if ./g3iterated.csh finished running, should produce 10 output files
        only pass if all 10 exist
        """
        infile_var = "test_infile.fasta"
        outfile_var = "iterated"
        glimmer = RunGlimmer(infile=infile_var, outfile=outfile_var, pdir=self.data_dir, check_exist=False)
        self.assertTrue(glimmer.check_outfiles_exist(self.data_dir + outfile_var))

        # negative test, outfiles are not suppose to exist
        outfile_var = "fineNotExist"
        glimmer = RunGlimmer(infile=infile_var, outfile=outfile_var, pdir=self.data_dir, check_exist=False)
        self.assertFalse(glimmer.check_outfiles_exist(self.data_dir + outfile_var))

##
    def test_RunGlimmer_run(self):
        infile_var = "tpall.fna"
        outfile_var = "iterated2"
        glimmer = RunGlimmer(infile=infile_var, outfile=outfile_var, pdir=self.data_dir)
#        glimmer.run()
#        self.assertTrue( glimmer.checkG3OutfilesExist() )

#
