from core.assembler.software_assembler import SoftwareAssembler

__author__ = 'erinmckenney'

import unittest


class TestSoftwareAssembler(unittest.TestCase):

    def setUp(self):
        self.assembly=SoftwareAssembler()
    pass


    def test_SoftwareAssembler_set_all_param(self):

        self.assembly.add_all_param(genovo_infile="gInfile", outfile="gOutfile", genovo_thresh=2)
        expected = {"genovo_infile":"gInfile", "outfile":"gOutfile", "genovo_thresh":2}
        self.assertEqual(self.assembly.get_all_par(), expected)

        self.assembly.add_all_param(glimmer_outfile="glimOutfile", glimpar="testAddPar",genovo_thresh=14)
        expected = {"genovo_infile":"gInfile", "outfile":"gOutfile", "genovo_thresh":14,
                    "glimmer_outfile":"glimOutfile", "glimpar":"testAddPar"}
        self.assertEqual(self.assembly.get_all_par(), expected)
#        self.assertEqual(True, False)

    def test_SoftwareAssembler_init_program(self):
        self.assembly.add_all_param(genovo_infile="gInfile", genovo_thresh=14, genovo_pdir="g_p_dir", genovo_noI=2)
        self.assembly.add_all_param(glimmer_pdir="glib_pdir")
        self.assembly.init_program()
#        self.assembly.run()

if __name__ == '__main__':
    unittest.main()
