'''
Created on Nov 30, 2011

@author: Steven Wu
'''
import os

    
def get_parent_path(path, above=1):
    while above != 1:
        path = path[0:path.rfind(os.sep)]
        above -= 1
    else:
        try:
            return path[0:path.rindex(os.sep)]
        except ValueError as e:
            print "Exception error is: %s, too many levels above path" % e;
            raise


def get_data_dir(path=os.getcwd()):
    '''
    find */src/ then go ../src/data/
    '''  
    while path.find("src") != -1:
        path = get_parent_path(path)
        
    return path+os.sep+"data"+os.sep







class pathUtils(object):
    '''
    classdocs
    '''
    

    def __init__(self):
        '''
        Constructor
        '''
        