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
        setting.add_all(genovo_thresh=14, genovo_pdir="g_p_dir")
        setting.add("genovo_thresh", 14)
        setting.add( "genovo_pdir","g_p_dir")
        #        self.assertFalse(  )
        expected = {"genovo_infile":"gInfile", "outfile":"gOutfile", "genovo_noI":2,
                    "genovo_thresh":14, "genovo_pdir":"g_p_dir",
                    "wdir":None,"checkExist":None,
                    "genovo_outfile":None,}
        self.assertEqual(expected, setting.get_genovo())

        setting.add("wdir", "optionaldir")
        expected["wdir"]="optionaldir"
        self.assertEqual(expected, setting.get_genovo())

        setting = Setting()
        setting.add_all(genovo_infile="gInfile", genovo_thresh=14, genovo_pdir="g_p_dir", genovo_noI=2)
        setting.add("wdir","optionaldir")

        expected.pop("outfile")

        self.assertEqual(expected, setting.get_genovo())


    def test_Setting_get_glimmer(self):
        pass

    def test_Setting_get_all_par(self, program_name):
        setting = Setting()
        expected = {}
        self.assertEqual(expected, setting.get_all_par("genovo"))
        self.assertEqual(setting.get_genovo(),expected)
