'''
Created on Nov 22, 2011

@author: sw167

maybe a better way to create proper test suite, which allow the testRunner to call it automatically
./src python test/main.py
./src python -m unittest discover -v 

 ## no ".py", auto call testRunner
./src python -m unittest test.main 
'''

import sys
sys.path.append("/home/sw167/Postdoc/Project_Lemur/src/")
import unittest
import test_sequence



def test_main():
    alltests = unittest.TestSuite([test_sequence.suite])
    unittest.TextTestRunner(verbosity=2).run(alltests)


    
if (__name__ == '__main__') | (__name__ == 'test.main') :
    # test.main is used for "-m unittest test.main" 
    test_main()



#TODO fix this to allow -m unittest to test.main works properly 
#class TestMain(unittest.TestSuite):
class TestMain(unittest.TestCase):

    def test_method(self):
        print __name__
        alltests = unittest.TestSuite([test_sequence.suite, test_sequence.suite])
        tt = unittest.TestSuite()
        tt.addTest(test_sequence.suite)
    
    