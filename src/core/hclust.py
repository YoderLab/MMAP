'''
Created on Nov 23, 2011

@author: Steven Wu
'''
from Bio import Cluster 
from Bio.Cluster import *
#from Pycluster import * #same so Bio.Cluster

            
class HClust(object):
    '''
    act as a wrapper for Bio.Cluster
    '''


    def __init__(self, dist):
        '''
        Constructor
        '''
        self.distMatrix = dist
        self.tree = None

        

    def treecluster(self, mask=None, weight=None, transpose=0, method='m'):
        '''
        distancematrix = self.distMatrix
        
       method   : specifies which linkage method is used:
           method=='s': Single pairwise linkage
           method=='m': Complete (maximum) pairwise linkage (default)
           method=='c': Centroid linkage
           method=='a': Average pairwise linkage
        '''
        self.tree = treecluster(distancematrix=self.distMatrix, mask=mask, weight=weight, transpose=transpose, method=method)
        
    
    def cal_dist(self, data, mask=None, weight=None, transpose=0, dist='e'):
        '''
        update self.dist
           dist=='e': Euclidean distance
           dist=='b': City Block distance
           dist=='c': Pearson correlation
           dist=='a': absolute value of the correlation
           dist=='u': uncentered correlation
           dist=='x': absolute uncentered correlation
           dist=='s': Spearman's rank correlation
           dist=='k': Kendall's tau
        '''
        self.distMatrix = distancematrix(data, mask=mask, weight=weight, transpose=transpose, dist=dist)
    
    
    def test_hclust_save(self):
        '''
        still need a way to save/export properly
        '''
        working_dir = "/home/sw167/Postdoc/Project_Lemur/Data/"
        handle = open(working_dir+"mydatafile.txt", 'w')
        
        handle.write("1 2 3\n")
        handle.write("1 22 3\n")
        handle.write("1 2 33")
        handle.close()
        
        handle = open(working_dir+"mydatafile.txt")
        record = Cluster.read(handle )
        
#        record.data = dist
        record.gorder = numpy.arange(4)
        print record.data
        print numpy.shape(record.data)
        
        print dir(record)
        genetree = record.treecluster(method='s')
        genetree.scale()
        exptree = record.treecluster(dist='u', transpose=1)
        record.save(working_dir+"cyano_result", genetree, exptree)
        print genetree
        print exptree
#        record.save(working_dir+"testResult", geneclusters=tree, expclusters=tree)
        handle.close()
            
        
    
    def test_hcluster_module(self):
        '''
        @Deprecated
        test methods is hcluster module
        use other package, required ipython to visualise the result
        '''
        from numpy.random import rand
        from hcluster import *
        from hcluster import pdist, linkage, squareform, dendrogram

        X = rand(3,5)
    
        Y=pdist(X, 'seuclidean')
        Z=linkage(Y, 'single')
        print "X:",X
        print "Y:",Y, type(Y),  Y.shape, Y.dtype
        print "Z:",Z
        
    #    Y=numpy.ndarray(numpy.array([1.1,2.2,3.3,4.4]))
        Y= numpy.array(range(1,7))
        print "Y:",Y, type(Y),  Y.shape, Y.dtype
        print squareform(Y)
        Z=linkage(Y, 'single')
    
        print "Z:",Z
        print dendrogram(Z)
        
    #    set1 = set([]) 
    #    set2 = set(['GO:0016310', 'GO:0009067', 'GO:0005488', 'GO:0016597', 'GO:0016491', 'GO:0005737', 'GO:0006566', 'GO:0050661', 'GO:0040007', 'GO:0009570', 'GO:0005634', 'GO:0006520', 'GO:0019877', 'GO:0000166', 'GO:0016740', 'GO:0009097', 'GO:0009090', 'GO:0009088', 'GO:0016301', 'GO:0003824', 'GO:0008152', 'GO:0005886', 'GO:0055114', 'GO:0009507', 'GO:0008652', 'GO:0005829', 'GO:0006555', 'GO:0004412', 'GO:0005575', 'GO:0009089', 'GO:0005524', 'GO:0006531', 'GO:0009086', 'GO:0004072', 'GO:0009082'])
    #    set3 = set(['GO:0004803', 'GO:0006313'])
    #    set4 = set(['GO:0005125', 'GO:0016311', 'GO:0046360', 'GO:0003674', 'GO:0030170', 'GO:0004795', 'GO:0005737', 'GO:0006566', 'GO:0005615', 'GO:0016829', 'GO:0006520', 'GO:0005524', 'GO:0004765', 'GO:0003824', 'GO:0008150', 'GO:0070905', 'GO:0008152', 'GO:0009071', 'GO:0008652', 'GO:0006897', 'GO:0005829', 'GO:0005575', 'GO:0005576', 'GO:0009088', 'GO:0005515', 'GO:0005634'])
    #    set5 = set(['GO:0005737', 'GO:0016310', 'GO:0009617', 'GO:0004413', 'GO:0000166', 'GO:0009620', 'GO:0009088', 'GO:0009570', 'GO:0009086', 'GO:0005524', 'GO:0009507'])
    #    
        
        set1 = set([]) 
        set2 = set(['GO:001', 'GO:002', 'GO:003', 'GO:003', 'GO:004'])
        set3 = set(['GO:003', 'GO:004'])
        set4 = set(['GO:005', 'GO:006', 'GO:007'])
        set5 = set(['GO:005', 'GO:006', 'GO:009', 'GO:010', 'GO:100'])
        
        ##assuming set(s) store as list for now
        all_sets =  [set1, set2, set3, set4, set5]
        len_set = len(all_sets)
        Y = numpy.ndarray(shape=(len_set*(len_set-1)/2))
        Y= numpy.zeros(shape=(len_set*(len_set-1)/2), dtype=numpy.int32)
        k = 1
        for i, s in enumerate(all_sets):
            for j, t in enumerate( all_sets[(i+1):len_set] ):
    #            print s, "and i:", i, "and t:", t 
                print "%s and \t i:%d \t j:%d and t: %s" % (str(s), i ,j+i+1,str(t))
                Y[k] = len(s&t)
                k += 1
    
        print "Round Y:", Y
        print squareform(Y)
        Z=linkage(Y, 'single')
        
        print "Z:",Z, type(Z)
        print dendrogram(Z,no_plot=True)
        
    
    
        