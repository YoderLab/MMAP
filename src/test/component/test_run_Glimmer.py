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
        self.longMessage = True
        self.data_dir = path_utils.get_data_dir()+"Glimmer/"


    def tearDown(self):
        pass

    def test_RunGlimmer_init(self):
        infile_var = "all_reads.fa"
#        outfile_var="testOutfile"
        test_glimmer = RunGlimmer(infile_var, pdir=self.data_dir, checkExist=False)
        self.assertEqual(test_glimmer.get_switch()[0], infile_var)
        self.assertListEqual(test_glimmer.get_switch(), [infile_var, "all_reads_out"])
#

    def test_RunGlimmer_setInfile(self):
    #   def_test_ClassName_whatAreWeTestingHere(self)
        infile_var="test_infile.fasta"
        outfile_var="testOutfile"
        glimmer = RunGlimmer(infile=infile_var, outfile=outfile_var,pdir = self.data_dir, checkExist=False)
        self.assertEqual(2, len(glimmer.get_switch()) )
        self.assertListEqual(glimmer.get_switch(), ["test_infile.fasta", outfile_var])

        infile_var="VICTORY!!!.fasta"
        glimmer.setInfileName(infile_var)
        self.assertListEqual(glimmer.get_switch(), ["VICTORY!!!.fasta", outfile_var])

    def test_RunGlimmer_set_outfile(self):
    #   def_test_ClassName_mhatAreWeTestingHere(self)
        infile_var="test_infile.fasta"
        outfile_var="testOutfile"
        glimmer = RunGlimmer(infile=infile_var, outfile=outfile_var, pdir = self.data_dir, checkExist=False)
        self.assertEqual(2, len(glimmer.get_switch()) )
        self.assertListEqual(glimmer.get_switch(), [ "test_infile.fasta", "testOutfile"])
        infile_var="test_infile.xyz.fasta.abc"
        glimmer2 = RunGlimmer(infile=infile_var,  outfile=outfile_var,pdir = self.data_dir,  checkExist=False)
        self.assertListEqual(glimmer2.get_switch(), ["test_infile.xyz.fasta.abc", outfile_var])
        infile_var="test_infile"
        glimmer2 = RunGlimmer(infile=infile_var, outfile=outfile_var, pdir = self.data_dir,  checkExist=False)
        self.assertListEqual(glimmer2.get_switch(), ["test_infile", outfile_var])


    def test_RunGlimmer_set_infile_outfile(self):
        infile_var="test_infile.fasta"
        outfile_var="test_outfile.fasta"
        glimmer = RunGlimmer(infile=infile_var, outfile = outfile_var, pdir = self.data_dir,  checkExist=False)
        self.assertListEqual(glimmer.get_switch(), [infile_var, "test_outfile.fasta"])
        infile_var="test_infile2.fasta"
        glimmer.setInfileName(infile_var)
        self.assertListEqual(glimmer.get_switch(), ["test_infile2.fasta", "test_outfile.fasta"])

        outfile_var="test_outfile2.fasta"
        glimmer.setOutputTag(outfile_var)
        self.assertListEqual(glimmer.get_switch(), ["test_infile2.fasta", "test_outfile2.fasta"])






    def test_RunGlimmer_check_directory_name(self):
        """
        check if directory name is valid
        """
        infile_var="test_infile.fasta"
        outfile_var="testOutfile"
        wrong_dir = self.data_dir[:-1]
        glimmer = RunGlimmer(infile=infile_var, outfile = outfile_var,pdir = wrong_dir,  checkExist=False)
        self.assertEqual(glimmer.pdir, self.data_dir)


    def test_RunGlimmer_infile_not_exist(self):
        """
        check if infile and/or file directory exist
        """

        infile_var = "fileDoesNotExist"
        outfile_var="testOutfile"
        with self.assertRaises(IOError):
            RunGlimmer(infile=infile_var, outfile = outfile_var,pdir = self.data_dir, checkExist= True)

        #        print self.data_dir
        #        infile_var = "test_infile.fasta"
        #        with self.assertRaises(IOError):
        #            RunGlimmer(infile=infile_var, pdir = self.data_dir, checkExist= True)

        infile_var = "anyFile"
        invalid_dir = "/RandomDirThatDoesNotExist/"
        with self.assertRaises(IOError):
            RunGlimmer(infile=infile_var, outfile = outfile_var,pdir = invalid_dir,checkExist= True)



    def test_RunGlimmer_outfile_already_exist(self):
        """
        check if out file already exists,
        maybe should not raise error, should
        TODO: maybe it should be handle it at different way, auto rename?
        """
        infile_var="tpall.fna"
        outfile_var = "iterated"
        with self.assertRaises(IOError):
            RunGlimmer(infile=infile_var, outfile = outfile_var, pdir = self.data_dir, checkExist= True)


    def test_RunGlimmer_checkOutfilesExist(self):
        """
        check if ./g3iterated.csh finished running, should produce 10 output files
        only pass if all 10 exist
        """
        infile_var="test_infile.fasta"
        outfile_var="iterated"
        glimmer = RunGlimmer(infile=infile_var, outfile = outfile_var,pdir = self.data_dir, checkExist=False)
        print glimmer.checkG3OutfilesExist()
        self.assertTrue( glimmer.checkG3OutfilesExist() )

        # negative test, outfiles are not suppose to exist

        outfile_var="fineNotExist"
        glimmer = RunGlimmer(infile=infile_var, outfile = outfile_var,pdir = self.data_dir, checkExist=False)
        print glimmer.checkG3OutfilesExist()
        self.assertFalse( glimmer.checkG3OutfilesExist() )

##
    def test_RunGlimmer_run(self):
        infile_var="tpall.fna"
        outfile_var="iterated2"
        glimmer = RunGlimmer(infile=infile_var, outfile = outfile_var, pdir = self.data_dir)
        glimmer.run()
#        self.assertTrue( glimmer.checkG3OutfilesExist() )

#
