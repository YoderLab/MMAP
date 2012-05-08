import os

__author__ = 'erinmckenney'


class RunComponent(object):

    def __init__(self):

        self.allextw=[]

    def checkInfileExist(self):
        if not os.path.exists(self.wdir):
            raise IOError("Error: invalid directory: %s" %self.wdir)
            #        If the directory is valid, this chunk makes sure the infile exists.
        #        self.infile_path="%s%s" % (self.pdir, self.infile_class_var)
        #        print "Infile path set to:",self.infile_path

        if not self.check_file_existence( "", self.infile_class_var, True):
            raise IOError("Error: infile does not exist. %s%s"%(self.wdir, self.infile_class_var))
            #        This chunk makes sure you won't overwrite an existing outfile.
        #        self.outfile_path="%s%s" % (self.wdir, self.outfileTag)

#        isExist = self.check_outfiles_exist(self.allextw)
#
#        if isExist:
#            raise IOError("WARNING: outfile already exists!!!")
#            #TODO: come back to this later.

    def GenerateOutfileName(self, infile, outtag):
        """
        infile name
            check if it exist
            overwrite or not
        if os.path.exists(  self.cwd+self.name_only  ):
        if os.path.exists(  full_file_path  ):
        """
        location=infile.rfind(".")
        if location is -1:
            namebase=infile
        else:
            namebase=infile[0:location]
        #        print "location", location, infile, infile[0:location]
        outfile=namebase+outtag
        return outfile


    def check_outfiles_exist(self, outfile_tag):
    #        allextw=[".status", ".dump1", ".dump.best"]
#        print "in c", self.allextw
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


