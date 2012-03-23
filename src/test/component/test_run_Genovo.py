"""
Created on Mar 20, 2012

@author: Steven Wu
"""
import unittest
from core.component.run_Genovo import RunGenovo
from core import run_ext_prog
from core.utils import path_utils

class TestRunGenovo(unittest.TestCase):

    platform = run_ext_prog.get_platform()
        
    def setUp(self):
        self.data_dir = path_utils.get_data_dir()


    def tearDown(self):
        pass

    def test_RunGenovo_init(self):
        infile_var = "all_reads.fa"
        genovo = RunGenovo(infile_var, pdir=self.data_dir,  noI=1, thresh=10)
        self.assertEqual(genovo.assemble.get_switch()[0], infile_var)
        self.assertEqual(genovo.assemble.get_switch(), [infile_var, "1"])


    def test_RunGenovo_simple_assemble(self):
        infile_var = "testMetaIDBA.fasta"
        genovo = RunGenovo(infile=infile_var, pdir = self.data_dir, noI=3, thresh=250)
        self.assertListEqual(genovo.assemble.get_switch(), [infile_var, "3"])
        
        genovo.setNumberOfIter(10)
        self.assertListEqual(genovo.assemble.get_switch(), [infile_var, "10"])
        
        infile_var="newname.fasta"
        genovo.setInfileName(infile_var)
        self.assertListEqual(genovo.assemble.get_switch(), [infile_var, "10"])
       
        
    def test_RunGenovo_simple_finalise(self):
        
        infile_var="newname.fasta"
        genovo = RunGenovo(infile=infile_var, pdir = self.data_dir, noI=3, thresh=250)
        self.assertEqual(3, len(genovo.finalize._switch) )
        self.assertListEqual(genovo.finalize.get_switch(), ["250", infile_var, infile_var+".dump.best"])
    
        genovo.setCutoff(300)
        self.assertListEqual(genovo.finalize.get_switch(), ["300", infile_var, infile_var+".dump.best"])
        
        infile_var="VICTORY!!!.fasta"
        genovo.setInfileName(infile_var)
        self.assertListEqual(genovo.finalize.get_switch(), ["300", infile_var, infile_var+".dump.best"])
        
#
#    def test_RunGenovo_setNumberOfIter(self):   
#        infile_var="newname.fasta"
#        genovo = RunGenovo(infile=infile_var, pdir = self.data_dir, noI=3, thresh=250)
#        self.assertRaises(ValueError, genovo.setNumberOfIter, 1.1)
#        self.assertRaises(ValueError, genovo.setNumberOfIter, -1)
#        self.assertRaises(TypeError, genovo.setNumberOfIter, "string")
