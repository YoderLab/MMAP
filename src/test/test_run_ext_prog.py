'''
Created on Jan 23, 2012

@author: Steven Wu
'''
import unittest
from core.run_ext_prog import runExtProg
from core.utils import path_utils
import os.path



class TestRunExtProg(unittest.TestCase):


    def test_RunExtProg_append_reset_switch(self):
        self.p1 = runExtProg("ls")
       
        self.assertListEqual(self.p1.get_switch(), [])
        
        self.p1.add_switch("-l")
        self.assertListEqual(self.p1.get_switch(), ["-l"])
        self.p1.add_switch("-s")
        self.assertListEqual(self.p1.get_switch(), ["-l","-s"])
        self.p1.add_switch(["-1","-2"])
        self.assertListEqual(self.p1.get_switch(), ["-l","-s","-1","-2"])
        self.p1.add_switch(["-x"])
        self.assertListEqual(self.p1.get_switch(), ["-l","-s","-1","-2","-x"])
        
        self.p1.reset_switch()
        self.assertListEqual(self.p1.get_switch(), [])
        self.p1.add_switch(["-a","-b"])
        self.assertListEqual(self.p1.get_switch(), ["-a","-b"])

    def test_RunExtProg_set_switch(self):
        self.p1 = runExtProg("ls")
        self.assertListEqual(self.p1.get_switch(), [])
        
        self.p1.set_switch("-l")
        self.assertListEqual(self.p1.get_switch(), ["-l"])
        self.p1.set_switch("-s")
        self.assertListEqual(self.p1.get_switch(), ["-s"])
        self.p1.set_switch(["-111","-222"])
        self.assertListEqual(self.p1.get_switch(), ["-111","-222"])


    def test_RunExtProg_run_command(self):
        self.p1 = runExtProg("ls")
        self.p1.add_switch("-l")
        self.p1.run()
        self.out = self.p1.output
        self.assertTrue(self.out.find("main.py"))
        self.assertTrue(self.out.find("test_run_ext_prog.py"))
        
#        print "\noutput:\n",self.out
        
    def test_RunExtProg_run_program(self):

        self.data_dir = path_utils.get_data_dir()
        self.outFileName = "tempAlignmentOutput.fasta"
        if os.path.isfile(self.data_dir+self.outFileName):
            os.remove(self.data_dir+self.outFileName)
        
        self.assertFalse(os.listdir(self.data_dir).count(self.outFileName))
        
        self.p2 = runExtProg("./muscle3.8.31_i86linux64")
        self.p2.cwd = self.data_dir
        self._switch = "-in testAlignmentInput.fasta -out".split()
        self._switch.append(self.outFileName)
        
        self.p2.add_switch( self._switch )
        self.p2.run()
        self.out = self.p2.errors #not sure why output capture by stderr, but it works
        
        self.assertTrue(os.listdir(self.data_dir).count(self.outFileName))
        self.assertTrue(self.out.find("MUSCLE v3.8.31"))
        self.assertTrue(self.out.find("testAlignmentInput 2 seqs"))
        
        #clean up
        os.remove(self.data_dir+self.outFileName)
        
    def test_RunExtProg_update_switch(self):
        self.p1 = runExtProg("ls")
        
        self.p1.add_switch(["-a", "1", "--b", "2"])
        self.assertListEqual(self.p1.get_switch(), ["-a", "1", "--b", "2"])
        self.p1.updateSwitch("-a", "3")
        self.assertListEqual(self.p1.get_switch(), ["-a", "3", "--b", "2"])
        self.p1.updateSwitch("-c", "4")
        self.assertListEqual(self.p1.get_switch(), ["-a", "3", "--b", "2", "-c", "4"])
        self.p1.updateSwitch("-b", "5")
        self.assertListEqual(self.p1.get_switch(), ["-a", "3", "--b", "2", "-c", "4", "-b", "5"])
        self.p1.updateSwitch("-C", "6")
        self.assertListEqual(self.p1.get_switch(), ["-a", "3", "--b", "2", "-c", "4", "-b", "5", "-C", "6"])
        self.p1.updateSwitch("--b", "7")
        self.assertListEqual(self.p1.get_switch(), ["-a", "3", "--b", "7", "-c", "4", "-b", "5", "-C", "6"])
        
    def test_RunExtProg_toggle_switch(self):
        self.p1 = runExtProg("ls")
        
        self.p1.add_switch(["-a", "1"])
        self.p1.toggleSwitch("-t")
        self.assertListEqual(self.p1.get_switch(), ["-a", "1", "-t"])
        self.p1.toggleSwitch("-t")
        self.assertListEqual(self.p1.get_switch(), ["-a", "1"])
        self.p1.toggleSwitch("-t", 0)
        self.assertListEqual(self.p1.get_switch(), ["-a", "1"])
        self.p1.toggleSwitch("-t", 1)
        self.assertListEqual(self.p1.get_switch(), ["-a", "1", "-t"])
        self.p1.toggleSwitch("-t", 1)
        self.assertListEqual(self.p1.get_switch(), ["-a", "1", "-t"])
        self.p1.toggleSwitch("-t", 0)
        self.assertListEqual(self.p1.get_switch(), ["-a", "1"])



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()