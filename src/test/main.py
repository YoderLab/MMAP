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
## check, auto run the test suite
from test.test_sequence import TestSequence
from test.test_hclust import TestHClust
from test.test_distance import TestDistance
from test.parser.test_go_OBO_parser import TestGOOBOParser
sys.path.append("/home/sw167/Postdoc/Project_Lemur/src/")

import test_sequence
import test_hclust


def test_main():
    print "\n"
    alltests = unittest.TestSuite()
    alltests.addTests( unittest.TestLoader().loadTestsFromTestCase(TestSequence) )
    alltests.addTests( unittest.TestLoader().loadTestsFromTestCase(TestHClust) )
    alltests.addTests( unittest.TestLoader().loadTestsFromTestCase(TestDistance) )
    print alltests
    print alltests.countTestCases()
    unittest.TextTestRunner(verbosity=2).run(alltests)
    
    
    
    
    
if (__name__ == '__main__') | (__name__ == 'test.main') :
    # test.main is used for "-m unittest test.main" 
    test_main()


