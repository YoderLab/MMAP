"""
Created on Mar 20, 2012

@author: Steven Wu
"""
import unittest
from core.component.run_Genovo import RunGenovo
from core import run_ext_prog
from core.utils import path_utils
import os

class TestRunGenovo(unittest.TestCase):

    platform = run_ext_prog.get_platform()
    
    def setUp(self):
        self.longMessage = True
        self.data_dir = path_utils.get_data_dir()+"Genovo/"


    def tearDown(self):
        pass

    def test_RunGenovo_init(self):
        infile_var = "all_reads.fa"
        genovo = RunGenovo(infile_var, pdir=self.data_dir,  noI=1, thresh=10)
        self.assertEqual(genovo.assemble.get_switch()[0], infile_var)
        self.assertEqual(genovo.assemble.get_switch(), [infile_var, "1"])
        self.assertListEqual(genovo.finalize.get_switch(), ["10", "all_reads_out.fasta", infile_var+".dump.best"])
          

    def test_RunGenovo_simple_assemble(self):
        infile_var = "all_read.fa"
        genovo = RunGenovo(infile=infile_var, pdir = self.data_dir, noI=3, thresh=250, checkExist=False)
        self.assertListEqual(genovo.assemble.get_switch(), [infile_var, "3"])
        
        genovo.setNumberOfIter(10)
        self.assertListEqual(genovo.assemble.get_switch(), [infile_var, "10"])
        
        infile_var="test_infile.fasta"
        genovo.setInfileName(infile_var)
        self.assertListEqual(genovo.assemble.get_switch(), [infile_var, "10"])
       
        
    def test_RunGenovo_simple_finalise(self):
