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

from test import *
from test.assembler import *
from test.component import *
from test.connector import *
from test.parser import *
import unittest
#
#





#class TestAll(unittest.TestCase):
#    pass

#def test_main():
#    '''
#    Testing method
#    run test class/module
#    '''
#    import sys
#    import os
#    from core.utils import path_utils
#    CWD = os.getcwd()
#    src_dir = path_utils.get_parent_path(CWD)
#    sys.path.append(src_dir)
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

