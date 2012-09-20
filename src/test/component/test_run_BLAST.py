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
        self.infile = data_dir + "AE014075_subTiny5.fasta"#"AE014075_subSmall100.fasta"
        self.e_value_cut_off = 1e-15
        self.record_index = SeqIO.index(self.infile, "fasta")


    def tearDown(self):
        pass


    def test_create_blast_from_file(self):
        file_var = "NotExist"
        e_var = 1e-50

        with self.assertRaises(IOError):
            RunBlast.create_blast_from_file(file_var, e_value=e_var)

        blast = RunBlast.create_blast_from_file(self.infile, e_value=e_var)
        self.assertEqual(blast.results, dict())

        for key in self.record_index:
            self.assertEqual(str(self.record_index[key].seq), str(blast.record_index[key].seq))
            self.assertEqual(str(self.record_index[key].id), str(blast.record_index[key].id))

        self.assertEqual(blast.e_value_cut_off, e_var)


    @unittest.skip("Take a while to run")
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


    @unittest.skip("Take a while to run")
    def test_RunBlast_subset(self):

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
            self.assertEqual(v, seq.all_terms)
#
        for k, v in blast.results.items():
            print k, v.all_terms
