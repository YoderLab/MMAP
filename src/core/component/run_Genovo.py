"""
Created on Feb 29, 2012

@author: Erin McKenney and Steven Wu
"""
import sys

from core.run_ext_prog import runExtProg
from Bio import SeqIO
import os


class RunGenovo(object):
    """
    classdocs

    """

    
    
    def __init__(self, infile, noI, thresh, pdir, outfile=None, checkExist = True):
        """
        Constructor
        TODO: implement finalize
        TODO: read/parse/check output
        
        """
        self.pdir = pdir
        self.infile_class_var = infile
        ## TODO (Steven): use this to demonstrate refactor
        self.outfile = outfile
        if outfile is None:
            self.outfile = self.GenerateOutfileName(self.infile_class_var)

        if checkExist:
            self.checkInfileExist()
            
            
        self.assemble = runExtProg("./assemble", pdir=self.pdir, len=2, checkOS=True)
        self.finalize = runExtProg("./finalize", pdir=self.pdir, len=3)
        self.setInfileName(self.infile_class_var)
        self.setNumberOfIter(noI)
#        print self.assemble.get_switch()
#
#        self.testRandom()
        self.setFinalizeOutfile(self.outfile)
        self.setCutoff(thresh)


    def setNumberOfIter(self, param):
        """

        """

        if param>0 and isinstance( param, ( int, long ) ):
            self.assemble.set_param_at(param, 2)
        else:
            raise TypeError, "Error: unacceptable value for param: %s" %param



    def setInfileName(self, infile):
        """
        type anything here
        TODO: check valid infile, infile exist or not
        """
        self.assemble.set_param_at(infile, 1)
        self.finalize.set_param_at(infile+".dump.best",3)

    def testRandom(self):
#        print "test method"
        print self.infile_class_var
#        print infile

        print "end test method"


    def setFinalizeOutfile(self, outfile):
        """
        """
        self.finalize.set_param_at(outfile, 2)
    
    
    def setCutoff(self, v):
        """
        """
        if v>0 and isinstance(v, ( int, long ) ):
            self.finalize.set_param_at(v,1)
        else:
            if isinstance(v,str):
                print 'Error: cutoff set as string "%s"' %v
            else:
                print 'Error: cutoff set to:',v
            sys.exit(-1)


    def GenerateOutfileName(self, infile):
        """
        infile name
               testAssemble.poiuyxcvbjkfastaaaasdfghjk
        step1: testAssemble
        step2: testAssemble_out.fasta
        step3: self.pdir+testAssemble_out.fasta
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
        outfile=namebase+"_out.fasta"
        return outfile



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
            print "Valid directory."
        else:
            print "Error: invalid directory:",self.pdir
            sys.exit(-1)

#        If the directory is valid, this chunk makes sure the infile exists.
        self.infile_path="%s%s" % (self.pdir, self.infile_class_var)
        print "Infile path set to:",self.infile_path
        if os.path.exists(self.infile_path):
            print "Infile exists."
        else:
            print "Error: infile does not exist."

#        This chunk makes sure you won't overwrite an existing outfile.
        self.outfile_path="%s%s" % (self.pdir, self.outfile)
        if os.path.exists(self.outfile_path):
            print "WARNING: outfile already exists!!!"
        else:
            pass

    
    def checkAssembleResultExist(self):
        """
        TODO: check if standard outfile from ./assemble exist
        
        start with self.infile_class_var (test_infile.fasta)
        should have 3 output
            test_infile.fasta.status
            test_infile.fasta.dump1
            test_infile.fasta.dump.best
            
        ./assemble_linux test_infile.fasta 1
        still generate test_infile.fasta.status
        
        check 
        *.status
        *.dump1
        *.dump.best
        exist
        
        if os.path.exists( fileName ):
        """
        infile = self.infile_class_var
#        Check *.status outfile:
        statusOutfile=infile+".status"
        print "*.status file:",statusOutfile
        self.statusOutfile_path="%s%s" % (self.pdir, statusOutfile)
        if os.path.exists(self.statusOutfile_path):
            print ".status outfile exists."
        else:
            print "Error: *.status outfile does not exist."

#        Check *.dump1 outfile:
        dump1Outfile=infile + ".dump1"
        print "*.dump1 file:",dump1Outfile
        self.dump1Outfile_path="%s%s" % (self.pdir, dump1Outfile)
        if os.path.exists(self.dump1Outfile_path):
            print ".dump1 outfile exists."
        else:
            print "Error: *.dump1 outfile does not exist."

        #        Check *.dump.best outfile:
        dumpBestOutfile=infile + ".dump.best"
        print dumpBestOutfile
        self.dumpbestOutfile_path="%s%s" % (self.pdir, dumpBestOutfile)
        if os.path.exists(self.dumpbestOutfile_path):
            print ".dump.best outfile exists."
        else:
            print "Error: *.dump.best outfile does not exist."

#        isExist = None
#        return isExist
    

    
    def readFinalizeOutfile(self):
        """
        use SeqIO.index(file, "fast") to read the result seq file, generated from ./finalize
        TODO: check outfile exist, properly generated by ./finalize 
        """
        self.record_index = SeqIO.index("filename", "fasta")
        return self.record_index
    

#
#    def checkFileExist(self, file):
#        """
#        TODO: implement method, refactor example
#        """
#        isExist = False;
#        return isExist;
#
#    def run(self):
#        self.assemble.run()
#        self.finalize.run()
#

