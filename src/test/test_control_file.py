__author__ = 'erinmckenney'

import unittest
from core.controlfile import ControlFile

class TestControlFile(unittest.TestCase):
    def test_add_all(self):
        file="/Users/erinmckenney/Desktop/Pipeline/metaLem/data/unittest_data/testControlFile"
        test = ControlFile()

        expected = {"parent_directory": "\someDir\subDir\ ",
        "metasim_pdir":"\metaSim",
        "metasim_model_infile": "metaSimInfile",
        "metasim_taxon_infile" : "metasim_taxon_infiles",
        "metasim_no_reads": 20,
        "genovo_infile": "genovoInfile",
        "genovo_pdir": "genevo\ ",
        "genovo_noI": "10",
        "genovo_thresh": "300"}

        print "!!!!!!!!!!", test.all_arguments
        self.assertEqual(expected, test.all_arguments(file))

if __name__ == '__main__':
    unittest.main()

