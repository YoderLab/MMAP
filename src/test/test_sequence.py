'''
Created on Nov 22, 2011

@author: Steven Wu
'''

import unittest
import random
#from ..src import sequence
from core.sequence import Sequence




class TestSequence(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)
        self.s = Sequence("TEST")        
        pass


    def tearDown(self):
        pass

    @unittest.skip("demonstrating skipping")
    def testSequence_nothing(self):
        self.fail("shouldn't happen")
        
    def testSequence_add(self):
        
        self.s.add(0,["term0", "term1"])
        self.s.add(1,["term2", "term3"])
        
        expect0 = set(["term0","term1"])
        expect1 = set(["term2","term3"])
        expect01 = set(["term0","term1","term2","term3"])
        
        self.assertSetEqual(self.s.each_term.get(0), expect0)
        self.assertSetEqual(self.s.each_term.get(1), expect1)
        self.assertEqual(self.s.all_terms, expect01)
        
        self.s.add(2,set(["term0", "term1"]))
        self.s.add(3,["term1", "term2"])
        self.s.add(4,["term4", "term5"])
        
        expect2 = set(["term0","term1"])
        expect3 = set(["term1","term2"])
        expect4 = set(["term4","term5"])
        expectAll = set(["term0","term1","term2","term3","term4","term5"])
        
        self.assertSetEqual(self.s.each_term.get(0), expect0)
        self.assertSetEqual(self.s.each_term.get(1), expect1)
        self.assertSetEqual(self.s.each_term.get(2), expect2)
        self.assertSetEqual(self.s.each_term.get(3), expect3)
        self.assertSetEqual(self.s.each_term.get(4), expect4)

        self.assertEqual(self.s.all_terms, expectAll)


    def testSequence_combinations(self):
        
        self.s.add(0,["0", "t00", "t01", "t02", "t03", "t04"])
        self.s.add(1,["1", "t01", "t01", "t02", "t03"])
        self.s.add(2,["2", "t02", "t04", "t06"])
        self.s.add(3,["3", "t03", "t06", "t07", "t08"])
        self.s.add(4,["4", "t04", "t08", "t08", "t10"])
       
        k = 0
        comb =  self.s.get_combinations()
        for i in range(0,5):
            for j in range(i+1,5):
                self.assertTupleEqual( (j,i), comb[k][0])
                self.assertSetEqual(self.s.each_term.get(i), comb[k][1])
                self.assertSetEqual(self.s.each_term.get(j), comb[k][2])
                k += 1

        
    def testSequence_combinations2(self):
        
        self.s.add(0,["0", "t00", "t01", "t02", "t03"])
        self.s.add(1,["1", "t01", "t02", "t03", "t04"])
        self.s.add(2,["2", "t02", "t03", "t04", "t05"])
        self.s.add(3,["3", "t03", "t04", "t05", "t06"])
        self.s.add(4,["4", "t04", "t05", "t06", "t07"])
       
        for comb in self.s.get_combinations():
            self.assertEqual(len(comb[1] & comb[2]), 4-(comb[0][0]-comb[0][1]))
        

    def testSequence_shuffle(self):
        # make sure the shuffled sequence does not lose any elements
        random.shuffle(self.seq)
        self.seq.sort()
        self.assertEqual(self.seq, range(10))

        # should raise an exception for an immutable sequence
        self.assertRaises(TypeError, random.shuffle, (1,2,3))

    def testSequence_choice(self):
        element = random.choice(self.seq)
        self.assertTrue(element in self.seq)

    def testSequence_sample(self):
        with self.assertRaises(ValueError):
            random.sample(self.seq, 20)
        for element in random.sample(self.seq, 5):
            self.assertTrue(element in self.seq)





#suite = unittest.TestLoader().loadTestsFromTestCase(TestSequence)
#unittest.TextTestRunner(verbosity=2).run(suite)
