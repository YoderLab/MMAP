'''
Created on Dec 7, 2011

@author: Steven Wu
'''
import unittest
from core.parser.go_OBO_parser import OBOParser
import os
from core.utils import path_utils
import pickle


class TestGOOBOParser(unittest.TestCase):
    
    def setUp(self):
        CWD = os.getcwd()
        self.data_dir = path_utils.get_data_dir(CWD)

    def tearDown(self):
        pass

    def test_parse_database(self):
        self.infile = self.data_dir+"test_gene_ontology_ext_1_10.obo" 
        self.pr = OBOParser(self.infile)
        self.pr.parse_database()
        
        self.data = self.pr.dict_is_a
        self.assertEqual(self.pr.version, "1.2")
        self.assertEqual(self.pr.date, "06:12:2011 18:33")

        self.assertSetEqual(self.data["GO:0000001"], {"GO:0048308", "GO:0048311"} )
        self.assertSetEqual(self.data["GO:0000002"], {"GO:0007005"})
        self.assertSetEqual(self.data["GO:0000003"], {"GO:0008150"})
        self.assertSetEqual(self.data["GO:0000005"], set())
        self.assertSetEqual(self.data["GO:0000006"], {"GO:0005385"})
        self.assertSetEqual(self.data["GO:0000007"], {"GO:0005385"})
        self.assertSetEqual(self.data["GO:0000008"], set())
        self.assertSetEqual(self.data["GO:0000009"], {"GO:0000030"})
        self.assertSetEqual(self.data["GO:0000010"], {"GO:0016765"})
        
        


    def test_save_file(self):
        
        self.infile = self.data_dir+"test_gene_ontology_ext_1_10.obo"
        self.save_file = self.data_dir+"testOBO_parser_save.zzz" 
        self.pr = OBOParser(self.infile)
        self.pr.parse_database()
        self.pr.save_dict_to_file(self.save_file)
        
        del self.pr
        self.pr = OBOParser(self.save_file)
        self.data = self.pr.load_dict_file()

        self.assertSetEqual(self.data["GO:0000001"], {"GO:0048308", "GO:0048311"} )
        self.assertSetEqual(self.data["GO:0000002"], {"GO:0007005"})
        self.assertSetEqual(self.data["GO:0000003"], {"GO:0008150"})
        self.assertSetEqual(self.data["GO:0000005"], set())
        self.assertSetEqual(self.data["GO:0000006"], {"GO:0005385"})
        self.assertSetEqual(self.data["GO:0000007"], {"GO:0005385"})
        self.assertSetEqual(self.data["GO:0000008"], set())
        self.assertSetEqual(self.data["GO:0000009"], {"GO:0000030"})
        self.assertSetEqual(self.data["GO:0000010"], {"GO:0016765"})
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_Init']
    unittest.main()