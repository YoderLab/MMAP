"""
Created on March 19, 2012

@author: Erin McKenney
"""

import os
from core.component.run_component import RunComponent
from core.run_ext_prog import runExtProg

class RunGlimmer(RunComponent):
    """
    classdocs
    """


    def __init__(self, infile, pdir, wdir=None, outfile=None, checkExist = True):
        """
        Constructor
        """
        self.allextw=[".coords", ".detail", ".icm", ".longorfs", ".motif", ".predict", ".run1.detail", ".run1.predict", ".train", ".upstream"]
#        Make sure directory ends with a "/":
        if pdir.endswith("/"):
            self.pdir=pdir
        else:
            self.pdir = pdir+"/"

        self.wdir = wdir
        if self.wdir is None:
            self.wdir = self.pdir

        self.infile_class_var = self.wdir+infile

        ## TODO (Steven): use this to demonstrate refactor

        if outfile is None:
            self.outfileTag = self.generate_outfile_name(self.infile_class_var,"_out")
        else:
            self.outfileTag = self.wdir+outfile

        if checkExist:
            self.check_infile_exist()

        self.glimmer = runExtProg("./g3-iterated.csh", pdir=self.pdir, length=2, checkOS=True)
        self.setInfileName(self.infile_class_var)
        self.set_output_tag(self.outfileTag)

        
    def run(self):
        self.glimmer.run()
#    def getRecord(self):
#        return self.record

    def get_switch(self):
        return self.glimmer.__switch
#

    def setInfileName(self, infile):
        """
        TODO: check valid infile, infile exist or not
        """
#        if os.path.isdir(infile) != True:
#            infile = self.wdir+infile
#            print("setInfile to", infile)
        self.glimmer.set_param_at(infile, 1)


    def set_output_tag(self, outfile):
#        if os.path.isdir(outfile) != True:
#            outfile = self.wdir+outfile
#            print("setOutfile to", outfile)
        self.glimmer.set_param_at(outfile, 2)

#    def generate_outfile_name(self, infile):
#        """
#        infile name
#               testGlimmer.poiuyxcvbjkfastaaaasdfghjk
#        step1: testGlimmer
#        step2: testGlimmer_out.fasta
#        step3: self.pdir+testGlimmer_out.fasta
#            check if it exist
#            overwrite or not
#
#
#        if os.path.exists(  self.cwd+self.name_only  ):
#        if os.path.exists(  full_file_path  ):
#        """
#        location=infile.rfind(".")
#        if location is -1:
#            namebase=infile
#        else:
#            namebase=infile[0:location]
#        #        print "location", location, infile, infile[0:location]
#        outfile=namebase+"_out"
#        return outfile


    #Check whether infile exists:
#    def check_infile_exist(self):
#        """
#         TODO: add code to check if these exist
#         check if self.pdir exist
#         check if infile exist
#         check if outfile already exist
#
#         use
#         if os.path.exists( fileName ):
#        """
#        if not os.path.exists(self.wdir):
#            raise IOError("Error: invalid directory: %s" %self.wdir)
#        #        If the directory is valid, this chunk makes sure the infile exists.
##        self.infile_path="%s%s" % (self.pdir, self.infile_class_var)
##        print "Infile path set to:",self.infile_path
#
#        if not self.check_file_existence( "", self.infile_class_var, True):
#            raise IOError("Error: infile does not exist. %s%s"%(self.wdir, self.infile_class_var))
#        #        This chunk makes sure you won't overwrite an existing outfile.
##        self.outfile_path="%s%s" % (self.wdir, self.outfileTag)
#
#        isExist = self.check_outfiles_exist(self.allextw)
#
#        if isExist:
#            raise IOError("WARNING: outfile already exists!!!")
#            #TODO: come back to this later.
#        #            Can rename the file, raise a different error, etc.


#
#    def check_outfiles_exist(self,  outfile_tag):
#        """
#        check
#        *.coords
#        *.detail
#        *.icm
#        *.longorfs
#        *.motif
#        *.preict
#        *.run1.detail
#        *.run1.predict
#        *.train
#        *.upstream
#        exist
#        """
#        print "in Glimmer"
#        self.allextw=[".coords", ".detail", ".icm", ".longorfs", ".motif", ".predict", ".run1.detail", ".run1.predict", ".train", ".upstream"]
#        isExist = self.check_multiple_outfiles_existence( self.outfileTag, allextw)
#        return isExist
#




