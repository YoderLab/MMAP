"""
Created on May 7, 2012

@author: Erin McKenney
"""
import unittest
from core.component.run_component import RunComponent
from core import run_ext_prog
from core.utils import path_utils


class TestRunComponent(unittest.TestCase):

    platform = run_ext_prog.get_platform()

    def setUp(self):
        self.longMessage = True
        self.data_dir = path_utils.get_data_dir() + "Genovo/"
        self.wdir = path_utils.get_data_dir() + "Genovo/test_data/"

    def tearDown(self):
        pass

    def test_GenerateOutfileName(self):
        infile_var = "test_infile.fasta"

        comp = RunComponent()
        comp.wdir = self.wdir
        comp.generate_outfile_name(infile_var, None, "_out")
        self.assertEqual(self.wdir + infile_var, comp.infile)
        self.assertEqual(self.wdir + "test_infile_out", comp.outfile)
        #        print genovo.checkAssembleOutfilesExist("test_infile.fasta")

    def test_check_outfiles_exist(self):
        infile_tag = "test_infile.fasta"
        exts = [".dump1", ".status"]
        comp = RunComponent()
        self.assertTrue(comp.is_multi_files_exist(file_tag=self.data_dir + infile_tag, all_exts=exts))
        exts = ["not1", "not2"]
        self.assertFalse(comp.is_multi_files_exist(file_tag=self.data_dir + infile_tag , all_exts=exts))




