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
        print genovo.assemble.get_switch()
        self.assertEqual(genovo.assemble.get_switch()[0], infile_var)
        self.assertEqual(genovo.assemble.get_switch(), [infile_var, "1"])
        self.assertListEqual(genovo.finalize.get_switch(), ["10", "all_reads.fa", infile_var+".dump.best"])
        

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
#   def_test_ClassName_mhatAreWeTestingHere(self)
        infile_var="newname.fasta"
        genovo = RunGenovo(infile=infile_var, pdir = self.data_dir, noI=3, thresh=250)
        self.assertEqual(3, len(genovo.finalize._switch) )
        self.assertListEqual(genovo.finalize.get_switch(), ["250", "newname_out.fasta", infile_var+".dump.best"])
    
        genovo.setCutoff(300)
        self.assertListEqual(genovo.finalize.get_switch(), ["300", "newname_out.fasta", infile_var+".dump.best"])
        
        infile_var="VICTORY!!!.fasta"
        genovo.setInfileName(infile_var)
        self.assertListEqual(genovo.finalize.get_switch(), ["300", "newname_out.fasta", infile_var+".dump.best"])


    def test_RunGenovo_finalise_outfile(self):




#    def test_RunGenovo_setNumberOfIter(self):   
#        infile_var="newname.fasta"
#        genovo = RunGenovo(infile=infile_var, pdir = self.data_dir, noI=3, thresh=250)
#        self.assertRaises(ValueError, genovo.setNumberOfIter, 1.1)
#        self.assertRaises(ValueError, genovo.setNumberOfIter, -1)
#        self.assertRaises(TypeError, genovo.setNumberOfIter, "string")












    def test_RunGenovo_set_dir(self):
        infile_var="newname.fasta"
        dir = self.data_dir[:-1]
        genovo = RunGenovo(infile=infile_var, pdir = dir, noI=3, thresh=250)
        self.assertEqual(genovo.pdir, self.data_dir)
        
        
    def test_RunGenovo_set_infile_outfile(self):
        infile_var="test_infile.fasta"
        outfile_var="test_outfile.fasta"
        genovo = RunGenovo(infile=infile_var, outfile = outfile_var, pdir = self.data_dir, noI=3, thresh=250)
        self.assertListEqual(genovo.assemble.get_switch(), [infile_var, "3"])
        self.assertListEqual(genovo.finalize.get_switch(), [250, outfile_var, infile_var+".dump.fastaS"])
        
        infile_var="test_infile2.fasta"
        genovo.setInfileName(infile_var)
        self.assertListEqual(genovo.assemble.get_switch(), [infile_var, "3"])
        self.assertListEqual(genovo.finalize.get_switch(), [250, outfile_var, infile_var+".dump.fastaS"])
        
        outfile_var="test_outfile2.fasta"
        genovo.setSwitchOutput(infile_var) # TODO need fix name here
        self.assertListEqual(genovo.assemble.get_switch(), [infile_var, "3"])
        self.assertListEqual(genovo.finalize.get_switch(), [250, outfile_var, infile_var+".dump.fastaS"])
        
    
        
#    def test_RunGenovo_set_cutoff(self):   
#        infile_var="newname.fasta"
#        genovo = RunGenovo(infile=infile_var, pdir = self.data_dir, noI=3, thresh=250)
#        self.assertRaises(ValueError, genovo.setCutoff, 1.1)
#        self.assertRaises(ValueError, genovo.setCutoff, -1)
#        self.assertRaises(TypeError, genovo.setCutoff, "string")    
#        










