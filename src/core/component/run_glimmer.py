"""
Created on March 19, 2012

@author: Erin McKenney
"""

import os
from core.run_ext_prog import runExtProg

class RunGlimmer(object):
    """
    classdocs
    """


    def __init__(self, infile, pdir, outfile=None, checkExist = True):
        """
        Constructor
        """

#        Make sure directory ends with a "/":
        if pdir.endswith("/"):

            self.pdir=pdir
        else:
            self.pdir = pdir+"/"



        self.infile_class_var = infile
        ## TODO (Steven): use this to demonstrate refactor
        self.outfileTag = outfile
        if outfile is None:
            self.outfileTag = self.GenerateOutfileName(self.infile_class_var)

        if checkExist:
            self.checkInfileExist()

#            Do we call the script using subprocess.call?
#            ...in which case, how to we set input and output parameters?
#        self.glimmerScript = subprocess.call(['./g3-iterated.csh'+ '%'+ '%'% (self.infile_class_var, self.outfileTag)])
#        self.setInfileName(self.infile_class_var)
#        self.setOutputTag(self.outfileTag)

#            Or, do we call the script using runExtProg?
        self.glimmer = runExtProg("./g3-iterated.csh", pdir=self.pdir, length=2, checkOS=True)
        self.setInfileName(self.infile_class_var)
        self.setOutputTag(self.outfileTag)

        
    def run(self):
        self.glimmer.run()
#    def getRecord(self):
#        return self.record

    def get_switch(self):
        return self.glimmer._switch
