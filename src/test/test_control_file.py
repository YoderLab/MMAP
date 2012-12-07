from core.utils import path_utils
__author__ = 'erinmckenney'

import unittest
from core.controlfile import ControlFile

class TestControlFile(unittest.TestCase):
    def setUp(self):
        self.data_dir = path_utils.get_data_dir() + "unittest_data/"


    def test_add_all(self):
        file = self.data_dir + "testControlFile"
        test = ControlFile()
        test.add_all(file)
        dict = test.all_arguments

        expected = {"parent_directory":"\\someDir\\subDir\\",
        "metasim_pdir":"\\metaSim",
        "metasim_model_infile":  "metaSimInfile",
        "metasim_taxon_infile" : "metasim_taxon_infiles",
        "metasim_no_reads": "20",
        "genovo_infile": "genovoInfile",
        "genovo_pdir": "genevo\\",
        "genovo_noI": "10",
        "genovo_thresh": "300",
        "glimmer_pdir":"\\glimmer\\",
        "mine_pdir":"\\MINE\\",
        "mine_comparison_style":"-allPairs",
        "wdir" :"workingDir"}

        self.assertEqual(expected, dict)

if __name__ == '__main__':
    unittest.main()

