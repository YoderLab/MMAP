'''
Created on Nov 25, 2011

@author: Steven Wu
'''
from core.dist.distance import Distance, check_param
import numpy
from core.zdeprecated.sequence import Sequence


class BasicDistance(Distance):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def cal_dist(self, data):

        if isinstance(data, Sequence):
            comb_list = data.get_combinations()
            len_set = len(data)
        else:
            comb_list = check_param(data)
            len_c = len(comb_list)

            d = int(numpy.ceil(numpy.sqrt(len_c * 2)))
            d2 = d * (d - 1) / 2
            if d2 != int(len_c):
                ##TODO update error message
                raise ValueError('Incompatible vector size. It must be a binomial coefficient n choose 2 for some integer n >= 2.')
            else:
                len_set = d

#            checking algorithm from /usr/lib64/python2.7/site-packages/hcluster/distance.py", line 1337, in squareform
#            d = int(numpy.ceil(numpy.sqrt(i * 2)))
#            # Check that v is of valid dimensions.
#            if d * (d - 1) / 2 != int(i):
#                raise ValueError('Incompatible vector size. It must be a binomial coefficient n choose 2 for some integer n >= 2.')

        self.dist = numpy.zeros(shape=(len_set, len_set), dtype=numpy.float32)

        for comb in comb_list:
            self.dist[comb[0][0], comb[0][1]] = len(comb[1] & comb[2])

        return self.dist
