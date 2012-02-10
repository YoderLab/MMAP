"""
Created on Feb 1, 2012

@author: Steven Wu
"""
import unittest

from core.component.run_metaIDBA import RunMetaIDBA
from core.utils import path_utils
import os


class TestRunMetaIDBA(unittest.TestCase):


    def testRunMetaIDBA_run(self):
        """
        TODO: how should we test this??
        The testMetaIDBA.fasta doesnt really work, just a (fail) example
        """
        self.data_dir = path_utils.get_data_dir();
        self.outFileName = "tempMetaIDBAOutput.fasta"

        if os.path.isfile(self.data_dir+self.outFileName):
            os.remove(self.data_dir+self.outFileName)
        self.assertFalse(os.listdir(self.data_dir).count(self.outFileName))

        self.p1 = RunMetaIDBA(infile="testMetaIDBA.fasta", outfile=self.outFileName, pdir=self.data_dir)
        self.p1.setSwitchMinK(1)
        self.p1.setSwitchMaxK(2)
        self.p1.run()

        self.assertTrue(os.listdir(self.data_dir).count(self.outFileName+"-contig.fa"))
        self.assertTrue(os.listdir(self.data_dir).count(self.outFileName+".align"))
        self.assertTrue(os.listdir(self.data_dir).count(self.outFileName+".graph"))
        self.assertTrue(os.listdir(self.data_dir).count(self.outFileName+".kmer"))
        
        # clean up
        os.remove(self.data_dir+self.outFileName+"-contig.fa")
        os.remove(self.data_dir+self.outFileName+".align")
        os.remove(self.data_dir+self.outFileName+".graph")
        os.remove(self.data_dir+self.outFileName+".kmer")
        
    
    def testRunMetaIDBA_parameters(self):
        
        self.p1 = RunMetaIDBA("test")
        self.p1.setSwitchMaxK(100)
        self.p1.setSwitchMinK(1)
        self.assertLessEqual(self.p1.getSwitch(), ["--read", "test", "--output", "None", "--maxk", "100", "--mink", "1"])
        self.p1.setSwitchMaxK(500)
        self.p1.setToggleConnect()
        self.assertLessEqual(self.p1.getSwitch(), ["--read", "test", "--output", "None", "--maxk", "500", "--mink", "1", "--connect"])


    def testRunMetaIDBA_readContig(self):
        pass
        
