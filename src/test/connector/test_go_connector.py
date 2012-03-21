"""
Created on Mar 21, 2012

@author: Steven Wu
"""
import unittest
from core.sequence import Sequence
from core.connector import go_connector
from core.dist.matching_distance import MatchingDistance
from Bio import SeqIO
from core.utils import path_utils

class TestGoConnector(unittest.TestCase):

    def setUp(self):
        self.data_dir = path_utils.get_data_dir()


    def tearDown(self):
        pass

    @unittest.skip("not working. properly yet")
    def test_GoConnector_single(self):
        """
        TODO(Steven Wu): write this properly
        """
        
        e_value_cut_off = 1e-15
        infile = self.data_dir+"AE014075_subSmall100.fasta"
        record_index = SeqIO.index(infile, "fasta") # use index for large file
        #    test_single(record_index, e_value_cut_off)
        data = record_index["lcl|AE014075.1_gene_3"].seq ## good
        seq = Sequence(data)
        seq = go_connector.blast_AmiGO(seq)
        seq = go_connector.extract_ID(seq)
        
        seq = go_connector.parse_go_term(seq, e_value_cut_off)
        
        print "test set", seq.each_term 
        print "test set", seq.all_terms
    
        dist_method = MatchingDistance()
        dist_matirx = dist_method.cal_dist(seq)
        print dist_matirx

