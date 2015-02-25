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
# from test import *
from test.assembler import *
from test.component import *
from test.connector import *
from test.parser import *
from test.utils import *
import unittest


# BLAST.test_create**from file
# test_runextprog_check
# Metasim
#

# # TODO: remove some files from repositories. tracking too many files
# # git ls-files
# # git rm --cached filename
# # add file to .gitignores
#



# class TestMain(unittest.TestCase):
#
#    def setUp(self):
#        self.seq = range(10)


class TestAll(unittest.TestCase):

    CWD = os.getcwd()
#    src_dir = path_utils.get_parent_path(CWD)
#    sys.path.append(src_dir)
#
#    print "\n==start test_main()=="
#    alltests = unittest.TestSuite()
#
#    alltests.addTests(unittest.TestLoader().loadTestsFromModule(test_sequence))
# #    from test.test_sequence import TestSequence
# #    alltests.addTests( unittest.TestLoader().loadTestsFromTestCase(TestSequence ))
#    print alltests
#    print alltests.countTestCases()
#    unittest.TextTestRunner(verbosity=2).run(alltests)
#    print "==end test_main()==\n"
#
# if (__name__ == '__main__') | (__name__ == 'test.main') :
# #     test.main is used for "-m unittest test.main"
#    test_main()

if __name__ == '__main__':
    unittest.main(verbosity=2)
#    suite = unittest.TestLoader().loadTestsFromTestCase(TestAll)
#    suite = unittest.TestSuite()
#    suite.addTests(unittest.TestLoader().discover(os.getcwd()))
#    suite.addTests(unittest.TestLoader().loadTestsFromModule(TestAll))
#    unittest.TextTestRunner(verbosity=2).run(suite)
