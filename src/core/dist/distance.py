'''
Created on Nov 25, 2011

@author: Steven Wu
'''


def check_param(comb_list):
    '''
    TODO
    check if comb_list is valid, should be list[comb[], set1[], set2[]]
    '''
    #    print type(comb_list)
    #    print type(comb_list[1])
    #    print type(comb_list[1][0])
    #    print type(comb_list[1][1])
    #    print type(comb_list[1][2])
    #    print type(comb_list[2][0])
    #    print type(comb_list[2][1])
    #    print type(comb_list[2][2])

    if not isinstance(comb_list, list):
        print "type(comb_list) is not list"
    if not isinstance(comb_list[1], tuple):
        print "type(comb_list[i]) is not tuple"

    return comb_list


class Distance(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
