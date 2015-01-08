"""
Created on Mar 21, 2012

@author: Steven Wu
"""
import math
import os
import pickle
import sys
import time
import unittest
from unittest.suite import TestSuite

from Bio import SeqIO

from core.amigo import go_connector
from core.amigo.go_connector import GOConnector
from core.amigo.go_sequence import GoSequence
from core.utils import path_utils


# from core.sequence import Sequence2, Sequence
class TestGoConnector(unittest.TestCase):
    '''
    
    '''
    def setUp(self):
        CWD = os.getcwd()
        self.data_dir = path_utils.get_data_dir(CWD)
        infile = self.data_dir + "AE014075_subTiny10.fasta"  # "AE014075_subSmall100.fasta"
        self.e_threshold = 1e-15
        self.record_index = SeqIO.index(infile, "fasta")



    def tearDown(self):
        pass

    def test_parse_seq(self):
        infile = self.data_dir + "BLAST/AmiGOBLASTResults_Gene_Local.html"
        webpage = open(infile, "r")
        data = ""
        for line in webpage:
            data += line
#         print data
        seq = GoSequence("gene5", data)
        seq.extract_ID()
        seq.parse_go_term(self.e_threshold, self.debug)


        expected = set(['GO:0005125', 'GO:0016311', 'GO:0046360', 'GO:0003674', 'GO:0030170', 'GO:0004795', 'GO:0005737', 'GO:0006566', 'GO:0005615', 'GO:0005634', 'GO:0006520', 'GO:0005524', 'GO:0008150', 'GO:0070905', 'GO:0008152', 'GO:0009071', 'GO:0008652', 'GO:0006897', 'GO:0005829', 'GO:0005575', 'GO:0009088', 'GO:0004765', 'GO:0016829'])

        self.assertEqual(expected, seq.combined_terms,
                         "Error!! \nExpected: %s\nActual: %s\n" % (sorted(expected), sorted(seq.combined_terms)))





#        data = self.record_index["lcl|AE014075.1_gene_5"].seq  # # good
#        seq = Sequence(data)

#        infile = self.data_dir + "BLAST/AmiGOBLASTResults_Gene5.html2"
#        webpage = open(infile, "w")
#        seq = go_connector.blast_AmiGO(seq)
#        webpage.write(seq.web_page)
#        seq = go_connector.extract_ID(seq)
#        seq = go_connector.parse_go_term(seq, self.e_threshold)
#        print seq.combined_terms

    def test_GoConnector_empty(self):

        data = self.record_index["lcl|AE014075.1_gene_1"].seq  # # good
        seq = GoSequence("G1", None)
        seq.blast_AmiGO(data)
        seq.extract_ID()
        seq.parse_go_term(self.e_threshold)

        expected = set([])
        self.assertEqual(expected, seq.combined_terms)

#    @unittest.skip("")
    def test_GoConnector_short(self):

        data = self.record_index["lcl|AE014075.1_gene_2"].seq  # # good
        seq = GoSequence("G2", None)
        seq.blast_AmiGO(data)
        seq.extract_ID()
        seq.parse_go_term(self.e_threshold)

        expected = set(['GO:0004803', 'GO:0006313'])
        self.assertEqual(expected, seq.combined_terms)

