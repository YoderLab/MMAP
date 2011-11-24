'''
Created on Nov 22, 2011

@author: sw167

maybe a better way to create proper test suite, which allow the testRunner to call it automatically
./src python test/main.py
./src python -m unittest discover -v 

 ## no ".py", auto call testRunner
./src python -m unittest test.main 
'''

import unittest
import sys
from test.test_sequence import TestSequence
from test.test_hclust import TestHClust
sys.path.append("/home/sw167/Postdoc/Project_Lemur/src/")

import test_sequence
import test_hclust


def test_main():
    print "\n"
    alltests = unittest.TestSuite(test_sequence.suite)
    alltests.addTests( unittest.TestLoader().loadTestsFromTestCase(TestSequence) )
    alltests.addTests( unittest.TestLoader().loadTestsFromTestCase(TestHClust) )
    print alltests
    print alltests.countTestCases()
    unittest.TextTestRunner(verbosity=2).run(alltests)
    
    
    
    
    
if (__name__ == '__main__') | (__name__ == 'test.main') :
    # test.main is used for "-m unittest test.main" 
    test_main()



#TODO fix this to allow -m unittest to test.main works properly 
#class TestMain(unittest.TestSuite):
class TestMain(unittest.TestCase):

    def test_method(self):
        print "====call test_method===="
        alltests = unittest.TestSuite([test_sequence.suite])
        tt = unittest.TestSuite()
        tt.addTest(test_sequence.suite)
    
    