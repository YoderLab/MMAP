class Sequence:
    """store all blast results from 1 seq"""
    
    def __init__(self, data=None):
        self.eachTerm = dict()
        self.allTerms = set()
        self.data = data
        self.webPage = None
        self.accID, self.matchID, self.eValue  = [],[],[]
        
    def add(self, key, terms):
        self.eachTerm[key]=terms
        self.allTerms.update(terms)
    
    def getOneTerm(self, key):
        return self.eachTerm[key]
    
    ## test property
    def getAllTerms(self):
        return self.allTerms
    def setAllTerms(self, value): 
        self.allTerms = value
    #def delAllTerms(self): 
        #del self.allTerms
    allTerms = property(getAllTerms, setAllTerms, None, doc="""Testing property""")
        
        
