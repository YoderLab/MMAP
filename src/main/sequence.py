from Bio import Seq

class Sequence(object):
    """store all blast results from 1 seq
    class __doc__
    """
    def __init__(self, data=None):
        if not (isinstance(data, Seq.Seq) or isinstance(data, str)):
            raise TypeError("Incorrect type, must be Bio.Seq.Seq or str: type(data) = %s" % type(data))
        self.each_term = dict()
        self.all_terms = set()
        self.data = data
        self.is_match = False
        self.web_page = None
        self.acc_ID, self.match_ID, self.e_value = [], [], []

        
    def add(self, key, term):
        '''append term, term must be a list (str doesnt work)'''
        self.each_term[key] = term
        self.all_terms.update(term)
    
    def add_multi(self, key, *terms):
        '''append multiple terms to the same key'''
        for term in terms:
            self.each_term[key] = term
            self.all_terms.update(term)
            
    def get_one_term(self, key):
        return self.each_term[key]

## test property    
    def get_web_page(self):
        return self.__web_page

    def set_web_page(self, value):
        self.__web_page = value

    def del_web_page(self):
        del self.__web_page
        
    web_page = property(get_web_page, set_web_page, del_web_page, "Testing property")
    



class Hits(object):
    
    def __init__(self):
        self.acc_ID = None
        self.match_ID = None
        self.e_value = None
        
        