"""
Created on May 7, 2012

@author: Erin McKenney
"""
import unittest
import os
from core.component.run_component import RunComponent
from core.component.run_Genovo import RunGenovo
from core import run_ext_prog
from core.utils import path_utils


class TestRunComponent(unittest.TestCase):

    platform = run_ext_prog.get_platform()


    def setUp(self):
        self.longMessage = True
        self.data_dir = path_utils.get_data_dir()+"Genovo/"
        self.working_dir = path_utils.get_data_dir()+"Genovo/test_data/"

    def tearDown(self):
        pass

    def test_GenerateOutfileName(self):
        infile_var="test_infile.fasta"

        comp = RunComponent()
        outfile = comp.generate_outfile_name(infile_var,"_out")
        self.assertEqual("test_infile_out", outfile)
        #        print genovo.checkAssembleOutfilesExist("test_infile.fasta")

    def test_check_outfiles_exist(self):
        print "in check outfile exist"
        infile_tag="test_infile.fasta"
        exts=[".dump1",".status"]
        comp = RunComponent()
        self.assertTrue( comp.check_multiple_outfiles_existence(outfileTag=self.data_dir+infile_tag , allext=exts) )
        exts=["not1","not2"]
        self.assertFalse( comp.check_multiple_outfiles_existence(outfileTag=self.data_dir+infile_tag , allext=exts) )
#        glimmer = RunComponent.generate_outfile_name(infile)
#        #        print genovo.checkAssembleOutfilesExist("test_infile.fasta")
#        self.assertTrue( glimmer.check_outfiles_exist(self.data_dir+infile_var) )


    def test_checkInfileExist(self):
        infile_var="test_infile.fasta"
        comp = RunComponent()
        genovo = RunComponent.check_infile_exist(infile)
        genovo.run()
        self.assertTrue(RunComponent.check_file_existence(self.data_dir+infile_var, ".fasta",True))

        glimmer = RunComponent.check_infile_exist(infile)
        glimmer.run()
        self.assertTrue(RunComponent.check_file_existence(self.data_dir+infile_var, ".fasta",True))

    @unittest.skip("")
    def test_check_outfiles_exista(self):
        infile_var="test_infile.fasta"
        genovo = RunComponent.check_outfiles_exist(outfile_tag=infile_var)
        self.assertTrue( genovo.check_outfiles_exist(self.data_dir+"test_infile.fasta") )

        glimmer = RunComponent.check_outfiles_exist(outfile_tag=infile_var)
        self.assertTrue( glimmer.check_outfiles_exist(self.data_dir+"test_infile.fasta") )