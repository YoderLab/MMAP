"""
Created on Feb 1, 2012

@author: Steven Wu
"""
import unittest

from core.component.run_metaIDBA import RunMetaIDBA
from core.utils import path_utils
import os

@unittest.skip("No longer use metaibda")
class TestRunMetaIDBA(unittest.TestCase):

    def setUp(self):
        self.data_dir = path_utils.get_data_dir()


    def test_RunMetaIDBA_run(self):
        """
        TODO: how should we test this??
        The testMetaIDBA.fasta doesnt really work, just a (fail) example
        """

        self.outfile = "tempMetaIDBAOutput.fasta"

        if os.path.isfile(self.data_dir + self.outfile):
            os.remove(self.data_dir + self.outfile)
        self.assertFalse(os.listdir(self.data_dir).count(self.outfile))

        self.p1 = RunMetaIDBA(infile="testMetaIDBA.fasta", outfile=self.outfile, pdir=self.data_dir)
        self.p1.set_switch_min_k(1)
        self.p1.set_switch_max_k(2)
        self.p1.run()

        self.assertTrue(os.listdir(self.data_dir).count(self.outfile + "-contig.fa"))
        self.assertTrue(os.listdir(self.data_dir).count(self.outfile + ".align"))
        self.assertTrue(os.listdir(self.data_dir).count(self.outfile + ".graph"))
        self.assertTrue(os.listdir(self.data_dir).count(self.outfile + ".kmer"))

        # clean up
        os.remove(self.data_dir + self.outfile + "-contig.fa")
        os.remove(self.data_dir + self.outfile + ".align")
        os.remove(self.data_dir + self.outfile + ".graph")
        os.remove(self.data_dir + self.outfile + ".kmer")

    def test_RunMetaIDBA_parameters(self):

        self.p1 = RunMetaIDBA("test")
        self.p1.set_switch_max_k(100)
        self.p1.set_switch_min_k(1)
        self.assertLessEqual(self.p1.get_switch(), ["--read", "test", "--output", "test", "--maxk", "100", "--mink", "1"])
        self.p1.set_switch_max_k(500)
        self.p1.set_toggle_connect()
        self.assertLessEqual(self.p1.get_switch(), ["--read", "test", "--output", "test", "--maxk", "500", "--mink", "1", "--connect"])


    def test_RunMetaIDBA_read_contig(self):
        self.p1 = RunMetaIDBA("test")

#        self.assertRaises(IOError, self.p1.readContig())
#        
#        self.assertRaises(ValueError, self.p1.readContig())
        with self.assertRaises(IOError):
            self.p1.read_contig()

        self.p1.read_contig(self.data_dir + "AE014075_subTiny5.fasta")
#        print self.p1.record.__dict__
#        print self.p1.record.items()
#        print self.p1.record.values()
        for i in self.p1.record.keys():
            print i, self.p1.record[i]
            print "\n"
#        with self.assertRaises(ValueError):
#            self.p1.readContig()
#        pass

