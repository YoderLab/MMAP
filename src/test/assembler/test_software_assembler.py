from core.assembler.software_assembler import SoftwareAssembler
from core.utils import path_utils

__author__ = 'erinmckenney'

import unittest


class TestSoftwareAssembler(unittest.TestCase):

    def setUp(self):
        self.assembly = SoftwareAssembler()
        self.genovo_dir = path_utils.get_data_dir() + "Genovo/"
        self.glimmer_dir = path_utils.get_data_dir() + "Glimmer/"
        self.metasim_dir = path_utils.get_data_dir() + "MetaSim/"
        self.mine_dir = path_utils.get_data_dir() + "MINE/"
        self.blast_dir = path_utils.get_data_dir() + "BLAST/"
        self.working_dir = path_utils.get_data_dir() + "test_data/"

    def test_SoftwareAssembler_set_all_param(self):

        self.assembly.add_all_param(genovo_infile="gInfile",
                                    outfile="gOutfile", genovo_thresh=2)
        expected = {"genovo_infile": "gInfile", "outfile": "gOutfile",
                    "genovo_thresh": 2}
        self.assertEqual(self.assembly.get_all_par(), expected)

        self.assembly.add_all_param(glimmer_outfile="glimOutfile",
                                    glimpar="testAddPar", genovo_thresh=14)
        expected = {"genovo_infile": "gInfile", "outfile": "gOutfile",
                    "genovo_thresh": 14, "glimmer_outfile": "glimOutfile",
                    "glimpar": "testAddPar"}
        self.assertEqual(self.assembly.get_all_par(), expected)

    def test_SoftwareAssembler_init_program(self):

        self.assembly.add_all_param(genovo_infile="wdir_all_reads.fa",
                                    genovo_thresh=50, genovo_pdir=self.genovo_dir,
                                    genovo_noI=10, parent_directory="main_pdir")
        self.assembly.add_all_param(glimmer_pdir=self.glimmer_dir)
        self.assembly.add_all_param(wdir=self.working_dir)
        self.assembly.add_all_param(metasim_model_infile="ErrorModelSolexa36bp.mconf", metasim_no_reads=10, metasim_pdir=self.metasim_dir,
                                    metasim_taxon_infile="MetaSim_bint.mprf")
        self.assembly.add_all_param(mine_pdir=self.mine_dir, mine_comparison_style="-allPairs")
        self.assembly.add_all_param(blast_wdir=self.blast_dir, records="dictionary", e_value=1e-15, outfile=None)
        self.assembly.init_program()
        self.assembly.run()


if __name__ == '__main__':
    unittest.main()
