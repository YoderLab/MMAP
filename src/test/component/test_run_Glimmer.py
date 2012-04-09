"""
Created on April 9, 2012

@author: Erin McKenney
"""

import unittest
from core.component.run_glimmer import RunGlimmer
from core import run_ext_prog
from core.utils import path_utils
import os
import subprocess


class TestRunGlimmer(unittest.TestCase):

    platform = run_ext_prog.get_platform()
    
    def setUp(self):
        self.longMessage = True
        self.data_dir = path_utils.get_data_dir()+"Glimmer/"


    def tearDown(self):
        pass

    def test_RunGlimmer_init(self):
        infile_var = "all_reads.fa"
        glimmer = RunGlimmer(infile_var, pdir=self.data_dir)
        self.assertEqual(glimmer.get_switch()[0], infile_var)
        self.assertEqual(glimmer.get_switch(), [infile_var, "1"])
        self.assertListEqual(glimmer.get_switch(), [infile_var, "all_reads_out"])


    def test_RunGlimmer_setInfile(self):
    #   def_test_ClassName_whatAreWeTestingHere(self)
        infile_var="test_infile.fasta"
        glimmer = RunGlimmer(infile=infile_var, pdir = self.data_dir, checkExist=False)
        self.assertEqual(2, len(glimmer._switch) )
        self.assertListEqual(glimmer.get_switch(), ["test_infile.fasta", "test_infile_out"])

        infile_var="VICTORY!!!.fasta"
        glimmer.setInfileName(infile_var)
        self.assertListEqual(glimmer.get_switch(), ["VICTORY!!!.fasta", "test_infile_out"])

    def test_RunGlimmer_set_outfile(self):
    #   def_test_ClassName_mhatAreWeTestingHere(self)
        infile_var="test_infile.fasta"
        outfile_var="testOutfile"
        glimmer = RunGlimmer(infile=infile_var, outfile=outfile_var, pdir = self.data_dir, checkExist=False)
        self.assertEqual(2, len(glimmer._switch) )
        self.assertListEqual(glimmer.get_switch(), [ "test_infile.fasta", "testOutfile"
        glimmer2 = RunGlimmer(infile=infile_var,  pdir = self.data_dir,  checkExist=False)   ## outfile == None
        self.assertListEqual(glimmer2.get_switch(), ["test_infile.fasta", "test_infile_out"])
        infile_var="test_infile.xyz.fasta.abc"
        glimmer2 = RunGlimmer(infile=infile_var,  pdir = self.data_dir,  checkExist=False)   ## outfile == None
        self.assertListEqual(glimmer2.get_switch(), ["test_infile.xyz.fasta.fasta", "test_infile_out"])
        infile_var="test_infile"
        glimmer2 = RunGlimmer(infile=infile_var,  pdir = self.data_dir,  checkExist=False)   ## outfile == None
        self.assertListEqual(glimmer2.get_switch(), ["test_infile", "test_infile_out"])


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
        dir = self.data_dir[:-1]
        glimmer = RunGlimmer(infile=infile_var, pdir = dir,  checkExist=False)
        self.assertEqual(glimmer.pdir, self.data_dir)


    def test_RunGlimmer_infile_not_exist(self):
        """
        check if infile and/or file directory exist
        """

        infile_var = "fileDoesNotExist"
        with self.assertRaises(IOError):
            RunGlimmer(infile=infile_var, pdir = self.data_dir, checkExist= True)

        #        print self.data_dir
        #        infile_var = "test_infile.fasta"
        #        with self.assertRaises(IOError):
        #            RunGlimmer(infile=infile_var, pdir = self.data_dir, checkExist= True)

        infile_var = "anyFile"
        invalid_dir = "/RandomDirThatDoesNotExist/"
        with self.assertRaises(IOError):
            RunGlimmer(infile=infile_var, pdir = invalid_dir,checkExist= True)



        #    def test_RunGenovo_outfile_already_exist(self):
        #        """
        #        check if out file already exists,
        #        maybe should not raise error, should
        #        TODO: maybe it should be handle it at different way, auto rename?
        #        """
        #        infile_var="test_infile.fasta"
        #        outfile_var = "testOutFileAlreadyExist.fasta"
        #        with self.assertRaises(IOError):
        #            RunGenovo(infile=infile_var, outfile = outfile_var, pdir = self.data_dir, noI=3, thresh=250, checkExist= True)
        #

    def test_RunGlimmer_checkOutfilesExist(self):
        """
        check if ./g3iterated.csh finished running, should produce 10 output files
        only pass if all 10 exist
        """
        infile_var="test_infile.fasta"
        glimmer = RunGlimmer(infile=infile_var, pdir = self.data_dir, checkExist=False)
        print glimmer.checkOutfilesExist()
        self.assertTrue( glimmer.checkOutfilesExist() )

        # negative test, outfiles are not suppose to exist
        infile_var="fileNotExist.fasta"
        glimmer = RunGlimmer(infile=infile_var, pdir = self.data_dir, checkExist=False)
        print glimmer.checkOutfilesExist()
        self.assertFalse( glimmer.checkOutfilesExist() )

    def test_RunGlimmer_readOutfile(self):
        """
        check if it can "read" assembled contig
        TODO: have check what happen in the file format is invalid, assuming its the correct fasta now
        """
        infile_var="test_infile.fasta"
        outfile_var="test_outfile.fasta"
        glimmer = RunGlimmer(infile=infile_var, outfile = outfile_var, pdir = self.data_dir, checkExist=False)
        result = glimmer.readOutfile()
        self.assertEqual(len(result), 2)
        self.assertEqual(result.keys(), ["1","2"])

        expected = [170,60]
        for i, key in enumerate(result):
            print key, i, type(result[key]), result[key]
            self.assertEqual(len(result[key]), expected[i])


#    
#    def test_RunGlimmer_run(self):
#        infile_var="test_run_infile.fasta"
#        outfile_var="test_run_outfile"
#        glimmer = RunGlimmer(infile=infile_var, outfile = outfile_var, pdir = self.data_dir, checkExist=False)
#        glimmer.run()
#        self.assertTrue( glimmer.checkOutfilesExist() )
#        
    
