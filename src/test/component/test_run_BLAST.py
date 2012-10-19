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
        self.infile = data_dir + "AE014075_subTiny5.fasta"  #"AE014075_subSmall100.fasta"
        self.e_value_cut_off = 1e-15
        self.record_index = SeqIO.index(self.infile, "fasta")

        self.template_set = dict({
                        'S1':set([]),
                        'S2':set(['GO:01', 'GO:02']),
                        'S3':set(['GO:01', 'GO:03', 'GO:04']),
                        'S4':set(['GO:03', 'GO:04', 'GO:05']),
                        'S5':set(['GO:01', 'GO:05', 'GO:06', 'GO:07']),
                        })
        self.template_set_small = dict({
            'S3':set(['GO:01', 'GO:03', 'GO:04']),
            'S4':set(['GO:03', 'GO:04', 'GO:05']),
            })
        self.S1 = self.template_set.get("S1")
        self.S2 = self.template_set.get("S2")
        self.S3 = self.template_set.get("S3")
        self.S4 = self.template_set.get("S4")
        self.S5 = self.template_set.get("S5")


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
#            
#print(1, k, seq)
#print(2, seq.all_terms)
#print(3, seq.each_term)
#(1, 'lcl|AE014075.1_gene_1', <core.sequence.Sequence object at 0x2ec9ad0>)
#(2, set([]))
#(3, {})
#(1, 'lcl|AE014075.1_gene_3', <core.sequence.Sequence object at 0x25e7bd0>)
#(2, set(['GO:0071470', 'GO:0016310', 'GO:0005886', 'GO:0009067', 'GO:0000023', 'GO:0016597', 'GO:0043085', 'GO:0016491', 'GO:0005737', 'GO:0050661', 'GO:0040007', 'GO:0005618', 'GO:0009570', 'GO:0005634', 'GO:0006520', 'GO:0019877', 'GO:0000166', 'GO:0016740', 'GO:0009097', 'GO:0009090', 'GO:0019252', 'GO:0019761', 'GO:0016301', 'GO:0008152', 'GO:0009088', 'GO:0055114', 'GO:0009507', 'GO:0008652', 'GO:0005829', 'GO:0006555', 'GO:0004412', 'GO:0005575', 'GO:0009089', 'GO:0005524', 'GO:0006164', 'GO:0006531', 'GO:0009086', 'GO:0004072', 'GO:0009082']))
#(3, {'UniProtKB:P0A4Z8': set(['GO:0040007', 'GO:0005618', 'GO:0019877', 'GO:0009089', 'GO:0005886', 'GO:0004072']), 'TIGR_CMR:BA_3936': set(['GO:0009089', 'GO:0004072']), 'TAIR:locus:2133995': set(['GO:0016491', 'GO:0008652', 'GO:0050661', 'GO:0009570', 'GO:0006520', 'GO:0004412', 'GO:0009067', 'GO:0008152', 'GO:0006164', 'GO:0000166', 'GO:0016597', 'GO:0004072', 'GO:0055114', 'GO:0009507']), 'ECOCYC:EG10998': set(['GO:0050661', 'GO:0016310', 'GO:0000166', 'GO:0009090', 'GO:0009089', 'GO:0005524', 'GO:0004412', 'GO:0016597', 'GO:0004072', 'GO:0055114', 'GO:0009088']), 'TIGR_CMR:BA_1811': set(['GO:0009089', 'GO:0004072']), 'CGD:CAL0002880': set(['GO:0005829', 'GO:0009086', 'GO:0004072', 'GO:0009090', 'GO:0009088']), 'TIGR_CMR:CPS_0456': set(['GO:0009086', 'GO:0004072', 'GO:0004412']), 'CGD:CAL0006049': set(['GO:0005737', 'GO:0005634', 'GO:0004412', 'GO:0009088', 'GO:0009086', 'GO:0009090']), 'TIGR_CMR:CHY_1909': set(['GO:0009089', 'GO:0004072']), 'UniProtKB:Q9KUH4': set(['GO:0009086', 'GO:0009089', 'GO:0004072', 'GO:0009088']), 'ECOCYC:EG10550': set(['GO:0016310', 'GO:0000166', 'GO:0009089', 'GO:0009090', 'GO:0016597', 'GO:0004072', 'GO:0005524']), 'TIGR_CMR:VC_2684': set(['GO:0009086', 'GO:0004072', 'GO:0004412']), 'TIGR_CMR:CJE_0685': set(['GO:0009089', 'GO:0004072']), 'TIGR_CMR:CBU_1051': set(['GO:0009089', 'GO:0004072']), 'ASPGD:ASPL0000040676': set(['GO:0005737', 'GO:0006520', 'GO:0005634', 'GO:0071470', 'GO:0004412', 'GO:0009088', 'GO:0009086', 'GO:0009090']), 'TIGR_CMR:SO_4055': set(['GO:0009088', 'GO:0009086', 'GO:0009089', 'GO:0004072', 'GO:0004412']), 'TIGR_CMR:SO_3427': set(['GO:0009086', 'GO:0009089', 'GO:0004072', 'GO:0009088']), 'TIGR_CMR:CHY_1155': set(['GO:0009089', 'GO:0004072']), 'TIGR_CMR:ECH_1001': set(['GO:0009089', 'GO:0004072']), 'TIGR_CMR:DET_1633': set(['GO:0009089', 'GO:0004072']), 'TAIR:locus:2078638': set(['GO:0008652', 'GO:0009067', 'GO:0008152', 'GO:0016597', 'GO:0004072', 'GO:0009507']), 'TAIR:locus:2183896': set(['GO:0008652', 'GO:0009570', 'GO:0008152', 'GO:0016597', 'GO:0004072', 'GO:0009507']), 'POMBASE:SPBC776.03': set(['GO:0004412', 'GO:0005575', 'GO:0009090', 'GO:0009088', 'GO:0009086', 'GO:0055114']), 'SGD:S000003900': set(['GO:0005737', 'GO:0008652', 'GO:0050661', 'GO:0000166', 'GO:0005634', 'GO:0006520', 'GO:0055114', 'GO:0004412', 'GO:0016491', 'GO:0009088', 'GO:0009097', 'GO:0009086', 'GO:0009090', 'GO:0009082']), 'ECOCYC:EG10590': set(['GO:0050661', 'GO:0016310', 'GO:0004412', 'GO:0000166', 'GO:0009090', 'GO:0009089', 'GO:0005524', 'GO:0009086', 'GO:0004072', 'GO:0055114']), 'UniProtKB:Q9KPK3': set(['GO:0009088', 'GO:0004072', 'GO:0004412']), 'TIGR_CMR:VC_0391': set(['GO:0009089', 'GO:0004072']), 'TIGR_CMR:VC_0547': set(['GO:0009086', 'GO:0009089', 'GO:0004072', 'GO:0009088']), 'TIGR_CMR:SPO_3035': set(['GO:0009089', 'GO:0004072']), 'TIGR_CMR:SO_3986': set(['GO:0009089', 'GO:0004072']), 'TIGR_CMR:CPS_4291': set(['GO:0009088', 'GO:0004072', 'GO:0004412']), 'UniProtKB:Q9KNP7': set(['GO:0009086', 'GO:0004072', 'GO:0004412']), 'TIGR_CMR:GSU_1799': set(['GO:0009089', 'GO:0004072']), 'UniProtKB:G4NCU5': set(['GO:0005575']), 'SGD:S000000854': set(['GO:0005737', 'GO:0008652', 'GO:0016310', 'GO:0016301', 'GO:0000166', 'GO:0016740', 'GO:0009090', 'GO:0009089', 'GO:0009088', 'GO:0009086', 'GO:0004072', 'GO:0005524']), 'TIGR_CMR:SO_3415': set(['GO:0009088', 'GO:0009086', 'GO:0009089', 'GO:0004072', 'GO:0004412']), 'POMBASE:SPBC19F5.04': set(['GO:0006531', 'GO:0005829', 'GO:0006555', 'GO:0009088', 'GO:0004072']), 'TAIR:locus:2029564': set(['GO:0016491', 'GO:0008652', 'GO:0050661', 'GO:0000023', 'GO:0019252', 'GO:0009570', 'GO:0006520', 'GO:0004412', 'GO:0019761', 'GO:0009067', 'GO:0043085', 'GO:0008152', 'GO:0000166', 'GO:0016597', 'GO:0004072', 'GO:0055114', 'GO:0009507']), 'TAIR:locus:2174708': set(['GO:0008652', 'GO:0009570', 'GO:0009067', 'GO:0008152', 'GO:0016597', 'GO:0004072', 'GO:0009507']), 'UniProtKB:Q9KUW8': set(['GO:0009089', 'GO:0004072']), 'TIGR_CMR:VC_2364': set(['GO:0009088', 'GO:0004072', 'GO:0004412']), 'TIGR_CMR:CPS_2004': set(['GO:0009089', 'GO:0004072']), 'ASPGD:ASPL0000077145': set(['GO:0005829', 'GO:0006520', 'GO:0009088', 'GO:0009086', 'GO:0004072', 'GO:0009090'])})
#(1, 'lcl|AE014075.1_gene_2', <core.sequence.Sequence object at 0x2ec9e50>)
#(2, set(['GO:0004803', 'GO:0006313']))
#(3, {'TIGR_CMR:VC_A0202': set(['GO:0004803', 'GO:0006313']), 'TIGR_CMR:VC_0870': set(['GO:0004803', 'GO:0006313']), 'TIGR_CMR:VC_A0493': set(['GO:0004803', 'GO:0006313']), 'TIGR_CMR:VC_A0275': set(['GO:0004803', 'GO:0006313']), 'TIGR_CMR:CPS_1800': set(['GO:0004803', 'GO:0006313']), 'UniProtKB:Q7DCS6': set(['GO:0004803', 'GO:0006313']), 'UniProtKB:Q9KM89': set(['GO:0004803', 'GO:0006313'])})
#(1, 'lcl|AE014075.1_gene_5', <core.sequence.Sequence object at 0x2ec9f10>)
#(2, set(['GO:0005125', 'GO:0016311', 'GO:0046360', 'GO:0003674', 'GO:0030170', 'GO:0000287', 'GO:0004795', 'GO:0005737', 'GO:0006566', 'GO:0005615', 'GO:0005634', 'GO:0006520', 'GO:0005524', 'GO:0003824', 'GO:0008150', 'GO:0070905', 'GO:0008152', 'GO:0009071', 'GO:0009073', 'GO:0008652', 'GO:0006897', 'GO:0005829', 'GO:0005575', 'GO:0009088', 'GO:0004765', 'GO:0016829']))
#(3, {'TIGR_CMR:CJE_0903': set(['GO:0004795', 'GO:0009088']), 'UniProtKB:Q5ZIX9': set(['GO:0009088', 'GO:0004795', 'GO:0005524', 'GO:0004765', 'GO:0030170']), 'POMBASE:SPAC9E9.06c': set(['GO:0005737', 'GO:0005634', 'GO:0004795', 'GO:0005829', 'GO:0009088']), 'UniProtKB:E2RIU8': set(['GO:0016311', 'GO:0046360', 'GO:0030170', 'GO:0009088', 'GO:0004795', 'GO:0009071', 'GO:0070905']), 'UniProtKB:Q86YJ6': set(['GO:0005125', 'GO:0005615', 'GO:0016311', 'GO:0046360', 'GO:0070905', 'GO:0005575', 'GO:0008150', 'GO:0009088', 'GO:0003674', 'GO:0004795', 'GO:0009071', 'GO:0030170']), 'TIGR_CMR:CPS_4289': set(['GO:0004795', 'GO:0009088']), 'CGD:CAL0000179': set(['GO:0006566', 'GO:0005634', 'GO:0004795', 'GO:0006897', 'GO:0005829']), 'UniProtKB:E2RR17': set(['GO:0005737', 'GO:0000287', 'GO:0030170', 'GO:0004765', 'GO:0009088', 'GO:0004795', 'GO:0005524', 'GO:0009073']), 'UniProtKB:G4MVN8': set(['GO:0005575']), 'UniProtKB:E1C5M5': set(['GO:0005737', 'GO:0000287', 'GO:0030170', 'GO:0004765', 'GO:0009088', 'GO:0004795', 'GO:0005524', 'GO:0009073']), 'TIGR_CMR:SPO_3071': set(['GO:0004795', 'GO:0009088']), 'UniProtKB:F1RVJ6': set(['GO:0005737', 'GO:0000287', 'GO:0030170', 'GO:0004765', 'GO:0009088', 'GO:0004795', 'GO:0005524', 'GO:0009073']), 'ECOCYC:EG11000': set(['GO:0004795', 'GO:0030170', 'GO:0009088']), 'UniProtKB:F1MBE1': set(['GO:0005737', 'GO:0030170', 'GO:0000287', 'GO:0009088', 'GO:0004765', 'GO:0004795', 'GO:0005524', 'GO:0009073']), 'UniProtKB:E1B913': set(['GO:0016311', 'GO:0046360', 'GO:0070905', 'GO:0009088', 'GO:0004795', 'GO:0009071', 'GO:0030170']), 'UniProtKB:C9JU10': set(['GO:0003824', 'GO:0030170']), 'MGI:MGI:3041254': set(['GO:0016311', 'GO:0016829', 'GO:0046360', 'GO:0070905', 'GO:0005575', 'GO:0030170', 'GO:0008152', 'GO:0004795', 'GO:0009071', 'GO:0009088']), 'UniProtKB:E9PTK4': set(['GO:0005737', 'GO:0030170', 'GO:0000287', 'GO:0009088', 'GO:0004765', 'GO:0004795', 'GO:0005524', 'GO:0009073']), 'ASPGD:ASPL0000040181': set(['GO:0006566', 'GO:0006897', 'GO:0005634', 'GO:0006520', 'GO:0004795', 'GO:0005829']), 'ZFIN:ZDB-GENE-051127-19': set(['GO:0005575', 'GO:0016829', 'GO:0004795', 'GO:0009088']), 'RGD:1309144': set(['GO:0016311', 'GO:0046360', 'GO:0070905', 'GO:0005575', 'GO:0008150', 'GO:0009088', 'GO:0003674', 'GO:0004795', 'GO:0009071', 'GO:0030170']), 'UniProtKB:Q8IYQ7': set(['GO:0005575', 'GO:0008150', 'GO:0009088', 'GO:0004765', 'GO:0003674', 'GO:0004795', 'GO:0005524', 'GO:0030170']), 'RGD:1564213': set(['GO:0005575', 'GO:0008150', 'GO:0003674']), 'UniProtKB:Q9KPK5': set(['GO:0004795', 'GO:0009088']), 'SGD:S000000649': set(['GO:0005737', 'GO:0008652', 'GO:0006897', 'GO:0006566', 'GO:0005634', 'GO:0006520', 'GO:0003824', 'GO:0009088', 'GO:0008152', 'GO:0004795', 'GO:0016829', 'GO:0030170']), 'UniProtKB:F1P5Q3': set(['GO:0016311', 'GO:0046360', 'GO:0030170', 'GO:0009088', 'GO:0004795', 'GO:0009071', 'GO:0070905']), 'UniProtKB:F1SVD9': set(['GO:0003824', 'GO:0030170']), 'UniProtKB:F1P9D1': set(['GO:0003824', 'GO:0030170']), 'MGI:MGI:2139347': set(['GO:0005575', 'GO:0003674', 'GO:0009088', 'GO:0004765', 'GO:0008150', 'GO:0004795', 'GO:0005524']), 'TIGR_CMR:SO_3413': set(['GO:0004795', 'GO:0009088']), 'TIGR_CMR:GSU_1695': set(['GO:0004795', 'GO:0009088']), 'TIGR_CMR:VC_2362': set(['GO:0004795', 'GO:0009088'])})


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




    def test_RunBlast_set_membership(self):
        # http://docs.python.org/library/stdtypes.html#set
        self.assertTrue("GO:01" in self.S2)
        self.assertTrue("GO:03" not in self.S2)

        #TODO: change the following None to sefl.S*
        self.assertTrue("GO:04" in self.S3)
        self.assertTrue("GO:05" in self.S4)
        self.assertTrue("GO:06" not in self.S1)
        self.assertTrue("GO:07" not in self.S2)

        self.assertFalse("GO:03" in self.S5)
        self.assertFalse("GO:04" in self.S2)
        self.assertFalse("GO:05" not in self.S4)
        self.assertFalse("GO:06" not in self.S5)

    def test_RunBlast_set_union(self): # A OR B (A|B)
        """
        union(other, ...)
        set | other | ...
        Return a new set with elements from the set and all others.
        """
        expected = set(["GO:01", "GO:02", "GO:05", "GO:06", "GO:07"])
        new_set = self.S2 | self.S5
        self.assertEqual(expected, new_set)

        expected = set(["GO:01", "GO:03", "GO:04", "GO:05", "GO:06", "GO:07"]) #TODO
        new_set = self.S4 | self.S5
        self.assertEqual(expected, new_set)

        expected = set(["GO:01", "GO:02", "GO:03", "GO:04", "GO:05", "GO:06", "GO:07"]) #TODO
        new_set = self.S2 | self.S4 | self.S5
        self.assertEqual(expected, new_set)

        expected = set(["GO:01", "GO:02", "GO:03", "GO:04"])
        new_set = self.S2 | self.S3
        self.assertEqual(expected, new_set)

        expected = set(["GO:01", "GO:02", "GO:03", "GO:04", "GO:05"])
        new_set = self.S2 | self.S4
        self.assertEqual(expected, new_set)

        expected = set(["GO:01", "GO:03", "GO:04", "GO:05"])
        new_set = self.S3 | self.S4
        self.assertEqual(expected, new_set)



    def test_RunBlast_set_intersection(self): # A AND B (A&B)
        """
        intersection(other, ...)
        set & other & ...
        Return a new set with elements common to the set and all others.
        """
        expected = set(["GO:05"]) #TODO GO:05
        new_set = self.S4 & self.S5
        self.assertEqual(expected, new_set)


        expected = set([]) #TODO
        new_set = self.S2 & self.S4 & self.S5
        self.assertEqual(expected, new_set)

        expected = set(["GO:04", "GO:03"])
        new_set = self.S3 & self.S4
        self.assertEqual(expected, new_set)

        expected = set(["GO:05"])
        new_set = self.S4 & self.S5
        self.assertEqual(expected, new_set)

        expected = set(["GO:03"])
        new_set = self.S3 & self.S4
        self.assertNotEqual(expected, new_set)


    def test_RunBlast_set_difference(self):
        """
        difference(other, ...)
        set - other - ...
        Return a new set with elements in the set that are not in the others.
        """
        expected = set(["GO:03", "GO:04"]) #TODO GO:03, GO:04
        new_set = self.S4 - self.S5
        self.assertEqual(expected, new_set)

        expected = set(["GO:01", "GO:06", "GO:07"])
        new_set = self.S5 - self.S4
        self.assertEqual(expected, new_set)


        expected = set(["GO:02"]) #TODO
        new_set = self.S2 - self.S3
        self.assertEqual(expected, new_set)

        expected = set(["GO:01"])
        new_set = self.S3 - self.S4
        self.assertEqual(expected, new_set)

        expected = set(["GO:05"])
        new_set = self.S4 - self.S3
        self.assertEqual(expected, new_set)


    def test_RunBlast_set_symmetric_difference(self):
        """
        symmetric_difference(other)
        set ^ other
        Return a new set with elements in either the set or other but not both.
        """
        expected = set(["GO:03", "GO:04", "GO:01", "GO:06", "GO:07"]) #TODO GO01, GO03 GO04 GO06 GO07
        new_set = self.S4 ^ self.S5
        self.assertEqual(expected, new_set)

        expected = set(["GO:05", "GO:01"]) #TODO
        new_set = self.S3 ^ self.S4
        self.assertEqual(expected, new_set)

        expected = set(["GO:02", "GO:03", "GO:04"])
        new_set = self.S3 ^ self.S2
        self.assertEqual(expected, new_set)

        expected = set(["GO:03", "GO:04", "GO:05", "GO:06", "GO:07"])
        new_set = self.S3 ^ self.S5
        self.assertEqual(expected, new_set)

    def test_RunBlast_set_count(self):

        expected = dict({"GO:01":1,
                         "GO:03":2,
                         "GO:04":2,
                         "GO:05":1, })


