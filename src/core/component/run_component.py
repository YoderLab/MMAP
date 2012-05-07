import os

__author__ = 'erinmckenney'


class RunComponent(object):

    def __init__(self):

        self.allextw=[]


    def check_outfiles_exist(self, outfile_tag):
    #        allextw=[".status", ".dump1", ".dump.best"]
        print "in c", self.allextw
        isExist = self.check_multiple_outfiles_existence( outfile_tag, self.allextw)
        return isExist

    def check_multiple_outfiles_existence(self, outfileTag, allext, isExist=True):
        for ext in allext:
            isExist = self.check_file_existence( outfileTag, ext, isExist)
        return isExist



    def check_file_existence(self, filetag, ext, isExist):
#        print(type(filetag))
#        print(type(ext))
        test_file= "%s%s" % (filetag, ext)
#        print ext," file:",test_file

#        print "*",ext," file:",test_outfile
        if os.path.exists(test_file):
        #            print ext,"  outfile exists."
            isExist=isExist and True
        else:
            isExist=False
        #            print "Error: ",ext,"  outfile does not exist."

        return isExist


