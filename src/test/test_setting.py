from core.setting import Setting
import unittest

__author__ = 'erinmckenney'


class TestSetting(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

#    @unittest.skip("demonstrating skipping")
    def test_Setting_set_param(self):
        setting = Setting()
        setting.add_all(infle="asdf", outfile="zxcv", noI=2)
        expected = {"infle": "asdf", "outfile": "zxcv", "noI": 2}
        self.assertEqual(setting.all_setting, expected)
        setting.add_all(infle="asdf", outfile2="12345", noI=6)
        expected = {"infle": "asdf", "outfile": "zxcv",
                    "noI": 6, "outfile2": "12345"}
        self.assertEqual(setting.all_setting, expected)

    def test_Setting_get_metasim(self): #"metasim_pdir", "metasim_model_infile", "metasim_taxon_infile", "metasim_no_reads"
        setting = Setting()
        setting.add_all(metasim_model_infile="mmInfile",
            outfile="mOutfile", metasim_no_reads=200)
        #        setting.print_all()
        self.assertRaises(KeyError, setting._get_metasim)

        setting = Setting()
        setting.add_all(metasim_model_infile="mmInfile",
            outfile="mOutfile", metasim_taxon_infile="tInfile")
        self.assertRaises(KeyError, setting._get_metasim)

        setting.add("metasim_pdir", "m_p_dir")
        setting.add_all(metasim_no_reads=250, parent_directory="main_pdir")
        expected = {"metasim_model_infile": "mmInfile", "outfile": "mOutfile",
                    "metasim_taxon_infile": "tInfile", "metasim_pdir": "m_p_dir",
                    "parent_directory": "main_pdir", "metasim_no_reads":250,
                    "wdir":None, "checkExist": True,
                    "metasim_outfile": None}
        self.assertEqual(expected, setting._get_metasim())

        setting.add("wdir", "otherdir")
        expected["wdir"] = "otherdir"
        self.assertEqual(expected, setting._get_metasim())

        setting = Setting()
        setting.add_all(metasim_model_infile="mmInfile", metasim_no_reads=250,
            metasim_taxon_infile="tInfile", metasim_pdir="m_p_dir",
            parent_directory="main_pdir")
        setting.add("wdir", "otherdir")
        expected.pop("outfile")
        self.assertEqual(expected, setting._get_metasim())

    def test_Setting_get_genovo(self):

        setting = Setting()
        setting.add_all(genovo_infile="gInfile",
                        outfile="gOutfile", genovo_thresh=2)
#        setting.print_all()
        self.assertRaises(KeyError, setting._get_genovo)

        setting = Setting()
        setting.add_all(genovo_infile="gInfile",
                        outfile="gOutfile", genovo_noI=2)
        self.assertRaises(KeyError, setting._get_genovo)

        setting.add("genovo_thresh", 10)
        setting.add_all(genovo_thresh=14,
                        genovo_pdir="g_p_dir", parent_directory="main_pdir")
        expected = {"genovo_infile": "gInfile", "outfile": "gOutfile",
                    "genovo_noI": 2, "genovo_thresh": 14,
                    "genovo_pdir": "g_p_dir", "parent_directory": "main_pdir",
                    "wdir": None, "checkExist": True,
                    "genovo_outfile": None}
        self.assertEqual(expected, setting._get_genovo())

        setting.add("wdir", "otherdir")
        expected["wdir"] = "otherdir"
        self.assertEqual(expected, setting._get_genovo())

        setting = Setting()
        setting.add_all(genovo_infile="gInfile", genovo_thresh=14,
                        genovo_pdir="g_p_dir", genovo_noI=2,
                        parent_directory="main_pdir")
        setting.add("wdir", "otherdir")
        expected.pop("outfile")
        self.assertEqual(expected, setting._get_genovo())

    def test_Setting_get_glimmer(self):
        setting = Setting()
        setting.add_all(outfile="Outfile")
        #        setting.print_all()
        self.assertRaises(KeyError, setting._get_glimmer)

        setting.add_all(genovo_outfile="infile", glimmer_outfile="glimOut",
            glimmer_pdir="glimp_dir", parent_directory="main_pdir")
        expected = {"glimmer_infile": "infile", "genovo_outfile": "infile",
                    "outfile": "Outfile", "glimmer_outfile": "glimOut",
                    "glimmer_pdir": "glimp_dir",
                    "wdir": None, "checkExist": True,
                    "extract_outfile": None,
                    "parent_directory": "main_pdir"}
        self.assertEqual(expected, setting._get_glimmer())

        setting.add_all(glimmer_infile="glInfile")
        expected["glimmer_infile"] = "glInfile"

    def test_Setting_get_blast(self):
        setting = Setting()
        setting.add_all(blast_infile="bInfile", blast_outfile="bOutfile")
        #        setting.print_all()
        self.assertRaises(KeyError, setting._get_blast)

        setting.add("blast_e-value", 1e-15)
        setting.add_all(blast_pdir="b_p_dir", parent_directory="main_pdir")
        expected = {"blast_infile": "bInfile", "blast_outfile": "bOutfile",
                    "blast_e_value": 1e-15, "blast_pdir": "b_p_dir",
                    "parent_directory": "main_pdir",
                    "wdir": None, "checkExist": True}
#        setting.debug = True
        self.assertEqual(expected, setting._get_blast())

        setting.add("wdir", "otherdir")
        expected["wdir"] = "otherdir"
        self.assertEqual(expected, setting._get_blast())

        setting = Setting()
        setting.add_all(blast_infile="bInfile",
            blast_pdir="b_p_dir", parent_directory="main_pdir")
        setting.add("wdir", "otherdir")
        setting.add("blast_e_value", 1e-15)
        setting.add("blast_outfile", "bOutfile")
#        expected.pop("outfile")
#        TODO: debug switch
        setting.debug = True
        self.assertEqual(expected, setting._get_blast())

    def test_Setting_get_mine(self):
        setting = Setting()
        setting.add_all(outfile="Outfile")
        setting.debug = True
        #        setting.print_all()
#        self.assertRaises(KeyError, setting._get_mine())

        setting.add_all( mine_outfile="mineOut",
            mine_pdir="mine_pdir", mine_comparison_style="-allPairs",parent_directory="main_pdir")
        setting.add("mine_infile", "infile")

        expected = {"mine_infile": "infile",
                    "outfile": "Outfile", "mine_outfile": "mineOut",
                    "mine_pdir": "mine_pdir", "mine_comparison_style":"-allPairs",
                    "wdir": None, "checkExist": True,
                    "parent_directory": "main_pdir",
                    "mine_cv": None, "mine_clumps":None, "mine_jobID": None}

        self.assertEqual(expected, setting._get_mine())

        setting.add_all(mine_infile="mineInfile")
        expected["mine_infile"] = "mineInfile"

def test_Setting_get_all_par(self):
        setting = Setting()
        setting.add_all(genovo_infile="gInfile", genovo_thresh=14,
                        genovo_pdir="g_p_dir", genovo_noI=2,
                        parent_directory="main_pdir", wdir="otherdir")
        expected = {"genovo_infile": "gInfile", "genovo_noI": 2,
                    "genovo_thresh": 14, "genovo_pdir": "g_p_dir",
                    "checkExist": True, "genovo_outfile": None,
                    "parent_directory": "main_pdir", "wdir": "otherdir"}

        self.assertEqual(expected, setting.get_all_par("genovo"))
        self.assertEqual(setting._get_genovo(), expected)

        setting = Setting()
        setting.add_all(outfile="Outfile", genovo_outfile="infile",
                        glimmer_outfile="glimOut", glimmer_pdir="glimp_dir",
                        parent_directory="main_pdir")

        expected = {"glimmer_infile": "infile", "genovo_outfile": "infile",
                    "outfile": "Outfile", "glimmer_outfile": "glimOut",
                    "glimmer_pdir": "glimp_dir",
                    "wdir": None, "checkExist": True,
                    "parent_directory": "main_pdir"}
        self.assertEqual(expected, setting.get_all_par("glimmer"))
        self.assertEqual(setting._get_glimmer(), expected)

        setting.add("glimmer_infile", "glInfile")
        expected["glimmer_infile"] = "glInfile"
        self.assertEqual(expected, setting.get_all_par("glimmer"))
        self.assertEqual(setting._get_glimmer(), expected)

