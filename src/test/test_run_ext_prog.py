'''
Created on Jan 23, 2012

@author: Steven Wu
'''
import unittest
from core.run_ext_prog import runExtProg
from core.utils import path_utils
import os.path



class TestRunExtProgram(unittest.TestCase):


    def test_addResetSwitch(self):
        self.p1 = runExtProg("ls")
        self.assertListEqual(self.p1.switch, [])
        
        self.p1.append_switch("-l")
        self.assertListEqual(self.p1.switch, ["-l"])
        self.p1.append_switch("-s")
        self.assertListEqual(self.p1.switch, ["-l","-s"])
        self.p1.append_switch(["-1","-2"])
        self.assertListEqual(self.p1.switch, ["-l","-s","-1","-2"])
        self.p1.append_switch(["-x"])
        self.assertListEqual(self.p1.switch, ["-l","-s","-1","-2","-x"])
        
        self.p1.reset_switch()
        self.assertListEqual(self.p1.switch, [])
        self.p1.append_switch(["-a","-b"])
        self.assertListEqual(self.p1.switch, ["-a","-b"])
        




    def test_runCommand(self):
        self.p1 = runExtProg("ls")
        self.p1.append_switch("-l")
        self.p1.run()
        self.out = self.p1.output
        self.assertTrue(self.out.find("main.py"))
        self.assertTrue(self.out.find("test_run_ext_prog.py"))
        
#        print "\noutput:\n",self.out
        
    def test_runProgram(self):

        self.data_dir = path_utils.get_data_dir()
        self.outFileName = "testAlignmentOutput.fasta"
        if os.path.isfile(self.data_dir+self.outFileName):
            os.remove(self.data_dir+self.outFileName)
        
        self.assertFalse(os.listdir(self.data_dir).count(self.outFileName))
        
        self.p2 = runExtProg("./muscle3.8.31_i86linux64")
        self.p2.cwd = self.data_dir
        self.switch = "-in testAlignmentInput.fasta -out".split()
        self.switch.append(self.outFileName)
        
        self.p2.append_switch( self.switch )
        self.p2.run()
        self.out = self.p2.errors #not sure why output capture by stderr, but it works
        
        self.assertTrue(os.listdir(self.data_dir).count(self.outFileName))
        self.assertTrue(self.out.find("MUSCLE v3.8.31"))
        self.assertTrue(self.out.find("testAlignmentInput 2 seqs"))

        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()