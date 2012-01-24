'''
Created on Nov 22, 2011

@author: sw167

#fully auto method
cd ./src
python -m unittest discover -v 

 #no ".py", auto call testRunner
 #create proper test suite, which allow the testRunner to call it automatically
 #need add from * import *
cd ./src
python -m unittest -v test.main 
'''

from test.parser.test_go_annotation_parser import TestGoAnnotationParser
from test.parser.test_go_OBO_parser import TestGOOBOParser

from test.test_distance import TestDistance
from test.test_hclust import TestHClust
from test.test_run_ext_prog import TestRunExtProgram
from test.test_sequence import TestSequence


#def test_main():
#    '''
#    Testing method
#    run test class/module 
#    '''
#    #import sys
#    #import os
#    #from core.utils import path_utils
#    #CWD = os.getcwd()
#    #src_dir = path_utils.get_parent_path(CWD)
#    #sys.path.append(src_dir)
#    
#    import unittest
#    print "\n==start test_main()=="
#    alltests = unittest.TestSuite()
#
#    import test_sequence
#    alltests.addTests( unittest.TestLoader().loadTestsFromModule(test_sequence) )
#    from test.test_sequence import TestSequence
#    alltests.addTests( unittest.TestLoader().loadTestsFromTestCase(TestSequence ))
#    print alltests
#    print alltests.countTestCases()
#    unittest.TextTestRunner(verbosity=2).run(alltests)
#    print "==end test_main()==\n"
#    
#if (__name__ == '__main__') | (__name__ == 'test.main') :
##     test.main is used for "-m unittest test.main" 
#    test_main()

