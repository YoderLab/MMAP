'''
Created on Nov 22, 2011

@author: sw167
'''
import unittest
import random
#from ..src import sequence
from main.sequence import Sequence




class TestSequence(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)
        self.s = Sequence("TEST")        
        pass


    def tearDown(self):
        pass

    def test_Add(self):
        
        self.s.add(0,["term0"])
        self.s.add(1,["term1"])
        expect = ["term0","term1"]
        self.assertEqual(self.s.each_term[0], [expect[0]])
        self.assertEqual(self.s.each_term[1], [expect[1]])
        self.assertEqual(self.s.all_terms, set(expect))
        
        self.s.add(2,["term0"])
        self.s.add(3,["term0"])
        self.s.add(4,["term2"])
        expect = ["term0","term1","term2"]
        self.assertEqual(self.s.each_term[0], [expect[0]])
        self.assertEqual(self.s.each_term[1], [expect[1]])
        self.assertEqual(self.s.each_term[2], [expect[0]])
        self.assertEqual(self.s.each_term[3], [expect[0]])
        self.assertEqual(self.s.each_term[4], [expect[2]])
        self.assertEqual(self.s.all_terms, set(expect))


    def test_shuffle(self):
        # make sure the shuffled sequence does not lose any elements
        random.shuffle(self.seq)
        self.seq.sort()
        self.assertEqual(self.seq, range(10))

        # should raise an exception for an immutable sequence
        self.assertRaises(TypeError, random.shuffle, (1,2,3))

    def test_choice(self):
        element = random.choice(self.seq)
        self.assertTrue(element in self.seq)

    def test_sample(self):
        with self.assertRaises(ValueError):
            random.sample(self.seq, 20)
        for element in random.sample(self.seq, 5):
            self.assertTrue(element in self.seq)

#if __name__ == '__main__':
#    unittest.main()
print "====name====:",__name__
#
suite = unittest.TestLoader().loadTestsFromTestCase(TestSequence)
unittest.TextTestRunner(verbosity=2).run(suite)
