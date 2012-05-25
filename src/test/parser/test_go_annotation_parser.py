'''
Created on Dec 8, 2011

@author: Steven Wu
'''
from core.parser.go_annotation_parser import AnnotationParser
from core.utils import path_utils
import os
import unittest


class TestGoAnnotationParser(unittest.TestCase):

    def setUp(self):
        CWD = os.getcwd()
        self.data_dir = path_utils.get_data_dir(CWD)

    def tearDown(self):
        pass

    def test_GoAnnotationParser_parse_database(self):
        data_file = self.data_dir + "test_gene_association.GeneDB_Lmajor"
        self.ap = AnnotationParser(data_file)
        self.ap.parse_database()
        self.data = self.ap.annotation

        self.assertEqual(self.ap.cvs_version, "1.45")
        self.assertEqual(self.ap.goc_validation_date, "08/12/2011")

        self.assertEqual(self.data["GO:0003677"], {"LmjF20.0010"})
        self.assertEqual(self.data["GO:0003682"], {"LmjF20.0050"})
        self.assertEqual(self.data["GO:0003779"], {"LmjF05.0285"})
        self.assertEqual(self.data["GO:0004618"], {"LmjF20.0100", "LmjF20.0110"})
        self.assertEqual(self.data["GO:0005198"], {"LmjF10.1000", "LmjF18.0920", "LmjF18.0920"})
        self.assertEqual(self.data["GO:0005634"], {"LmjF20.0050"})
        self.assertEqual(self.data["GO:0005666"], {"LmjF20.0010"})
        self.assertEqual(self.data["GO:0005885"], {"LmjF05.0285", "LmjF10.1000", "LmjF18.0920", "LmjF18.0920"})
        self.assertEqual(self.data["GO:0006096"], {"LmjF20.0100", "LmjF20.0110"})
        self.assertEqual(self.data["GO:0006383"], {"LmjF20.0010"})
        self.assertEqual(self.data["GO:0007010"], {"LmjF05.0285"})
        self.assertEqual(self.data["GO:0008612"], {"LmjF20.0250"})
        self.assertEqual(self.data["GO:0015114"], {"LmjF10.0030", "LmjF10.1300"})
        self.assertEqual(self.data["GO:0016021"], {"LmjF10.0030", "LmjF10.1300"})
        self.assertEqual(self.data["GO:0020015"], {"LmjF20.0100", "LmjF20.0110"})
        self.assertEqual(self.data["GO:0030036"], {"LmjF18.0920", "LmjF18.0920"})

    def test_GoAnnotationParser_get_annotation_count(self):
        data_file = self.data_dir + "test_gene_association.GeneDB_Lmajor"
        self.ap = AnnotationParser(data_file)
        self.ap.parse_database()

        self.assertEqual(self.ap.get_annotation_count("GO:0003677"), 1)
        self.assertEqual(self.ap.get_annotation_count("GO:0003682"), 1)
        self.assertEqual(self.ap.get_annotation_count("GO:0003779"), 1)
        self.assertEqual(self.ap.get_annotation_count("GO:0004618"), 2)
        self.assertEqual(self.ap.get_annotation_count("GO:0005634"), 1)  # 1 repeat term
        self.assertEqual(self.ap.get_annotation_count("GO:0005666"), 1)
        self.assertEqual(self.ap.get_annotation_count("GO:0005885"), 3)  # 1 repeat term
        self.assertEqual(self.ap.get_annotation_count("GO:0006096"), 2)
        self.assertEqual(self.ap.get_annotation_count("GO:0006383"), 1)
        self.assertEqual(self.ap.get_annotation_count("GO:0007010"), 1)
        self.assertEqual(self.ap.get_annotation_count("GO:0008612"), 1)
        self.assertEqual(self.ap.get_annotation_count("GO:0015114"), 2)
        self.assertEqual(self.ap.get_annotation_count("GO:0016021"), 2)
        self.assertEqual(self.ap.get_annotation_count("GO:0020015"), 2)
        self.assertEqual(self.ap.get_annotation_count("GO:0030036"), 1)  # 1 repeat term


