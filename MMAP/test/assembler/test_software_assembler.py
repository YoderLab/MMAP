from core.assembler.software_assembler import SoftwareAssembler
from core.setting import Setting, list_all_optionals
from core.utils import path_utils
import core
from core.component import run_genovo

__author__ = 'erinmckenney'

import unittest


class TestSoftwareAssembler(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.list_all_parameters = []
        cls.list_all_parameters.extend(core.setting.list_essential_genovo_only)
        cls.list_all_parameters.extend(core.setting.list_essential_glimmer_only)
        cls.list_all_parameters.extend(core.setting.list_essential_blast_only)
        cls.list_all_parameters.extend(core.setting.list_optional_shared)
        cls.list_all_parameters.extend(core.setting.list_optional_genovo_only)
        cls.list_all_parameters.extend(core.setting.list_optional_glimmer_only)
        cls.list_all_parameters.extend(core.setting.list_optional_blast_only)
        cls.list_all_parameters.extend(core.setting.list_optional_internal_only)

    def setUp(self):
        self.maxDiff = None
        self.unittest_dir = path_utils.get_data_dir() + "unittest_data/"

        self.genovo_dir = path_utils.get_data_dir() + "Genovo/"
        self.glimmer_dir = path_utils.get_data_dir() + "Glimmer/"
        self.metasim_dir = path_utils.get_data_dir() + "MetaSim/"
        self.mine_dir = path_utils.get_data_dir() + "MINE/"
        self.blast_dir = path_utils.get_data_dir() + "BLAST/"
        self.working_dir = path_utils.get_data_dir() + "test_data/"



#    def test_set_all_param(self):
#
#        setting = Setting();
#        setting.add_all(genovo_infile="gInfile",
#                                    filename="gOutfile", genovo_thresh=2)
#        self.assembly = SoftwareAssembler(setting)
#        expected = {"genovo_infile": "gInfile", "filename": "gOutfile",
#                    "genovo_thresh": 2}
#        self.assertEqual(self.assembly.get_all_par(), expected)
#
#        setting.add_all(glimmer_outfile="glimOutfile",
#                                    glimpar="testAddPar", genovo_thresh=14)
#        expected = {"genovo_infile": "gInfile", "filename": "gOutfile",
#                    "genovo_thresh": 14, "glimmer_outfile": "glimOutfile",
#                    "glimpar": "testAddPar"}
#        self.assertEqual(self.assembly.get_all_par(), expected)

    def test_init_program(self):
        setting = Setting();
        setting.add_all(genovo_infile="wdir_all_reads.fa",
                        genovo_pdir=self.genovo_dir)

        setting.add_all(glimmer_pdir=self.glimmer_dir)
        setting.add_all(wdir=self.working_dir)
#        setting.add_all(metasim_model_infile="ErrorModelSolexa36bp.mconf", metasim_no_reads=10, metasim_pdir=self.metasim_dir,
#                                    metasim_taxon_infile="MetaSim_bint.mprf")
        setting.add_all(mine_pdir=self.mine_dir, mine_comparison_style="-allPairs")
        setting.add_all(blast_infile="dictionary", blast_e_value=1e-15, blast_wdir=self.blast_dir, blast_outfile=None)

        assembly = SoftwareAssembler(setting)
        assembly.init_program()
#        assembly.run()


    def test_min_setting(self):
        infile = self.unittest_dir + "testControlFileMin"

        setting = Setting.create_setting_from_file(infile)
        assembler = SoftwareAssembler(setting)

        expected = set(TestSoftwareAssembler.list_all_parameters)
        self.assertEqual(expected, set(assembler.get_all_par().viewkeys()))

        print assembler.get_all_par().values()

    def test_missed_essential(self):

#        When not all essential parameters exist, should fail.
        infile = self.unittest_dir + "missedEssentials"
        with self.assertRaises(KeyError):
            setting = Setting.create_setting_from_file(infile)
            assembler = SoftwareAssembler(setting)

    def test_all_parameters(self):

        infile = self.unittest_dir + "allPass"

        setting = Setting.create_setting_from_file(infile)
        assembler = SoftwareAssembler(setting)


        expected = set(TestSoftwareAssembler.list_all_parameters)
        self.assertEqual(expected, set(assembler.get_all_par().viewkeys()))
        print assembler.get_all_par()
        print assembler.get_all_par().keys()
        print assembler.get_all_par().values

    def test_from_setting(self):

#
# #    When not all essential parameters exist, should fail.
#        infile="/Users/erinmckenney/Desktop/Pipeline/metaLem/data/unittest_data/missedEssentials"
#        test = ControlFile()
#        test.add_all(infile)
#        setting=Setting.create_setting_from_controlfile(test)
#        with self.assertRaises(KeyError):
#            SoftwareAssembler.create_SoftwareAssembler_from_setting(setting)

#    When not all essential parameters exist but no optional parameters exist, should pass.
        infile = self.unittest_dir + "testControlFile"

#        setting = Setting.create_setting_from_file(infile)
#        assembler = SoftwareAssembler(setting)
#
#        expected = set(core.setting.list_all_parameters)
#        self.assertEqual(expected, set(assembler.get_all_par().viewkeys()))

    def test_some_optional(self):
        infile = self.unittest_dir + "testControlFileOp1"

        setting = Setting.create_setting_from_file(infile)
        assembler = SoftwareAssembler(setting)

        expected = set(TestSoftwareAssembler.list_all_parameters)
        self.assertEqual(expected, set(assembler.get_all_par().viewkeys()))
        self.assertEqual(run_genovo.DEFAULT_GENOVO_NO_ITER, assembler.get("genovo_num_iter"))
        self.assertEqual("1e-10", assembler.get("blast_e_value"))




if __name__ == '__main__':
    unittest.main()