#    @unittest.skip("")
    def test_GoConnector_long(self):

        data = self.record_index["lcl|AE014075.1_gene_3"].seq  # # good
        seq = GoSequence("G3", None)
        seq.blast_AmiGO(data)
        seq.extract_ID()
        seq.parse_go_term(self.e_threshold)

        expected = set(['GO:0071470', 'GO:0016310', 'GO:0005886', 'GO:0009067', 'GO:0000023', 'GO:0016597', 'GO:0043085', 'GO:0016491', 'GO:0005737', 'GO:0050661', 'GO:0040007', 'GO:0005618', 'GO:0009570', 'GO:0005634', 'GO:0006520', 'GO:0019877', 'GO:0000166', 'GO:0016740', 'GO:0009097', 'GO:0009090', 'GO:0019252', 'GO:0019761', 'GO:0016301', 'GO:0008152', 'GO:0009088', 'GO:0055114', 'GO:0009507', 'GO:0008652', 'GO:0005829', 'GO:0006555', 'GO:0004412', 'GO:0005575', 'GO:0009089', 'GO:0005524', 'GO:0006164', 'GO:0006531', 'GO:0009086', 'GO:0004072', 'GO:0009082'])
        self.assertEqual(expected, seq.combined_terms)


    def test_batch_mode(self):
        """
        syntax:
        http://amigo1.geneontology.org/cgi-bin/amigo/blast.cgi?action=blast&seq=%3ES1%0ATTGAAAAACCTCCGGCTATGCCGGAGGATATTTATTTCGACCAAAGGTAACGAGGTAACAACCATGCGAGTGTTGAAGTTCGGCGGTACATCAGTGGCAAATGCAGAACGTTTTCTGCGGGTTGCCGATATTCTGGAA%3ES2%0AAGCAATGCCAGGCAGGGGCAGGTGGCCACCGTCCTCTCTGCCCCCGCCAAAATCACCAACCATCTGGTAGCGATGATTGAAAAAACCATTAGCGGCCAGGATGCTTTACCCAATATCAGCGATGCCGAACGTATTTTTGCCGAACTTCTGACGGGACTCGCCGCCGCCCAGCCGGGATTTCCGCTGGCACAATTGAAAACTTTCGTCGACCAGGAATTTGCCCAAATAAAACATGTCCTGCATGGCATCAGTTTGTTGGGGCAGTGCCCGGATAGCATCAACGCTGCGCTGATTTGCCGTGGCGAGAAAATGTCGATCGCCATTATGGCCGGCGTGTTAGAAGCGCGTGGTCACAACGTTACCGTTATCGATCCGGTCGAAAAA&CMD=Put
        http://amigo1.geneontology.org/cgi-bin/amigo/blast.cgi?action=blast&CMD=PUT&expect=0.001&seq=%3ES1%0ATTGTTATCGATCCGGTCGAAAAA
        
        http://amigo.geneontology.org/cgi-bin/amigo/blast.cgi?
        action=blast&seq=%3ES1%0ATTGAAAAACCTCCGGCTATGCCGGAGGATATTTATTTC....
                         %3ES2%0AAGCAATGCCAGGCAGGGGCAGGTGGCCACCGTCCTCTC...
                         &CMD=Put


filter
http://amigo1.geneontology.org/cgi-bin/amigo/blast.cgi?action=blast&CMD=Put&maxhits=200&threshold=0.0001&seq=%3ES1%0ATTGTTATCGATCCGGTCGAAAAA
        """
        infile = self.data_dir + "AE014075_subTiny10.fasta"  # "AE014075_subSmall100.fasta"
        record_index = SeqIO.index(infile, "fasta")

        go = GOConnector(record_index, 6)
        go.create_WebSessions_batches()
        self.assertEqual(2, len(go.web_session_list))

        go = GOConnector(record_index, 3)
        go.create_WebSessions_batches()
        self.assertEqual(4, len(go.web_session_list))

        go = GOConnector(record_index, 2)
        go.create_WebSessions_batches()
        self.assertEqual(5, len(go.web_session_list))

        self.tempfile = self.data_dir + "Amigo_Tempfile"
        try:
            os.remove(self.tempfile)
        except OSError:
            pass
        batch_size = 4
        go = GOConnector(record_index, batch_size, tempfile=self.tempfile)
        count = go.amigo_batch_mode()

        expected = set(['lcl|AE014075.1_gene_1', 'lcl|AE014075.1_gene_2', 'lcl|AE014075.1_gene_3',
                        'lcl|AE014075.1_gene_4', 'lcl|AE014075.1_gene_5', 'lcl|AE014075.1_gene_6',
                        'lcl|AE014075.1_gene_7', 'lcl|AE014075.1_gene_8', 'lcl|AE014075.1_gene_9',
                        'lcl|AE014075.1_gene_10'])
        expected_count = math.ceil(10.0 / 4)
        self.assertEqual(expected_count, count)  # 10/4 round up to 3
        for seq in go.all_seqs:
            self.assertTrue(seq.seq_id in expected, seq.seq_id)

        go = GOConnector(record_index, batch_size, tempfile=self.tempfile)
        count = go.amigo_batch_mode()  # do nothing
        self.assertEqual(0, count)


        tempout = open(self.tempfile, "r")
        all_lines = tempout.readlines()
        tempout.close()
        tempout = open(self.tempfile, "w")
        for line in all_lines:
            tempout.write(line)
            if line.startswith("ENDResult"):
                break
        tempout.close()

        go = GOConnector(record_index, batch_size, tempfile=self.tempfile)
        resume_count = go.amigo_batch_mode()
        self.assertEqual(expected_count - 1, resume_count)

if __name__ == '__main__':
#    unittest.main(verbosity=2)
#    Test = TestGoConnector()
    suite = TestSuite()
#    suite.addTest(TestGoConnector("test_parse_seq"))
    suite.addTest(TestGoConnector("test_batch_mode"))
#    suite.addTest(TestGoConnector("test_GoConnector_long"))
    unittest.TextTestRunner().run(suite)
