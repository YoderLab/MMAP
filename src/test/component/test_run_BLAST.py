"""
Created on Aug 27, 2012

@author: Steven Wu
"""
import unittest
import os


from core.connector import go_connector
from core.utils import path_utils
from core.component.run_BLAST import RunBlast
from Bio import SeqIO
from core.sequence import Sequence




class TestClass(unittest.TestCase):

    def setUp(self):

        CWD = os.getcwd()
        data_dir = path_utils.get_data_dir(CWD)
        infile = data_dir + "AE014075_subTiny5.fasta"#"AE014075_subSmall100.fasta"
        self.e_value_cut_off = 1e-15
        self.record_index = SeqIO.index(infile, "fasta")


    def tearDown(self):
        pass


    @unittest.skip("run this later")
    def test_RunBlast(self):

        blast = RunBlast(self.record_index, self.e_value_cut_off)
        blast.run()

        expected = dict({'lcl|AE014075.1_gene_1':set([]),
                        'lcl|AE014075.1_gene_2':set(['GO:0004803', 'GO:0006313']),
                        'lcl|AE014075.1_gene_3':set(['GO:0071470', 'GO:0016310', 'GO:0005886', 'GO:0009067', 'GO:0000023', 'GO:0016597', 'GO:0043085', 'GO:0016491', 'GO:0005737', 'GO:0050661', 'GO:0040007', 'GO:0005618', 'GO:0009570', 'GO:0005634', 'GO:0006520', 'GO:0019877', 'GO:0000166', 'GO:0016740', 'GO:0009097', 'GO:0009090', 'GO:0019252', 'GO:0019761', 'GO:0016301', 'GO:0008152', 'GO:0009088', 'GO:0055114', 'GO:0009507', 'GO:0008652', 'GO:0005829', 'GO:0006555', 'GO:0004412', 'GO:0005575', 'GO:0009089', 'GO:0005524', 'GO:0006164', 'GO:0006531', 'GO:0009086', 'GO:0004072', 'GO:0009082']),
                        'lcl|AE014075.1_gene_4':set(['GO:0005737', 'GO:0006566', 'GO:0000394', 'GO:0016310', 'GO:0009617', 'GO:0004413', 'GO:0000166', 'GO:0019344', 'GO:0009620', 'GO:0009088', 'GO:0009570', 'GO:0009086', 'GO:0005524', 'GO:0009507']),
                        'lcl|AE014075.1_gene_5':set(['GO:0005125', 'GO:0016311', 'GO:0016310', 'GO:0046360', 'GO:0003674', 'GO:0030170', 'GO:0004795', 'GO:0005737', 'GO:0006566', 'GO:0005615', 'GO:0016829', 'GO:0006520', 'GO:0005524', 'GO:0003824', 'GO:0008150', 'GO:0070905', 'GO:0008152', 'GO:0009071', 'GO:0008652', 'GO:0006897', 'GO:0005829', 'GO:0005575', 'GO:0009088', 'GO:0004765', 'GO:0005634'])
                        })
        for k, v in expected.items():
            seq = blast.results[k]
            self.assertEqual(v, seq.all_terms)

#        self.assertEqual(expected, seq.all_terms)
#        dist_method = MatchingDistance()
#        dist_matirx = dist_method.cal_dist(seq)
#        print dist_matirx

#    @unittest.skip("run this later")
    def test_run_blast(self):#, record_index, e_value_cut_off):

#        results = dict()
#        for key in self.record_index:
#            seq = Sequence(self.record_index[key].seq)
##            print len(seq.data)
##            print seq.data
#            seq = go_connector.blast_AmiGO(seq)
#            seq = go_connector.extract_ID(seq)
#            seq = go_connector.parse_go_term(seq, 1e-200)
#
#            print key, seq, seq.all_terms
#            results[key] = seq

        sub_record = dict({'lcl|AE014075.1_gene_4':self.record_index['lcl|AE014075.1_gene_4'],
                           'lcl|AE014075.1_gene_5':self.record_index['lcl|AE014075.1_gene_5']
                           })
        blast = RunBlast(sub_record, 1e-200)
        blast.run()

        expected = dict({'lcl|AE014075.1_gene_4':set([]),
                         'lcl|AE014075.1_gene_5':set(['GO:0004795', 'GO:0030170', 'GO:0009088'])
                         })

        for k, v in expected.items():
            seq = blast.results[k]
#            print seq
#            print seq.acc_ID
#            print seq.match_ID
#            print seq.e_value
#            print seq.each_term
            self.assertEqual(v, seq.all_terms)

#
#        for k, v in results.items():
#            print k, v.all_terms


#
#
#
#
#def setup_database():
#
#    infile = data_dir + "AE014075_subSmall100.fasta"
##    infile = data_dir + "MetaSim_bint-454.20e39f4c.fna"
#    #records = (SeqIO.parse(infile, "fasta"))
#    #records = list(SeqIO.parse(infile, "fasta"))
#    #record_dict = SeqIO.to_dict(SeqIO.parse(infile, "fasta"))
#    record_index = SeqIO.index(infile, "fasta") # use index for large file
#
#    #print record_index["lcl|AE014075.1_gene_1"].format("fasta")
##    data = record_index["lcl|AE014075.1_gene_1"].seq ## short no result
#    ## TODO mismatch
#    ## maybe change from *** NONE *** to 
#    ##  Sorry, your BLAST query returned no results. Please see the raw BLAST data for full details.
##    data = record_index["lcl|AE014075.1_gene_2"].seq ## good
##    data = record_index["lcl|AE014075.1_gene_3"].seq ## long search time, implemented waiting time
#
#    #data = str(data)
#    #data = data+data+data+data+data+data
#
#    ## do more test here later
#    ##Test try...except..raise
#    #try:
#    #    v = float("12.33")
#    #except ValueError as e:
#    #    print 'Exception error is: %s' % e;
#    #    print "c0", sys.exc_info()[0], sys.exc_info()[1]
#    #    raise
#    return record_index
#
#
#
#def main():
#    print __name__
##    time_profile()
#
#    record_index = setup_database()
##    test_single(record_index, e_value_cut_off)
##    run_blast(record_index, e_value_cut_off)
#
