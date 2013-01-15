'''
Created on Nov 30, 2011

@author: Steven Wu
'''
import os
import re


def get_parent_path(path, above=1):
    while above != 1:
        path = path[0:path.rfind(os.sep)]
        above -= 1
    else:
        try:
            return path[0:path.rindex(os.sep)]
        except ValueError as e:
            raise ValueError("Exception error is: %s, too many levels above path" % e)


def get_data_dir(path=os.getcwd()):
    '''
    find */src/ then go ../src/data/
    '''
    while path.find("src") != -1:
        path = get_parent_path(path)

    return path + os.sep + "data" + os.sep



def append_before_ext(name, ext):
    index = name.rfind(".")
    if index > -1:
        new_name = name[0:index] + ext + name[index:len(name)]
    else:
        new_name = name + ext
    return new_name


def remove_ext(name):
    index = name.rfind(".")
    if index > -1:
        name = name[0:index]
    return name


def check_wdir_prefix(wdir, filename):
    if filename.find(wdir) is -1:
        filename = wdir + filename
    return filename


def check_program_dir(dir_prefix, pdir=""):
    """
    make sure it's /widr/pdir/ format with os.sep
    """
#    pdir = os.sep + dir_prefix + os.sep + pdir + os.sep
#    pdir = re.sub("%s+" % os.sep, os.sep, pdir)
    new_path = os.path.normpath(dir_prefix + os.sep + pdir)

    return new_path


class PathUtils(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

