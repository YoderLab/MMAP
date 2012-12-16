"""
Created on Dec 5, 2012

@author: Steven Wu
"""
def append_before_ext(name, ext):
    index = name.rfind(".")
    if index > -1:
        new_name = name[0:index] + ext + name[index:len(name)]
    else:
        new_name = name + ext
    return new_name

class FileUtility(object):
    """
    classdocs
    """


    def __init__(self):
        """
        Constructor
        """
