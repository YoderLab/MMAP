'''
Created on March 7, 2011

@author:  Steven Wu
'''
import pickle
from core.parser import parser


def parse_version(readline):
    return parser.parse_keyword(readline, "version:")


def parse_date(readline):
    return parser.parse_keyword(readline, "date:")


def parse_id(readline):
    return parser.parse_keyword(readline, "id:")


def parse_name(readline):
    return parser.parse_keyword(readline, "name:")


def parse_namespace(readline):
    return parser.parse_keyword(readline, "namespace:")


def parse_isa(readline):
    index_start = readline.find("is_a:") + 5
    index_end = readline.find("!")
    return readline[index_start:index_end].strip()


class OBOParser(object):
    '''
    Parser for GO ontology
    OBO format
    OBO v1.2
    http://www.geneontology.org/GO.downloads.ontology.shtml
    '''

    def parse_database(self):
        '''
        version and date should be the first two line in the infile
        e.g.
        format-version: 1.2
        date: 06:12:2011 18:33
        '''
        self.data = open(self.infile, "r")
        self.version = parse_version(self.data.readline())
        self.date = parse_date(self.data.readline())

        print("Begin parsing version: %s date: %s" %
              (self.version, self.date))

        self.dict_is_a = dict()  # {str(id) : set(is_a)}
        self.line = self.data.readline()
        while self.line != "":

            if self.line.find("[Term]") != -1:
                self.id = parse_id(self.data.readline())
                self.name = parse_name(self.data.readline())
                self.namespace = parse_namespace(self.data.readline())
                self.in_term = True
                self.set = set()

                while self.in_term:
                    self.line = self.data.readline()
                    if self.line.find("is_obsolete: true") != -1:
                        self.in_term = False
                    if self.line == "\n":
                        self.in_term = False
                    if self.line.find("is_a") != -1:
                        self.set.add(parse_isa(self.line))
                self.dict_is_a[self.id] = self.set

            self.line = self.data.readline()

        self.data.close()
        print("Done")

    def __init__(self, infile):
        '''
        Constructor
        '''
        self.infile = infile

    def save_dict_to_file(self, outfile):
        '''
        ?save the whole class not just 1 object
        TODO: move save/load to parser class
        '''
        save_file = open(outfile, "w")
#        pickle.dump(self.date, save_file)
        pickle.dump(self.dict_is_a, save_file)
#        pickle.dump(self.version, save_file)
        save_file.close()

    def load_dict_file(self):
        self.dict_file = open(self.infile, "r")
        self.dict_is_a = pickle.load(self.dict_file)
        self.dict_file.close()
        return self.dict_is_a



