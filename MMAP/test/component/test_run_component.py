"""
Created on May 7, 2012

@author: Erin McKenney
"""
import os
import unittest

from core.component.run_component import RunComponent
from core import run_ext_prog
from core.utils import path_utils


class TestRunComponent(unittest.TestCase):

    platform = run_ext_prog.get_platform()

    def setUp(self):
        self.longMessage = True
        self.data_dir = path_utils.get_data_dir() + "unittest_data/"
        self.wdir = path_utils.get_data_dir() + "Genovo/test_data/"
#    TODO: rename / consolidate all test_data to unittest_data

    def tearDown(self):
        pass

    def test_GenerateOutfileName(self):
        infile_var = "test_infile.fasta"

        comp = RunComponent()
        comp.wdir = self.wdir
        comp.check_outfile_filename(infile_var, None, "_out")
        self.assertEqual(self.wdir + infile_var, comp.infile)
        self.assertEqual(self.wdir + "test_infile_out", comp.outfile)
        #        print genovo.checkAssembleOutfilesExist("test_infile.fasta")

    def test_check_outfiles_exist(self):
        infile_tag = "tIn"

        comp = RunComponent()
        comp.all_exts = [".test1", ".test2"]
        self.assertTrue(comp.check_outfiles_with_filetag_exist(self.data_dir + infile_tag))
        comp.all_exts = ["not1", "not2"]
        is_exist, _ = comp.check_outfiles_with_filetag_exist(self.data_dir + infile_tag)
        self.assertFalse(is_exist)




