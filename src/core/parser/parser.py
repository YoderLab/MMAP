'''
Created on Dec 8, 2011

@author: Steven Wu
'''


def parse_keyword(line, keyword, keyword2=""):
    index = line.find(keyword)
    if keyword2 == "":
        index_end = len(line)
    else:
        index_end = line.rfind(keyword2)
    if index == -1:
        return None
    else:
        if keyword.endswith(":"):
            return line[index + len(keyword) + 1:index_end].strip()
        else:
            indexC = line.find(":", index + len(keyword))
            return line[indexC + 1:index_end].strip()


class Parser(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
