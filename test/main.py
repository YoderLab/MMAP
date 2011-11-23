'''
Created on Nov 22, 2011

@author: sw167
'''
import unittest
import test_sequence

def main():
    unittest.TextTestRunner(verbosity=2).run(test_sequence.suite)


if __name__ == '__main__':
    main()
    
    
    