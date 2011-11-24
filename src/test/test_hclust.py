'''
Created on Nov 23, 2011

@author: Steven Wu
'''
import unittest
from core.hclust import HClust
import numpy
#from Pycluster import *
from Bio.Cluster import *

class TestHClust(unittest.TestCase):



    def setUp(self):
        dist = 0
        self.hc = HClust(dist)


    def tearDown(self):
        pass


    def test_treeclust_dataset1_single(self):
        len_set = 5
        self.hc.distMatrix = dataset1(len_set)
        self.hc.treecluster(method="s")
        for i in range(0,len_set-1):
            self.assertEqual(self.hc.distMatrix[i+1,0], self.hc.tree[i].distance)
            
    def test_treeclust_dataset1_complete(self):
        len_set = 5
        self.hc.distMatrix = dataset1(len_set)
        self.hc.treecluster(method="m")
        for i in range(0,len_set-1):
            self.assertEqual(self.hc.distMatrix[i+1,i], self.hc.tree[i].distance)
            
    def test_treeclust_dataset1_average(self):
        len_set = 5
        self.hc.distMatrix = dataset1(len_set)            
        self.hc.treecluster(method="a")
        for i in range(0,len_set-1):
            expected =  numpy.mean(self.hc.distMatrix[i+1, range(0,i+1)]) #row mean
            self.assertEqual(expected, self.hc.tree[i].distance)

    def test_treeclust_dataset2_single(self):
        
        self.hc.distMatrix = dataset2()
        self.hc.treecluster(method="s")
        expected = [2, 6, 10, 21]
        for i in range(0,4):
            self.assertEqual(expected[i], self.hc.tree[i].distance)

    def test_treeclust_dataset2_complete(self):
        
        self.hc.distMatrix = dataset2()
        self.hc.treecluster(method="m")
        expected = (2, 6, 15, 38)
        for i in range(0,4):
            self.assertEqual(expected[i], self.hc.tree[i].distance)


    def test_treeclust_dataset2_average(self):
        
        self.hc.distMatrix = dataset2()
        self.hc.treecluster(method="a")
        expected = (2, 6, 12.5, 30+(1.0/3))
        for i in range(0,4):
            self.assertEqual(expected[i], self.hc.tree[i].distance)

#        print self.hc.distMatrix
#        print len(self.hc.tree)
#        for i in range(0,len_set-1):
#            self.assertEqual(self.hc.distMatrix[i+1,0], self.hc.tree[i].distance)
#
#        self.hc.treecluster(method="m")
#        for i in range(0,len_set-1):
#            self.assertEqual(self.hc.distMatrix[i+1,i], self.hc.tree[i].distance)



''' global method''' 
def dataset1(len_set):


    dist = numpy.zeros(shape=(len_set, len_set), dtype=numpy.float32)
    k=0
#    dist_array = array("f") # array to matrix in row based order
    for i in range(0, len_set):
        for j  in range(i+1, len_set):
            k += 1
            dist[j, i] = k
#            dist_array.append(k)

#    for les_set = 5
#    [[  0.   0.   0.   0.   0.]
#     [  1.   0.   0.   0.   0.]
#     [  2.   5.   0.   0.   0.]
#     [  3.   6.   8.   0.   0.]
#     [  4.   7.   9.  10.   0.]]

    return dist

def dataset2():
    '''
    output from R
            1  2  3  4
        2 38         
        3 33  6      
        4 21 10 15   
        5  2 35 29 26
    single: 2  6 10 21
    complete: 2  6 15 38
    average:  2.00000  6.00000 12.50000 30.33333

    '''
    dist = numpy.zeros(shape=(5, 5), dtype=numpy.float32)
    dist[1,0] = 38
    dist[2,0:2] = (33,6)
    dist[3,0:3] = (21, 10, 15)   
    dist[4,0:4] = (2, 35, 29, 26)
    
    return dist



def dataset3():
    
    set0 = set(['GO:001', 'GO:002', 'GO:003', 'GO:004']) 
    set1 = set(['GO:001', 'GO:002', 'GO:003', 'GO:004', 'GO:005'])
    set2 = set(['GO:003', 'GO:006', 'GO:007'])
    set3 = set(['GO:001', 'GO:002', 'GO:009', 'GO:010'])
    set4 = set(['GO:002', 'GO:003', 'GO:005', 'GO:010', 'GO:100'])

    ##assuming set(s) store as list for now
    all_sets =  [set0, set1, set2, set3, set4]
    len_set = len(all_sets)

    dist = numpy.zeros(shape=(len_set, len_set), dtype=numpy.float32)

    for i, s in enumerate(all_sets):
        for j, t in enumerate( all_sets[(i+1):len_set] ):
#            print "i:%d \t j:%d \t %d and %s and t: %s" % (i ,j+i+1,len(s&t), str(s), str(t))
            dist[i+j+1, i] = len(s&t)
#
#[[ 0.  0.  0.  0.  0.]
# [ 3.  0.  0.  0.  0.]
# [ 1.  2.  0.  0.  0.]
# [ 1.  1.  0.  0.  0.]
# [ 2.  2.  1.  2.  0.]]
    print dist
    return dist


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_treeclust']
    unittest.main(verbosity=2)
    
    