#        union = self.S3 | self.S4
        print(self.template_set_small)
        new_dict = self.init_dict(self.template_set_small, 0)


        print(new_dict)
#        new_dict=self.update_counter_from_set(new_dict, self.S3)
#        new_dict=self.update_counter_from_set(new_dict, self.S4)

        self.update_counter_from_dictionaries(new_dict, self.template_set_small)
        print(new_dict)
        self.assertEqual(expected, new_dict)

        expected = dict({"GO:01":3,
                         "GO:02":1,
                         "GO:03":2,
                         "GO:04":2,
                         "GO:05":2,
                         "GO:06":1,
                         "GO:07":1 })

        new_dict = self.init_dict(self.template_set, 0)
        self.update_counter_from_dictionaries(new_dict, self.template_set)

        print(new_dict)
        self.assertEqual(expected, new_dict)

    def test_init_dict(self): # allterms, default_value=0)
        expected = dict({"GO:01":0,
                         "GO:02":0,
                         "GO:03":0,
                         "GO:04":0,
                         "GO:05":0,
                         "GO:06":0,
                         "GO:07":0 })

        new_dict = RunBlast(records, e_value, outfile)
        new_dict.init_dict(self, self.template_set, 0)
        self.assertEqual(expected, new_dict)

    def init_dict_old(self, union, default_value=0):
        new_dict = dict()
        for k in union:
        #            new_dict.setdefault(k, default_value)
            new_dict[k]=default_value
        return new_dict

    def update_counter_from_dictionaries(self, counter, allterms):
