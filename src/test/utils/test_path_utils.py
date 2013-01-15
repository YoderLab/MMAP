"""
Created on Jan 11, 2013

@author: Steven Wu
"""
import unittest
from core.utils import path_utils
import os

class TestPathUtility(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass

    def test_get_name_without_ext(self):
        self.assertEqual("AA", path_utils.remove_ext("AA"))
        self.assertEqual("AA", path_utils.remove_ext("AA.1"))
        self.assertEqual("AA.1", path_utils.remove_ext("AA.1.2"))
        self.assertEqual("AA.1.2", path_utils.remove_ext("AA.1.2.3"))

    def test_check_program_dir(self):
        wdir = "workingDir"
        pro_dir = "progromDir"
        expected = wdir + os.sep + pro_dir
        self.assertEqual(expected, path_utils.check_program_dir(wdir, pro_dir))

        wdir = "workingDir" + os.sep
        pro_dir = "progromDir" + os.sep
        self.assertEqual(expected, path_utils.check_program_dir(wdir, pro_dir))

        wdir = "workingDir" + os.sep
        pro_dir = os.sep + "progromDir"
        self.assertEqual(expected, path_utils.check_program_dir(wdir, pro_dir))

        expected = os.sep + expected
        wdir = os.sep + "workingDir" + os.sep
        pro_dir = os.sep + "progromDir" + os.sep
        self.assertEqual(expected, path_utils.check_program_dir(wdir, pro_dir))

        wdir = os.sep + "workingDir"
        pro_dir = os.sep + "progromDir"
        self.assertEqual(expected, path_utils.check_program_dir(wdir, pro_dir))

        wdir = os.sep + "workingDir"
        pro_dir = "progromDir" + os.sep
        self.assertEqual(expected, path_utils.check_program_dir(wdir, pro_dir))


