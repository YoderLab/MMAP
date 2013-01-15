
from core.setting import Setting
import unittest
from core.utils import path_utils

__author__ = 'erinmckenney'


class TestSetting(unittest.TestCase):

    def setUp(self):
        self.data_dir = path_utils.get_data_dir() + "unittest_data/"
        self.wdir = "working_dir"
        self.maxDiff = None

    def tearDown(self):
        pass

#    @unittest.skip("demonstrating skipping")
    def test_Setting_set_param(self):
        setting = Setting()
        setting.add_all(infle="asdf", filename="zxcv", noI=2)
        expected = {"infle": "asdf", "filename": "zxcv", "noI": 2}
        self.assertEqual(setting.all_setting, expected)
        setting.add_all(infle="asdf", outfile2="12345", noI=6)
        expected = {"infle": "asdf", "filename": "zxcv",
                    "noI": 6, "outfile2": "12345"}
        self.assertEqual(setting.all_setting, expected)

    def test_Setting_get_metasim(self): #"metasim_pdir", "metasim_model_infile", "metasim_taxon_infile", "metasim_no_reads"
        setting = Setting()
        setting.add_all(metasim_model_infile="mmInfile",
            filename="mOutfile", metasim_no_reads=200)
        #        setting.print_all()
        self.assertRaises(KeyError, setting.get_pars, "metasim")

        setting = Setting()
        setting.add_all(metasim_model_infile="mmInfile",
            filename="mOutfile", metasim_taxon_infile="tInfile")
        self.assertRaises(KeyError, setting.get_pars, "metasim")

        setting.add("metasim_pdir", "m_p_dir")
        setting.add_all(metasim_no_reads=250, parent_directory="main_pdir",
                        wdir=self.wdir)
        expected = {"metasim_model_infile": "mmInfile", "filename": "mOutfile",
                    "metasim_taxon_infile": "tInfile", "metasim_pdir": "m_p_dir",
                    "parent_directory": "main_pdir", "metasim_no_reads":250,
                    "wdir":self.wdir, "checkExist": True,
                    "metasim_outfile": None}
        setting.debug = 0
        self.assertEqual(expected, setting.get_pars("metasim"))

        setting.add("wdir", "otherdir")
        expected["wdir"] = "otherdir"
        self.assertEqual(expected, setting.get_pars("metasim"))

        setting = Setting()
        setting.add_all(metasim_model_infile="mmInfile", metasim_no_reads=250,
            metasim_taxon_infile="tInfile", metasim_pdir="m_p_dir",
            parent_directory="main_pdir")
        setting.add("wdir", "otherdir")
        expected.pop("filename")
        self.assertEqual(expected, setting.get_pars("metasim"))

    def test_Setting_get_genovo(self):

        setting = Setting()
        setting.add_all(genovo_infile="gInfile",
                        filename="gOutfile", genovo_thresh=2)
#        setting.print_all()
        self.assertRaises(KeyError, setting.get_pars, "genovo")

        setting = Setting()
        setting.add_all(genovo_infile="gInfile",
                        filename="gOutfile", genovo_noI=2)
        self.assertRaises(KeyError, setting.get_pars, "genovo")

        setting.add("genovo_thresh", 10)
        setting.add_all(genovo_thresh=14, genovo_pdir="g_p_dir", parent_directory="main_pdir",
                        wdir=self.wdir)
        expected = {"genovo_infile": "gInfile", "filename": "gOutfile",
                    "genovo_noI": 2, "genovo_thresh": 14,
                    "genovo_pdir": "g_p_dir", "parent_directory": "main_pdir",
                    "wdir": self.wdir, "checkExist": True,
                    "genovo_outfile": None}
        self.assertEqual(expected, setting.get_pars("genovo"))

        setting.add("wdir", "otherdir")
        expected["wdir"] = "otherdir"
        self.assertEqual(expected, setting.get_pars("genovo"))

        setting = Setting()
        setting.add_all(genovo_infile="gInfile", genovo_thresh=14,
                        genovo_pdir="g_p_dir", genovo_noI=2,
                        parent_directory="main_pdir")
        setting.add("wdir", "otherdir")
        expected.pop("filename")
        self.assertEqual(expected, setting.get_pars("genovo"))

    def test_Setting_get_glimmer(self):
        setting = Setting()
        setting.add_all(filename="Outfile")
        #        setting.print_all()
        self.assertRaises(KeyError, setting.get_pars, "glimmer")


        setting.add_all(genovo_outfile="infile", glimmer_outfile="glimOut",
            glimmer_pdir="glimp_dir", parent_directory="main_pdir", wdir=self.wdir)
        expected = {"glimmer_infile": "infile", "genovo_outfile": "infile",
                    "filename": "Outfile", "glimmer_outfile": "glimOut",
                    "glimmer_pdir": "glimp_dir",
                    "wdir": self.wdir, "checkExist": True,
                    "parent_directory": "main_pdir"}
        self.assertEqual(expected, setting.get_pars("glimmer"))

        setting.add_all(glimmer_infile="glInfile")
        expected["glimmer_infile"] = "glInfile"


    def test_Setting_get_blast(self):
        setting = Setting()
        setting.add_all(blast_infile="bInfile", blast_outfile="bOutfile")

        with self.assertRaises(KeyError):
            setting.get_pars("blast")

        setting.add_all(blast_e_value=1e-15, parent_directory="main_pdir",
                        wdir="working_dir", checkExist=True)
        expected = {"blast_infile": "bInfile", "blast_outfile": "bOutfile",
                    "blast_e_value": 1e-15,
                    "parent_directory": "main_pdir",
                    "wdir": "working_dir", "checkExist": True, "blast_comparison_file":None}
        setting.debug = True
        self.assertEqual(expected, setting.get_pars("blast"))


        setting.add("wdir", "otherdir")
        expected["wdir"] = "otherdir"
        self.assertEqual(expected, setting.get_pars("blast"))

        setting = Setting()
        setting.add_all(blast_infile="bInfile", parent_directory="main_pdir")
        setting.add("wdir", "otherdir")
        setting.add("blast_e_value", 1e-15)
        setting.add("blast_outfile", "bOutfile")