#   def_test_ClassName_whatAreWeTestingHere(self)
        infile_var="test_infile.fasta"
        genovo = RunGenovo(infile=infile_var, pdir = self.data_dir, noI=3, thresh=250, checkExist=False)
        self.assertEqual(3, len(genovo.finalize._switch) )
        self.assertListEqual(genovo.finalize.get_switch(), ["250", "test_infile_out.fasta", infile_var+".dump.best"])
    
        genovo.setCutoff(300)
        self.assertListEqual(genovo.finalize.get_switch(), ["300", "test_infile_out.fasta", infile_var+".dump.best"])
        
        infile_var="VICTORY!!!.fasta"
        genovo.setInfileName(infile_var)
        self.assertListEqual(genovo.finalize.get_switch(), ["300", "test_infile_out.fasta", infile_var+".dump.best"])


    def test_RunGenovo_finalise_outfile(self):
    #   def_test_ClassName_mhatAreWeTestingHere(self)
        infile_var="test_infile.fasta"
        outfile_var="testOutfile.fasta"
        genovo = RunGenovo(infile=infile_var, outfile=outfile_var, pdir = self.data_dir, noI=3, thresh=250, checkExist=False)
        self.assertEqual(3, len(genovo.finalize._switch) )
        self.assertListEqual(genovo.finalize.get_switch(), ["250", outfile_var, infile_var+".dump.best"])

        genovo2 = RunGenovo(infile=infile_var,  pdir = self.data_dir, noI=3, thresh=250, checkExist=False)   ## outfile == None
        self.assertListEqual(genovo2.finalize.get_switch(), ["250", "test_infile_out.fasta", infile_var+".dump.best"])
        infile_var="test_infile.xyz.fasta.abc"
        genovo2 = RunGenovo(infile=infile_var,  pdir = self.data_dir, noI=3, thresh=250, checkExist=False)   ## outfile == None
        self.assertListEqual(genovo2.finalize.get_switch(), ["250", "test_infile.xyz.fasta_out.fasta", infile_var+".dump.best"])

        infile_var="test_infile"
        genovo2 = RunGenovo(infile=infile_var,  pdir = self.data_dir, noI=3, thresh=250, checkExist=False)   ## outfile == None
        self.assertListEqual(genovo2.finalize.get_switch(), ["250", "test_infile_out.fasta", infile_var+".dump.best"])


    def test_RunGenovo_set_infile_outfile(self):
        infile_var="test_infile.fasta"
        outfile_var="test_outfile.fasta"
        genovo = RunGenovo(infile=infile_var, outfile = outfile_var, pdir = self.data_dir, noI=3, thresh=250, checkExist=False)
        self.assertListEqual(genovo.assemble.get_switch(), [infile_var, "3"])
        self.assertListEqual(genovo.finalize.get_switch(), ["250", outfile_var, infile_var+".dump.best"])
        
        infile_var="test_infile2.fasta"
        genovo.setInfileName(infile_var)
        self.assertListEqual(genovo.assemble.get_switch(), [infile_var, "3"])
        self.assertListEqual(genovo.finalize.get_switch(), ["250", outfile_var, infile_var+".dump.best"])
        
        outfile_var="test_outfile2.fasta"
        genovo.setFinalizeOutfile(outfile_var) 
        self.assertListEqual(genovo.assemble.get_switch(), [infile_var, "3"])
        self.assertListEqual(genovo.finalize.get_switch(), ["250", outfile_var, infile_var+".dump.best"])
        
           


    def test_RunGenovo_setNumberOfIter(self):
        infile_var="test_infile.fasta"
        genovo = RunGenovo(infile=infile_var, pdir = self.data_dir, noI=3, thresh=250, checkExist=False)
        self.assertRaises(TypeError, genovo.setNumberOfIter, 1.1)
        self.assertRaises(TypeError, genovo.setNumberOfIter, -1)
        self.assertRaises(TypeError, genovo.setNumberOfIter, "string")
        self.assertRaises(TypeError, genovo.setNumberOfIter, "5")



    def test_RunGenovo_setCutoff(self):
        """
        Note: There are different type of Errors
        Feel free to change/swap/move between ValueError and TypeError
        """   
        infile_var="test_infile.fasta"
        genovo = RunGenovo(infile=infile_var, pdir = self.data_dir, noI=3, thresh=250, checkExist=False)
        self.assertRaises(ValueError, genovo.setCutoff, 1.1)
        self.assertRaises(ValueError, genovo.setCutoff, -1)
        self.assertRaises(ValueError, genovo.setCutoff, -2.5)
        self.assertRaises(TypeError, genovo.setCutoff, "string")
        self.assertRaises(TypeError, genovo.setCutoff, "3")


    def test_RunGenovo_check_directory_name(self):
        """
        check if directory name is valid
        """        
        infile_var="test_infile.fasta"
        dir = self.data_dir[:-1]
        genovo = RunGenovo(infile=infile_var, pdir = dir, noI=3, thresh=250, checkExist=False)
        self.assertEqual(genovo.pdir, self.data_dir, "need append \"/\" to dir")
        

    def test_RunGenovo_infile_not_exist(self):
        """
        check if infile and/or file directory exist
        """        
        
        infile_var = "fileDoesNotExist"
        with self.assertRaises(IOError):
            RunGenovo(infile=infile_var, pdir = self.data_dir, noI=3, thresh=250, checkExist= True)
        
        invalid_dir = "/RandomDirThatDoesNotExist/"
        with self.assertRaises(IOError):
            RunGenovo(infile=infile_var, pdir = invalid_dir, noI=3, thresh=250, checkExist= True)
        


    def test_RunGenovo_outfile_already_exist(self):
        """
        check if out file alread exist,
        maybe should not raise error, should
        TODO: maybe it should be handle it at different way, auto rename? 
        """
        infile_var="test_infile.fasta"
        outfile_var = "testOutFileAlreadyExist.fasta"
        with self.assertRaises(IOError):
            RunGenovo(infile=infile_var, outfile = outfile_var, pdir = self.data_dir, noI=3, thresh=250, checkExist= True)
        
        
    def test_RunGenovo_checkAssembleResultExist(self):
        """
        check if ./assemble finished running, shoulde produce 3 output files
        only pass if all 3 exist
        """
        infile_var="test_infile.fasta"
        genovo = RunGenovo(infile=infile_var, pdir = self.data_dir, noI=10, thresh=250, checkExist=False)
        self.assertTrue( genovo.checkAssembleResultExist() )

        # negative test, outfiles are not suppose to exist
        infile_var="fileNotExist.fasta"
        genovo = RunGenovo(infile=infile_var, pdir = self.data_dir, noI=10, thresh=250, checkExist=False)
        self.assertFalse( genovo.checkAssembleResultExist() )

    def test_RunGenove_readFinalizeOutfile(self):
        """
        check if it can "read" assembled contig
        TODO: have check what happen in the file format is invalid, assuming its the correct fasta now
        """
        infile_var="test_infile.fasta"
        outfile_var="test_outfile.fasta"
        genovo = RunGenovo(infile=infile_var, outfile = outfile_var, pdir = self.data_dir, noI=10, thresh=250, checkExist=False)
        result = genovo.readFinalizeOutfile()
        self.assertEqual(len(result), 2)
        self.assertEqual(result.keys(), ["1","2"])
        
        expected = [170,60]
        for i, key in enumerate(result):
            self.assertEqual(len(result[key]), expected[i])
            
            
#    
#    def test_RunGenovo_run(self):
#        infile_var="test_run_infile.fasta"
#        outfile_var="test_run_outfile.fasta"
#        genovo = RunGenovo(infile=infile_var, outfile = outfile_var, pdir = self.data_dir, noI=10, thresh=100, checkExist=False)
#        genovo.run()
#        self.assertTrue( genovo.checkAssembleResultExist() )
#        
    