#
#    def setSwitchRead(self, v):
#        """
#          -r, --read arg         read file
#        """
#        self.g3Iterated.add_switch(v)
#        self.finalize.set_param_at(v+".fasta")
#
#    def setSwitchOutput(self, v):
#         """
#          -o, --output arg (=out)    prefix of output
#         """
#         self.g3Iterated.set_param_at(v)

    def setInfileName(self, infile):
        """
        type anything here
        TODO: check valid infile, infile exist or not
        """
        self.glimmer.set_param_at(infile, 1)


    def setOutputTag(self, outfile):
        """
        """
        self.glimmer.set_param_at(outfile, 2)

    def GenerateOutfileName(self, infile):
        """
        infile name
               testGlimmer.poiuyxcvbjkfastaaaasdfghjk
        step1: testGlimmer
        step2: testGlimmer_out.fasta
        step3: self.pdir+testGlimmer_out.fasta
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
        outfile=namebase+"_out"
        return outfile


    #Check whether infile exists:
    def checkInfileExist(self):
        """
         TODO: add code to check if these exist
         check if self.pdir exist
         check if infile exist
         check if outfile already exist

         use
         if os.path.exists( fileName ):
        """
        #        This chunk checks for a valid directory.
        print "Directory set to:",self.pdir
        if os.path.exists(self.pdir):
            print("Valid directory.")
        else:
        #            print
        #            sys.exit(-1)
            raise IOError, "Error: invalid directory:%s" %self.pdir
        #        If the directory is valid, this chunk makes sure the infile exists.
#        self.infile_path="%s%s" % (self.pdir, self.infile_class_var)
#        print "Infile path set to:",self.infile_path

        if self.check_outfile_existence( "", self.infile_class_var, True):
            print "Infile exists."
        else:

            raise IOError("Error: infile does not exist. %s%s"%(self.pdir, self.infile_class_var))
        #        This chunk makes sure you won't overwrite an existing outfile.
        self.outfile_path="%s%s" % (self.pdir, self.outfileTag)

        isExist = self.checkG3OutfilesExist()
#        print "zzzzzzzzz:",    isExist

        if isExist:
#        os.path.exists(self.outfile_path):
            raise IOError("WARNING: outfile already exists!!!")
            #TODO: come back to this later.
        #            Can rename the file, raise a different error, etc.
        else:
            pass


    def checkG3OutfilesExist(self):

        allextw=[".coords", ".detail", ".icm", ".longorfs", ".motif", ".predict", ".run1.detail", ".run1.predict", ".train", ".upstream"]
        isExist = self.check_multiple_outfiles_existence( self.outfileTag, allextw)
        return isExist




    def check_multiple_outfiles_existence(self, outfileTag, allext, isExist=True):
        for ext in allext:
            isExist = self.check_outfile_existence( outfileTag, ext, isExist)
        return isExist


    def check_outfile_existence(self, filetag, ext, isExist):

        test_outfile=filetag + ext
        print ext," file:",test_outfile
        test_outfile="%s%s" % (self.pdir, test_outfile)
        print "*",ext," file:",test_outfile
        if os.path.exists(test_outfile):
            print ext,"  outfile exists."
            isExist=isExist and True
        else:
            isExist=False
            print "Error: ",ext,"  outfile does not exist."

        return isExist


    #Check for expected output files:
    def checkG3OutfilesExistOld2(self):
        """
        TODO: check if standard outfile from ./assemble exist

        start with self.infile_class_var (test_infile.fasta)
        should have 10 output
            test_infile.fasta.coords
            test_infile.fasta.detail
            test_infile.fasta.icm
            test_infile.fasta.longorfs
            test_infile.fasta.motif
            test_infile.fasta.predict
            test_infile.fasta.run1.detail
            test_infile.fasta.run1.predict
            test_infile.fasta.train
            test_infile.fasta.upstream

        ./assemble_linux test_infile.fasta 1
        still generate test_infile.fasta.status

        check
        *.coords
        *.detail
        *.icm
        *.longorfs
        *.motif
        *.preict
        *.run1.detail
        *.run1.predict
        *.train
        *.upstream
        exist

        if os.path.exists( fileName ):
        """
        
#        isExist=True
#
#        isExist = self.check_outfile_existence( self.outfileTag, ".coords", isExist)
#        isExist = self.check_outfile_existence( self.outfileTag, ".detail", isExist)
#        isExist = self.check_outfile_existence( self.outfileTag, ".icm", isExist)
#        isExist = self.check_outfile_existence( self.outfileTag, ".longorfs", isExist)
#        isExist = self.check_outfile_existence( self.outfileTag, ".motif", isExist)
#        isExist = self.check_outfile_existence( self.outfileTag, ".predict", isExist)
#        isExist = self.check_outfile_existence( self.outfileTag, ".run1.detail", isExist)
#        isExist = self.check_outfile_existence( self.outfileTag, ".run1.predict", isExist)
#        isExist = self.check_outfile_existence( self.outfileTag, ".train", isExist)
#        isExist = self.check_outfile_existence( self.outfileTag, ".upstream", isExist)
#        return isExist

    
    
    #Check for expected output files:
    def checkG3OutfilesExistOld(self):
        """
        TODO: check if standard outfile from ./assemble exist

        start with self.infile_class_var (test_infile.fasta)
        should have 10 output
            test_infile.fasta.coords
            test_infile.fasta.detail
            test_infile.fasta.icm
            test_infile.fasta.longorfs
            test_infile.fasta.motif
            test_infile.fasta.predict
            test_infile.fasta.run1.detail
            test_infile.fasta.run1.predict
            test_infile.fasta.train
            test_infile.fasta.upstream

        ./assemble_linux test_infile.fasta 1
        still generate test_infile.fasta.status

        check
        *.coords
        *.detail
        *.icm
        *.longorfs
        *.motif
        *.preict
        *.run1.detail
        *.run1.predict
        *.train
        *.upstream
        exist

        if os.path.exists( fileName ):
        """
        outfile = self.outfileTag
        isExist=False
        #        Check *.coords outfile:
        test_outfile=outfile+".coords"
        print "*.coords file:",test_outfile
        test_outfile="%s%s" % (self.pdir, test_outfile)
        print "*.coords file:",test_outfile
        if os.path.exists(test_outfile):
            print ".coords outfile exists."
            isExist=True

    #            Check *.detail outfile:
        test_outfile=outfile + ".detail"
        print "*.detail file:",test_outfile
        test_outfile="%s%s" % (self.pdir, test_outfile)
        print "*.detail file:",test_outfile
        if os.path.exists(test_outfile):
            print ".detail outfile exists."
            isExist=isExist and True
        else:
            isExist=False
            print "Error: *.detail outfile does not exist."

        #        Check *.icm outfile:
        icmOutfile=outfile + ".icm"
        print icmOutfile
        self.icmOutfile_path="%s%s" % (self.pdir, icmOutfile)
        if os.path.exists(self.icmOutfile_path):
            print ".icm outfile exists."
            isExist=isExist and True
        else:
            print "Error: *.icm outfile does not exist."
            isExist=False

            #        Check *.longorfs outfile:
        longorfsOutfile=outfile+".longorfs"
        print "*.longorfs file:",longorfsOutfile
        self.longorfsOutfile_path="%s%s" % (self.pdir, longorfsOutfile)
        if os.path.exists(self.longorfsOutfile_path):
            print ".longorfs outfile exists."
            isExist=isExist and True
        else:
            print "Error: *.longorfs outfile does not exist."
            isExist=False

        #            Check *.motif outfile:
        motifOutfile=outfile + ".motif"
        print "*.motif file:",motifOutfile
        self.motifOutfile_path="%s%s" % (self.pdir, motifOutfile)
        if os.path.exists(self.motifOutfile_path):
            print ".motif outfile exists."
            isExist=isExist and True
        else:
            isExist=False
            print "Error: *.motif outfile does not exist."

        #        Check *.predict outfile:
        predictOutfile=outfile + ".predict"
        print predictOutfile
        self.predictOutfile_path="%s%s" % (self.pdir, predictOutfile)
        if os.path.exists(self.predictOutfile_path):
            print ".predict outfile exists."
            isExist=isExist and True
        else:
            print "Error: *.predict outfile does not exist."
            isExist=False

            #        Check *.run1.detail outfile:
        run1detailOutfile=outfile+".run1.detail"
        print "*.run1.detail file:",run1detailOutfile
        self.run1detailOutfile_path="%s%s" % (self.pdir, run1detailOutfile)
        if os.path.exists(self.run1detailOutfile_path):
            print ".run1.detail outfile exists."
            isExist=isExist and True
        else:
            print "Error: *.run1.detail outfile does not exist."
            isExist=False

        #            Check *.run1.predict outfile:
        run1predictOutfile=outfile + ".run1.predict"
        print "*.run1.predict file:",run1predictOutfile
        self.run1predictOutfile_path="%s%s" % (self.pdir, run1predictOutfile)
        if os.path.exists(self.run1predictOutfile_path):
            print ".run1.predict outfile exists."
            isExist=isExist and True
        else:
            print "Error: *.run1.predict outfile does not exist."
            isExist=False


        #        Check *.train outfile:
        trainOutfile=outfile + ".train"
        print trainOutfile
        self.trainOutfile_path="%s%s" % (self.pdir, trainOutfile)
        if os.path.exists(self.trainOutfile_path):
            print ".train outfile exists."
            isExist=isExist and True
        else:
            print "Error: *.train outfile does not exist."
            isExist=False

        #        Check *.upstream outfile:
        upstreamOutfile=outfile + ".upstream"
        print upstreamOutfile
        self.upstreamOutfile_path="%s%s" % (self.pdir, upstreamOutfile)
        if os.path.exists(self.upstreamOutfile_path):
            print ".upstream outfile exists."
            isExist=isExist and True
        else:
            print "Error: *.upstream outfile does not exist."
            isExist=False


        #        isExist = None
        return isExist