#        print allterms
#        print(allterms.values())
        for v in allterms.values():
            counter = self.update_counter_from_set(counter,v)

    def update_counter_from_set(self, counter, each_set):
        for k in each_set:
            counter[k]= counter[k]+1
        return counter

#    def test_RunBlast_generateOutputMatrix(self):
#
#        blast = RunBlast(self.record_index, self.e_value_cut_off)
#        expected_all_terms = dict({'lcl|AE014075.1_gene_1':set([]),
#                        'lcl|AE014075.1_gene_2':set(['GO:0004803', 'GO:0006313']),
#                        'lcl|AE014075.1_gene_3':set(['GO:0071470', 'GO:0016310', 'GO:0005886', 'GO:0009067', 'GO:0000023', 'GO:0016597', 'GO:0043085', 'GO:0016491', 'GO:0005737', 'GO:0050661', 'GO:0040007', 'GO:0005618', 'GO:0009570', 'GO:0005634', 'GO:0006520', 'GO:0019877', 'GO:0000166', 'GO:0016740', 'GO:0009097', 'GO:0009090', 'GO:0019252', 'GO:0019761', 'GO:0016301', 'GO:0008152', 'GO:0009088', 'GO:0055114', 'GO:0009507', 'GO:0008652', 'GO:0005829', 'GO:0006555', 'GO:0004412', 'GO:0005575', 'GO:0009089', 'GO:0005524', 'GO:0006164', 'GO:0006531', 'GO:0009086', 'GO:0004072', 'GO:0009082']),
#                        'lcl|AE014075.1_gene_4':set(['GO:0005737', 'GO:0006566', 'GO:0000394', 'GO:0016310', 'GO:0009617', 'GO:0004413', 'GO:0000166', 'GO:0019344', 'GO:0009620', 'GO:0009088', 'GO:0009570', 'GO:0009086', 'GO:0005524', 'GO:0009507']),
#                        'lcl|AE014075.1_gene_5':set(['GO:0005125', 'GO:0016311', 'GO:0016310', 'GO:0046360', 'GO:0003674', 'GO:0030170', 'GO:0004795', 'GO:0005737', 'GO:0006566', 'GO:0005615', 'GO:0016829', 'GO:0006520', 'GO:0005524', 'GO:0003824', 'GO:0008150', 'GO:0070905', 'GO:0008152', 'GO:0009071', 'GO:0008652', 'GO:0006897', 'GO:0005829', 'GO:0005575', 'GO:0009088', 'GO:0004765', 'GO:0005634'])
#                        })
#
##(1, 'lcl|AE014075.1_gene_1', <core.sequence.Sequence object at 0x2ec9ad0>)
##(3, {})
##
##(1, 'lcl|AE014075.1_gene_3', <core.sequence.Sequence object at 0x25e7bd0>)
##(3, {'UniProtKB:P0A4Z8': set(['GO:0040007', 'GO:0005618', 'GO:0019877', 'GO:0009089', 'GO:0005886', 'GO:0004072']), 'TIGR_CMR:BA_3936': set(['GO:0009089', 'GO:0004072']), 'TAIR:locus:2133995': set(['GO:0016491', 'GO:0008652', 'GO:0050661', 'GO:0009570', 'GO:0006520', 'GO:0004412', 'GO:0009067', 'GO:0008152', 'GO:0006164', 'GO:0000166', 'GO:0016597', 'GO:0004072', 'GO:0055114', 'GO:0009507']), 'ECOCYC:EG10998': set(['GO:0050661', 'GO:0016310', 'GO:0000166', 'GO:0009090', 'GO:0009089', 'GO:0005524', 'GO:0004412', 'GO:0016597', 'GO:0004072', 'GO:0055114', 'GO:0009088']), 'TIGR_CMR:BA_1811': set(['GO:0009089', 'GO:0004072']), 'CGD:CAL0002880': set(['GO:0005829', 'GO:0009086', 'GO:0004072', 'GO:0009090', 'GO:0009088']), 'TIGR_CMR:CPS_0456': set(['GO:0009086', 'GO:0004072', 'GO:0004412']), 'CGD:CAL0006049': set(['GO:0005737', 'GO:0005634', 'GO:0004412', 'GO:0009088', 'GO:0009086', 'GO:0009090']), 'TIGR_CMR:CHY_1909': set(['GO:0009089', 'GO:0004072']), 'UniProtKB:Q9KUH4': set(['GO:0009086', 'GO:0009089', 'GO:0004072', 'GO:0009088']), 'ECOCYC:EG10550': set(['GO:0016310', 'GO:0000166', 'GO:0009089', 'GO:0009090', 'GO:0016597', 'GO:0004072', 'GO:0005524']), 'TIGR_CMR:VC_2684': set(['GO:0009086', 'GO:0004072', 'GO:0004412']), 'TIGR_CMR:CJE_0685': set(['GO:0009089', 'GO:0004072']), 'TIGR_CMR:CBU_1051': set(['GO:0009089', 'GO:0004072']), 'ASPGD:ASPL0000040676': set(['GO:0005737', 'GO:0006520', 'GO:0005634', 'GO:0071470', 'GO:0004412', 'GO:0009088', 'GO:0009086', 'GO:0009090']), 'TIGR_CMR:SO_4055': set(['GO:0009088', 'GO:0009086', 'GO:0009089', 'GO:0004072', 'GO:0004412']), 'TIGR_CMR:SO_3427': set(['GO:0009086', 'GO:0009089', 'GO:0004072', 'GO:0009088']), 'TIGR_CMR:CHY_1155': set(['GO:0009089', 'GO:0004072']), 'TIGR_CMR:ECH_1001': set(['GO:0009089', 'GO:0004072']), 'TIGR_CMR:DET_1633': set(['GO:0009089', 'GO:0004072']), 'TAIR:locus:2078638': set(['GO:0008652', 'GO:0009067', 'GO:0008152', 'GO:0016597', 'GO:0004072', 'GO:0009507']), 'TAIR:locus:2183896': set(['GO:0008652', 'GO:0009570', 'GO:0008152', 'GO:0016597', 'GO:0004072', 'GO:0009507']), 'POMBASE:SPBC776.03': set(['GO:0004412', 'GO:0005575', 'GO:0009090', 'GO:0009088', 'GO:0009086', 'GO:0055114']), 'SGD:S000003900': set(['GO:0005737', 'GO:0008652', 'GO:0050661', 'GO:0000166', 'GO:0005634', 'GO:0006520', 'GO:0055114', 'GO:0004412', 'GO:0016491', 'GO:0009088', 'GO:0009097', 'GO:0009086', 'GO:0009090', 'GO:0009082']), 'ECOCYC:EG10590': set(['GO:0050661', 'GO:0016310', 'GO:0004412', 'GO:0000166', 'GO:0009090', 'GO:0009089', 'GO:0005524', 'GO:0009086', 'GO:0004072', 'GO:0055114']), 'UniProtKB:Q9KPK3': set(['GO:0009088', 'GO:0004072', 'GO:0004412']), 'TIGR_CMR:VC_0391': set(['GO:0009089', 'GO:0004072']), 'TIGR_CMR:VC_0547': set(['GO:0009086', 'GO:0009089', 'GO:0004072', 'GO:0009088']), 'TIGR_CMR:SPO_3035': set(['GO:0009089', 'GO:0004072']), 'TIGR_CMR:SO_3986': set(['GO:0009089', 'GO:0004072']), 'TIGR_CMR:CPS_4291': set(['GO:0009088', 'GO:0004072', 'GO:0004412']), 'UniProtKB:Q9KNP7': set(['GO:0009086', 'GO:0004072', 'GO:0004412']), 'TIGR_CMR:GSU_1799': set(['GO:0009089', 'GO:0004072']), 'UniProtKB:G4NCU5': set(['GO:0005575']), 'SGD:S000000854': set(['GO:0005737', 'GO:0008652', 'GO:0016310', 'GO:0016301', 'GO:0000166', 'GO:0016740', 'GO:0009090', 'GO:0009089', 'GO:0009088', 'GO:0009086', 'GO:0004072', 'GO:0005524']), 'TIGR_CMR:SO_3415': set(['GO:0009088', 'GO:0009086', 'GO:0009089', 'GO:0004072', 'GO:0004412']), 'POMBASE:SPBC19F5.04': set(['GO:0006531', 'GO:0005829', 'GO:0006555', 'GO:0009088', 'GO:0004072']), 'TAIR:locus:2029564': set(['GO:0016491', 'GO:0008652', 'GO:0050661', 'GO:0000023', 'GO:0019252', 'GO:0009570', 'GO:0006520', 'GO:0004412', 'GO:0019761', 'GO:0009067', 'GO:0043085', 'GO:0008152', 'GO:0000166', 'GO:0016597', 'GO:0004072', 'GO:0055114', 'GO:0009507']), 'TAIR:locus:2174708': set(['GO:0008652', 'GO:0009570', 'GO:0009067', 'GO:0008152', 'GO:0016597', 'GO:0004072', 'GO:0009507']), 'UniProtKB:Q9KUW8': set(['GO:0009089', 'GO:0004072']), 'TIGR_CMR:VC_2364': set(['GO:0009088', 'GO:0004072', 'GO:0004412']), 'TIGR_CMR:CPS_2004': set(['GO:0009089', 'GO:0004072']), 'ASPGD:ASPL0000077145': set(['GO:0005829', 'GO:0006520', 'GO:0009088', 'GO:0009086', 'GO:0004072', 'GO:0009090'])})
##
##(1, 'lcl|AE014075.1_gene_2', <core.sequence.Sequence object at 0x2ec9e50>)
##(3, {'TIGR_CMR:VC_A0202': set(['GO:0004803', 'GO:0006313']), 'TIGR_CMR:VC_0870': set(['GO:0004803', 'GO:0006313']), 'TIGR_CMR:VC_A0493': set(['GO:0004803', 'GO:0006313']), 'TIGR_CMR:VC_A0275': set(['GO:0004803', 'GO:0006313']), 'TIGR_CMR:CPS_1800': set(['GO:0004803', 'GO:0006313']), 'UniProtKB:Q7DCS6': set(['GO:0004803', 'GO:0006313']), 'UniProtKB:Q9KM89': set(['GO:0004803', 'GO:0006313'])})
##
##(1, 'lcl|AE014075.1_gene_5', <core.sequence.Sequence object at 0x2ec9f10>)
##(3, {'TIGR_CMR:CJE_0903': set(['GO:0004795', 'GO:0009088']), 'UniProtKB:Q5ZIX9': set(['GO:0009088', 'GO:0004795', 'GO:0005524', 'GO:0004765', 'GO:0030170']), 'POMBASE:SPAC9E9.06c': set(['GO:0005737', 'GO:0005634', 'GO:0004795', 'GO:0005829', 'GO:0009088']), 'UniProtKB:E2RIU8': set(['GO:0016311', 'GO:0046360', 'GO:0030170', 'GO:0009088', 'GO:0004795', 'GO:0009071', 'GO:0070905']), 'UniProtKB:Q86YJ6': set(['GO:0005125', 'GO:0005615', 'GO:0016311', 'GO:0046360', 'GO:0070905', 'GO:0005575', 'GO:0008150', 'GO:0009088', 'GO:0003674', 'GO:0004795', 'GO:0009071', 'GO:0030170']), 'TIGR_CMR:CPS_4289': set(['GO:0004795', 'GO:0009088']), 'CGD:CAL0000179': set(['GO:0006566', 'GO:0005634', 'GO:0004795', 'GO:0006897', 'GO:0005829']), 'UniProtKB:E2RR17': set(['GO:0005737', 'GO:0000287', 'GO:0030170', 'GO:0004765', 'GO:0009088', 'GO:0004795', 'GO:0005524', 'GO:0009073']), 'UniProtKB:G4MVN8': set(['GO:0005575']), 'UniProtKB:E1C5M5': set(['GO:0005737', 'GO:0000287', 'GO:0030170', 'GO:0004765', 'GO:0009088', 'GO:0004795', 'GO:0005524', 'GO:0009073']), 'TIGR_CMR:SPO_3071': set(['GO:0004795', 'GO:0009088']), 'UniProtKB:F1RVJ6': set(['GO:0005737', 'GO:0000287', 'GO:0030170', 'GO:0004765', 'GO:0009088', 'GO:0004795', 'GO:0005524', 'GO:0009073']), 'ECOCYC:EG11000': set(['GO:0004795', 'GO:0030170', 'GO:0009088']), 'UniProtKB:F1MBE1': set(['GO:0005737', 'GO:0030170', 'GO:0000287', 'GO:0009088', 'GO:0004765', 'GO:0004795', 'GO:0005524', 'GO:0009073']), 'UniProtKB:E1B913': set(['GO:0016311', 'GO:0046360', 'GO:0070905', 'GO:0009088', 'GO:0004795', 'GO:0009071', 'GO:0030170']), 'UniProtKB:C9JU10': set(['GO:0003824', 'GO:0030170']), 'MGI:MGI:3041254': set(['GO:0016311', 'GO:0016829', 'GO:0046360', 'GO:0070905', 'GO:0005575', 'GO:0030170', 'GO:0008152', 'GO:0004795', 'GO:0009071', 'GO:0009088']), 'UniProtKB:E9PTK4': set(['GO:0005737', 'GO:0030170', 'GO:0000287', 'GO:0009088', 'GO:0004765', 'GO:0004795', 'GO:0005524', 'GO:0009073']), 'ASPGD:ASPL0000040181': set(['GO:0006566', 'GO:0006897', 'GO:0005634', 'GO:0006520', 'GO:0004795', 'GO:0005829']), 'ZFIN:ZDB-GENE-051127-19': set(['GO:0005575', 'GO:0016829', 'GO:0004795', 'GO:0009088']), 'RGD:1309144': set(['GO:0016311', 'GO:0046360', 'GO:0070905', 'GO:0005575', 'GO:0008150', 'GO:0009088', 'GO:0003674', 'GO:0004795', 'GO:0009071', 'GO:0030170']), 'UniProtKB:Q8IYQ7': set(['GO:0005575', 'GO:0008150', 'GO:0009088', 'GO:0004765', 'GO:0003674', 'GO:0004795', 'GO:0005524', 'GO:0030170']), 'RGD:1564213': set(['GO:0005575', 'GO:0008150', 'GO:0003674']), 'UniProtKB:Q9KPK5': set(['GO:0004795', 'GO:0009088']), 'SGD:S000000649': set(['GO:0005737', 'GO:0008652', 'GO:0006897', 'GO:0006566', 'GO:0005634', 'GO:0006520', 'GO:0003824', 'GO:0009088', 'GO:0008152', 'GO:0004795', 'GO:0016829', 'GO:0030170']), 'UniProtKB:F1P5Q3': set(['GO:0016311', 'GO:0046360', 'GO:0030170', 'GO:0009088', 'GO:0004795', 'GO:0009071', 'GO:0070905']), 'UniProtKB:F1SVD9': set(['GO:0003824', 'GO:0030170']), 'UniProtKB:F1P9D1': set(['GO:0003824', 'GO:0030170']), 'MGI:MGI:2139347': set(['GO:0005575', 'GO:0003674', 'GO:0009088', 'GO:0004765', 'GO:0008150', 'GO:0004795', 'GO:0005524']), 'TIGR_CMR:SO_3413': set(['GO:0004795', 'GO:0009088']), 'TIGR_CMR:GSU_1695': set(['GO:0004795', 'GO:0009088']), 'TIGR_CMR:VC_2362': set(['GO:0004795', 'GO:0009088'])})
#
#        for k, v in expected_all_terms.items():
#            blast.results[k] = Sequence(k)
#            blast.results[k].all_terms = v
#        print "aoeu", blast.results
