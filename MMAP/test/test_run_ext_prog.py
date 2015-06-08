'''
Created on Jan 23, 2012

@author: Steven Wu
'''
from core import run_ext_prog
from core.run_ext_prog import runExtProg
from core.utils import path_utils
import os.path
import unittest


class TestRunExtProg(unittest.TestCase):

    platform = run_ext_prog.get_platform()

    def setUp(self):
        self.data_dir = path_utils.get_data_dir() + "/unittest_data/"

    def test_RunExtProg_append_reset_switch(self):
        prog1 = runExtProg("ls")
        self.assertEqual(prog1.get_all_switches(), [])

        prog1.add_switch("-l")
        self.assertEqual(prog1.get_all_switches(), ["-l"])

        prog1.add_switch("-s")
        self.assertEqual(prog1.get_all_switches(), ["-l", "-s"])

        prog1.add_switch(["-1", "-2"])
        self.assertEqual(prog1.get_all_switches(), ["-l", "-s", "-1", "-2"])

        prog1.add_switch(["-x"])
        self.assertEqual(prog1.get_all_switches(), ["-l", "-s", "-1", "-2", "-x"])

        prog1.reset_switch()
        self.assertEqual(prog1.get_all_switches(), [])

        prog1.add_switch(["-a", "-b"])
        self.assertEqual(prog1.get_all_switches(), ["-a", "-b"])

    def test_RunExtProg_set_switch(self):
        prog1 = runExtProg("ls")
        self.assertEqual(prog1.get_all_switches(), [])

        prog1.set_switch("-l")
        self.assertEqual(prog1.get_all_switches(), ["-l"])

        prog1.set_switch("-s")
        self.assertEqual(prog1.get_all_switches(), ["-s"])

        prog1.set_switch(["-111", "-222"])
        self.assertEqual(prog1.get_all_switches(), ["-111", "-222"])

    def test_RunExtProg_run_command(self):
        prog1 = runExtProg("ls")
        prog1.add_switch("-l")
        prog1.run()
        self.out = prog1.output
        self.assertTrue(self.out.find("main.py"))
        self.assertTrue(self.out.find("test_run_ext_prog.py"))

#        print "\noutput:\n",self.out
    @unittest.skip("#TODO: not testing muscle alignment")
    def test_RunExtProg_run_program(self):

        self.filename = "tempAlignmentOutput.fasta"
        if os.path.isfile(self.data_dir + self.filename):
            os.remove(self.data_dir + self.filename)

        self.assertFalse(os.listdir(self.data_dir).count(self.filename))

        prog2 = runExtProg("./muscle3.8.31_i86linux64", pdir=self.data_dir)
        self._switch = "-in testAlignmentInput.fasta -out".split()
        self._switch.append(self.filename)

        prog2.add_switch(self._switch)
        prog2.run()
        self.out = prog2.errors  # not sure why output capture by stderr, but it works
        self.assertTrue(os.listdir(self.data_dir).count(self.filename))
        self.assertTrue(self.out.find("MUSCLE v3.8.31"))
        self.assertTrue(self.out.find("testAlignmentInput 2 seqs"))

        # clean up
        os.remove(self.data_dir + self.filename)

    def test_RunExtProg_update_switch(self):
        prog1 = runExtProg("ls")

        prog1.add_switch(["-a", "1", "--b", "2"])
        self.assertEqual(prog1.get_all_switches(), ["-a", "1", "--b", "2"])
        prog1.update_switch("-a", "3")
        self.assertEqual(prog1.get_all_switches(), ["-a", "3", "--b", "2"])
        prog1.update_switch("-c", "4")
        self.assertEqual(prog1.get_all_switches(), ["-a", "3", "--b", "2", "-c", "4"])
        prog1.update_switch("-b", "5")
        self.assertEqual(prog1.get_all_switches(), ["-a", "3", "--b", "2", "-c", "4", "-b", "5"])
        prog1.update_switch("-C", "6")
        self.assertEqual(prog1.get_all_switches(), ["-a", "3", "--b", "2", "-c", "4", "-b", "5", "-C", "6"])
        prog1.update_switch("--b", "7")
        self.assertEqual(prog1.get_all_switches(), ["-a", "3", "--b", "7", "-c", "4", "-b", "5", "-C", "6"])

    def test_RunExtProg_toggle_switch(self):
        prog1 = runExtProg("ls")
        prog1.add_switch(["-a", "1"])
        prog1.toggle_switch("-t")
        self.assertEqual(prog1.get_all_switches(), ["-a", "1", "-t"])

        prog1.toggle_switch("-t")
        self.assertEqual(prog1.get_all_switches(), ["-a", "1"])

        prog1.toggle_switch("-t", 0)
        self.assertEqual(prog1.get_all_switches(), ["-a", "1"])

        prog1.toggle_switch("-t", 1)
        self.assertEqual(prog1.get_all_switches(), ["-a", "1", "-t"])

        prog1.toggle_switch("-t", 1)
        self.assertEqual(prog1.get_all_switches(), ["-a", "1", "-t"])

        prog1.toggle_switch("-t", 0)
        self.assertEqual(prog1.get_all_switches(), ["-a", "1"])

    def test_RunExtProg_check(self):

        prog1 = runExtProg("./program1", pdir=self.data_dir, check_OS=True)
        self.assertEqual(prog1.program_name, "./program1_" + TestRunExtProg.platform)

        prog1 = runExtProg("./muscle3.8.31_i86linux64", pdir=self.data_dir, check_OS=True)
        self.assertEqual(prog1.program_name, "./muscle3.8.31_i86linux64")

        with self.assertRaises(TypeError):
            runExtProg("./muscle3.8.31_i86linux64", check_OS=True)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

# suite = unittest.TestLoader().loadTestsFromTestCase(TestRunExtProg)
# unittest.TextTestRunner(verbosity=2).run(suite)
