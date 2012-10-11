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
import os

class TestGoConnector(unittest.TestCase):

    def setUp(self):
        CWD = os.getcwd()
        data_dir = path_utils.get_data_dir(CWD)
        infile = data_dir + "AE014075_subTiny5.fasta"#"AE014075_subSmall100.fasta"
        self.e_value_cut_off = 1e-15
        self.record_index = SeqIO.index(infile, "fasta")


    def tearDown(self):
        pass

    def test_GoConnector_empty(self):

        data = self.record_index["lcl|AE014075.1_gene_1"].seq ## good
        seq = Sequence(data)
        seq = go_connector.blast_AmiGO(seq)
        seq = go_connector.extract_ID(seq)
        seq = go_connector.parse_go_term(seq, self.e_value_cut_off)

        expected = set([])
        self.assertEqual(expected, seq.all_terms)

    @unittest.skip("")
    def test_GoConnector_short(self):

        data = self.record_index["lcl|AE014075.1_gene_2"].seq ## good
        seq = Sequence(data)
        seq = go_connector.blast_AmiGO(seq)
        seq = go_connector.extract_ID(seq)
        seq = go_connector.parse_go_term(seq, self.e_value_cut_off)

        expected = set(['GO:0004803', 'GO:0006313'])
        self.assertEqual(expected, seq.all_terms)

    @unittest.skip("")
    def test_GoConnector_long(self):

        data = self.record_index["lcl|AE014075.1_gene_3"].seq ## good
        seq = Sequence(data)
        seq = go_connector.blast_AmiGO(seq)
        seq = go_connector.extract_ID(seq)
        seq = go_connector.parse_go_term(seq, self.e_value_cut_off)

        expected = set(['GO:0071470', 'GO:0016310', 'GO:0005886', 'GO:0009067', 'GO:0000023', 'GO:0016597', 'GO:0043085', 'GO:0016491', 'GO:0005737', 'GO:0050661', 'GO:0040007', 'GO:0005618', 'GO:0009570', 'GO:0005634', 'GO:0006520', 'GO:0019877', 'GO:0000166', 'GO:0016740', 'GO:0009097', 'GO:0009090', 'GO:0019252', 'GO:0019761', 'GO:0016301', 'GO:0008152', 'GO:0009088', 'GO:0055114', 'GO:0009507', 'GO:0008652', 'GO:0005829', 'GO:0006555', 'GO:0004412', 'GO:0005575', 'GO:0009089', 'GO:0005524', 'GO:0006164', 'GO:0006531', 'GO:0009086', 'GO:0004072', 'GO:0009082'])
        self.assertEqual(expected, seq.all_terms)



#        dist_method = MatchingDistance()
#        dist_matirx = dist_method.cal_dist(seq)
#        print dist_matirx

