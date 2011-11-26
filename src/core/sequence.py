'''

@author: Steven Wu
'''


from Bio import Seq
import numpy

class Sequence(object):
    """store all blast results from 1 seq
    class __doc__
    """
    def __init__(self, data=None):
        if not (isinstance(data, Seq.Seq) or isinstance(data, str)):
            raise TypeError("Incorrect type, must be Bio.Seq.Seq or str: type(data) = %s" % type(data))
        self.each_term = dict() #{str: set()}
        self.all_terms = set()
        self.data = data
        self.is_match = False
        self.web_page = None
        self.len = 0
        self.acc_ID, self.match_ID, self.e_value = [], [], []

        
    def add(self, key, term):
        '''append term, term must be a list (str doesnt work)'''
        self.each_term[key] = set(term)
        self.all_terms.update(term)
        self.len += 1
    
    def add_multi(self, key, *terms):
        '''append multiple terms to the same key'''
        for term in terms:
            self.add(key, term)

    def __len__(self):
        ''' "Emulating" method, should override len()''' 
        return self.len
            
    def get_one_term(self, key):
        return self.each_term[key]

    def get_combinations(self):
        '''
        return tuple (index_in_dist_matrix, set1, set2)
        index_in_dist_matrix in "tuple", with (row_index, col_index) for lower triangle 
        '''
        
        keyList = self.each_term.keys();
        len_set = len(keyList)
#        dist = numpy.zeros(shape=(len_set, len_set), dtype=numpy.float32)
        combList = []
        for i, u in enumerate(self.each_term.values()):
            for j in range(i+1, len_set):
                v = self.each_term.get(keyList[j])
#                print "i:%d \t j:%d \t %d and %s and %s" % (i ,j,len(u&v), str(u), str(v))
                combList.append(((j, i), u, v))            

        return combList

    ## TODO: 
    def cal_distance(self, method="s"):
        if method == "s":
            return 0

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
        
        