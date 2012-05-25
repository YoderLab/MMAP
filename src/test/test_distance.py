'''
Created on Nov 25, 2011

@author: Steven Wu
'''
import unittest
from core.dist.matching_distance import MatchingDistance
from core.sequence import Sequence


class TestDistance(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_Distance_matching_distance(self):


        d = MatchingDistance()
        seq = dataset1();
        expected = [[ 0, 0, 0, 0, 0],
         [ 4, 0, 0, 0, 0],
         [ 1, 1, 0, 0, 0],
         [ 2, 2, 0, 0, 0],
         [ 2, 3, 1, 2, 0]]

        dist = d.cal_dist(seq)
        for i in range(0, dist.shape[0]):
            self.assertEqual(expected[i], list(dist[i, ]))

        del(dist)
        dist = d.cal_dist(seq.get_combinations())
        for i in range(0, dist.shape[0]):
            self.assertEqual(expected[i], list(dist[i, ]))


        pass

def dataset1():

    sets = []
    sets.append(set(['GO:001', 'GO:002', 'GO:003', 'GO:004']))
    sets.append(set(['GO:001', 'GO:002', 'GO:003', 'GO:004', 'GO:005']))
    sets.append(set(['GO:003', 'GO:006', 'GO:007']))
    sets.append(set(['GO:001', 'GO:002', 'GO:009', 'GO:010']))
    sets.append(set(['GO:002', 'GO:003', 'GO:005', 'GO:010', 'GO:100']))

    ##assuming set(s) store as list for now
    s = Sequence("TEST")
    for i, u in enumerate(sets):
        s.add(i, u)
    return s


