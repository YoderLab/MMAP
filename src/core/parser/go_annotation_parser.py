'''
Created on Dec 8, 2011

@author: Steven Wu
'''

from core.parser import parser


def parse_version(readline):
    return parser.parse_keyword(readline, "!CVS Version: Revision", "$")
    
def parse_date(readline):
    return parser.parse_keyword(readline, "!GOC Validation Date:", "$")


def addPair(annotation, key, value):
    if key in annotation:
        annotation[key].add(value)
    else:
        annotation[key] = {value}


class AnnotationParser(object):
    '''
    Parse annotation files downloaded from
    http://www.geneontology.org/GO.downloads.annotations.shtml
    Only tested on "Filtered Files" at this stage
    use GAF 2.0 format
    http://www.geneontology.org/GO.format.gaf-2_0.shtml
    '''


    def __init__(self, file):
        '''
        Constructor
        '''
        self.file = file
    
    
    def parse_database(self):        
        '''
        GAF 2.0 format
        take 
            2    DB Object ID 
            5    GO ID
        TODO: double check which field to use
        '''
        self.data = open(self.file, "r")
        self.cvs_version = parse_version(self.data.readline())
        self.goc_validation_date = parse_date(self.data.readline())
#        print "\n","zz",self.version
        self.annotation = dict() #{str(id) : set(is_a)} 
        
        print "Begin parsing annotation version: %s date: %s" %(self.cvs_version, self.goc_validation_date)
        
        self.line = self.data.readline()
        while self.line != "":
            if not self.line.startswith("!"):
                self.token = self.line.split("\t")
                self.key = self.token[4]
                self.value = self.token[1] #TODO: double check which field to use
                addPair(self.annotation, self.key, self.value)
            
            self.line = self.data.readline()

        self.data.close()

        print "Done"
        
        
    def get_annotation_count(self, key):
        terms = self.annotation[key]
        return len(terms)