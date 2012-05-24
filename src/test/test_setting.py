from core.setting import Setting

__author__ = 'erinmckenney'

import unittest
import random
#from ..src import sequence
from core.sequence import Sequence




class TestSetting(unittest.TestCase):

    def setUp(self):

        pass


    def tearDown(self):
        pass

#    @unittest.skip("demonstrating skipping")
    def test_Setting_set_param(self):
        setting = Setting()
        setting.add_all(infle="asdf", outfile="zxcv", noI=2)
        expected = {"infle":"asdf", "outfile":"zxcv", "noI":2}
        self.assertEqual(setting.all_setting, expected)
        setting.add_all(infle="asdf", outfile2="12345", noI=6)
        expected = {"infle":"asdf", "outfile":"zxcv", "noI":6,"outfile2":"12345"}
        self.assertEqual(setting.all_setting, expected)




    def test_Setting_get_genovo(self):
        """

        """
        setting = Setting()
        setting.add_all(genovo_infile="gInfile", outfile="gOutfile", genovo_thresh=2)
        setting.print_all()
        self.assertRaises(KeyError, setting.get_genovo)

        print "starting second test"
        setting = Setting()
        setting.add_all(genovo_infile="gInfile", outfile="gOutfile", genovo_noI=2)
        self.assertRaises(KeyError, setting.get_genovo)
#        ["genovo_infile","genovo_pdir","genovo_noI","genovo_thresh"]
        setting.add("genovo_thresh",13)
        setting.add_all(genovo_thresh=14, genovo_pdir="g_p_dir", parent_directory="main_pdir")
        #        self.assertFalse(  )
        expected = {"genovo_infile":"gInfile", "outfile":"gOutfile", "genovo_noI":2,
                    "genovo_thresh":14, "genovo_pdir":"g_p_dir",
                    "wdir":None,"checkExist":None,
                    "genovo_outfile":None,"parent_directory":"main_pdir"}
#        print "setting.get_genovo:\t", setting.get_genovo()
        self.assertEqual(expected, setting.get_genovo())

        setting.add("wdir","otherdir")
        expected["wdir"]="otherdir"
        print "=====setting check:\t",setting.print_all()
        self.assertEqual(expected, setting.get_genovo())

        setting = Setting()
        setting.add_all(genovo_infile="gInfile", genovo_thresh=14, genovo_pdir="g_p_dir", genovo_noI=2, parent_directory="main_pdir")
        setting.add("wdir","otherdir")

        expected.pop("outfile")

        self.assertEqual(expected, setting.get_genovo())


    def test_Setting_get_glimmer(self):
        setting = Setting()
        setting.add_all(glimmer_infile="glInfile", outfile="Outfile")
        setting.print_all()
        self.assertRaises(KeyError, setting.get_glimmer)

        setting.add("genovo_outfile","infile")
        setting.add_all(glimmer_outfile="glimOut", glimmer_pdir="glimp_dir", parent_directory="main_pdir")
        #        self.assertFalse(  )
        expected = {"glimmer_infile":"infile", "genovo_outfile":"infile","outfile":"Outfile", "glimmer_outfile":"glimOut",
                    "glimmer_pdir":"glimp_dir",
                    "wdir":None,"checkExist":None,
                    "parent_directory":"main_pdir"}
        #        print "setting.get_genovo:\t", setting.get_genovo()
        self.assertEqual(expected, setting.get_glimmer())

    def test_Setting_get_all_par(self):
        setting = Setting()
        setting.add_all(genovo_infile="gInfile", genovo_thresh=14, genovo_pdir="g_p_dir", genovo_noI=2,
            parent_directory="main_pdir")
        setting.add("wdir","otherdir")

        expected = {"genovo_infile":"gInfile", "genovo_noI":2,
                    "genovo_thresh":14, "genovo_pdir":"g_p_dir",
                    "wdir":None,"checkExist":None,
                    "genovo_outfile":None,"parent_directory":"main_pdir", "wdir":"otherdir"}
        self.assertEqual(expected, setting.get_all_par("genovo"))
        self.assertEqual(setting.get_genovo(),expected)

        setting = Setting()
        setting.add_all( outfile="Outfile")
        setting.add("genovo_outfile","infile")
        setting.add_all(glimmer_outfile="glimOut", glimmer_pdir="glimp_dir", parent_directory="main_pdir")

        expected = {"glimmer_infile":"infile", "genovo_outfile":"infile","outfile":"Outfile", "glimmer_outfile":"glimOut",
                    "glimmer_pdir":"glimp_dir",
                    "wdir":None,"checkExist":None,
                    "parent_directory":"main_pdir"}
        self.assertEqual(expected, setting.get_all_par("glimmer"))
        self.assertEqual(setting.get_glimmer(),expected)
        setting.add("glimmer_infile","glInfile")
        expected["glimmer_infile"]="glInfile"
        self.assertEqual(expected, setting.get_all_par("glimmer"))
        self.assertEqual(setting.get_glimmer(),expected)