#        expected.pop("filename")
#        TODO: debug switch
        setting.debug = True
        self.assertEqual(expected, setting.get_pars("blast"))

    def test_Setting_get_mine(self):
        setting = Setting()
        setting.add_all(filename="Outfile")
        setting.debug = True
        #        setting.print_all()
#        self.assertRaises(KeyError, setting._get_mine())

        setting.add_all(mine_outfile="mineOut",
            mine_pdir="mine_pdir", mine_comparison_style="-allPairs", parent_directory="main_pdir")
        setting.add("mine_infile", "infile")
        setting.add("wdir", "working_dir")
        setting.add("csv_files", "file1,file2,file3")

        expected = {"mine_infile": "infile",
                    "filename": "Outfile", "mine_outfile": "mineOut",
                    "mine_pdir": "mine_pdir", "mine_comparison_style":"-allPairs",
                    "wdir": "working_dir", "checkExist": True,
                    "parent_directory": "main_pdir",
                    "mine_cv": 0.0, "mine_exp":0.6, "mine_clumps":15, "mine_jobID": None,
                    "csv_files": ["file1", "file2", "file3"]}

        self.assertEqual(expected, setting.get_pars("mine"))

        setting.add_all(mine_infile="mineInfile")
        expected["mine_infile"] = "mineInfile"

    def test_Setting_get_pars(self):
        setting = Setting(genovo_infile="gInfile", genovo_thresh=14)
        setting.add_all(
                        genovo_pdir="g_p_dir", genovo_noI=2,
                        parent_directory="main_pdir", wdir="otherdir",
                        checkExist=True)
        expected = {"genovo_infile": "gInfile", "genovo_noI": 2,
                    "genovo_thresh": 14, "genovo_pdir": "g_p_dir",
                    "checkExist": True, "genovo_outfile": None,
                    "parent_directory": "main_pdir", "wdir": "otherdir"}
        print "W", setting.get_pars("genovo")
        self.assertEqual(expected, setting.get_pars("genovo"))


        setting = Setting()
        setting.add_all(filename="Outfile", genovo_outfile="infile",
                        glimmer_outfile="glimOut", glimmer_pdir="glimp_dir",
                        parent_directory="main_pdir", wdir="working_dir")

        expected = {"glimmer_infile": "infile", "genovo_outfile": "infile",
                    "filename": "Outfile", "glimmer_outfile": "glimOut",
                    "glimmer_pdir": "glimp_dir",
                    "wdir": "working_dir", "checkExist": True,
                    "parent_directory": "main_pdir",
                    }
        print setting.get_pars("glimmer")
        self.assertEqual(expected, setting.get_pars("glimmer"))

        setting.add("glimmer_infile", "glInfile")
        expected["glimmer_infile"] = "glInfile"
        self.assertEqual(expected, setting.get_pars("glimmer"))


    def test_create_setting_from_file(self):
#    When not all essential parameters exist but no optional parameters exist, should pass.
        file = self.data_dir + "testControlFileOp1"
        setting = Setting.create_setting_from_file(file)
        expected = {"parent_directory":"/someDir/subDir",
                    "wdir" :"/someDir/subDir/workingDir",
                    "master_tag": "genovoInfile",

                    "genovo_infile": "genovoInfile",
                    "genovo_pdir": "/someDir/subDir/genevo",
                    "genovo_noI": "20",
                    "glimmer_pdir":"/someDir/subDir/glimmer",

                    "blast_e_value":"1e-10",
                    }

        self.assertEqual(expected, setting.all_setting)

#        When not all essential parameters exist, should fail.
        file = self.data_dir + "missedEssentials"
        with self.assertRaises(KeyError):
            Setting.create_setting_from_file(file)

#        When all essential parameters exist and all optional parameters exist, should pass.
        file = self.data_dir + "allPass"
        try:
            setting = Setting.create_setting_from_file(file)
        except KeyError:
            self.fail("raise KeyError unexpectedly")


#        When not all essential parameters exist and some optional parameters exist, should pass.
        file = self.data_dir + "testControlFileOp1"
        try:
            setting = Setting.create_setting_from_file(file)
        except KeyError:
            self.fail("raise KeyError unexpectedly")


    def test_create_setting_from_file_MINE_only(self):
#    When not all essential parameters exist but no optional parameters exist, should pass.
        file = self.data_dir + "testControlFileMINE"
        setting = Setting.create_setting_from_file(file)
        expected = {
                    "parent_directory":"/someDir/subDir",
                    "wdir" :"/someDir/subDir/workingDir",
                    "mine_pdir":"/someDir/subDir/MINE",
                    "mine_cv":"20",
                    }
#        self.assertEqual(setting.all_setting, expected)
        self.assertEqual(expected, setting.all_setting)
