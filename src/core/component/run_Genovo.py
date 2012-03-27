"""
Created on Feb 29, 2012

@author: Erin McKenney and Steven Wu
"""
import sys

from core.run_ext_prog import runExtProg
from Bio import SeqIO


class RunGenovo(object):
    """
    classdocs

    """


    def __init__(self, infile, noI, thresh, outfile=None, pdir=None):
        """
        Constructor
        TODO: implement finalize
        TODO: read/parse/check output
        
        """
        self.pdir = pdir
        self.infile_class_var = infile
        self.outfile = outfile
        if outfile is None:
            self.outfile = self.GenerateOutfileName(self.infile_class_var)


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
        TODO(Erin): check for invalid number
        """

        if param>0 and isinstance( param, ( int, long ) ):
            self.assemble.set_param_at(param, 2)
        else:
            print "Error:", param
            sys.exit(-1)


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
        self.finalize.set_param_at(outfile+".fasta", 2)
    #
    def setCutoff(self, v):
        """
        """
        if v>0 and isinstance(v, ( int, long ) ):
            self.finalize.set_param_at(v,1)
        else:
            print "Error:", v
#            raise TypeError, "invalid argument %s" %v
            sys.exit(-1)
    """
    ignore after this
    """

    def GenerateOutfileName(self, infile):
        """
        infile name testAssemble.fasta
        step1: testAssemble
        step2: testAssemble_out.fasta
        step3: self.pdir+testAssemble_out.fasta
            check if it exist
            overwrite or not


        if os.path.exists(  self.cwd+self.name_only  ):
        if os.path.exists(  full_file_path  ):
        """
        return "out.test"



#    def setSwitch(self, switch):
#        self.assemble.get_switch(switch)
#        self.finalize.get_switch(switch)
#
#    def run(self):
#        self.assemble.run()
#        self.finalize.run()
#
#    def readContig(self, outfile=None):
#        if outfile is None:
#            outfile = self.pdir+self.outfile
#        self.record = SeqIO.index(outfile+"-contig.fa",'fasta')
#
#    def getRecord(self):
#        return self.record
#
#
#
#    def getSwitch(self):
#        return self.assemble._switch
#        return self.finalize._switch
#
#
#
#
#
#    def setIterations(self, v):
#        """
#        N       number of iterations for assembly
#        """
#        self.assemble.add_switch(v)
#        self.finalize.add_switch(v)
#
#
#
#    def setToggleConnect(self, v=None):
#        """
#        #    --connect         use paired-end reads to connect components
#        #
#        """
#        self.assemble.toggleSwitch("--connect", v)
#        self.finalize.toggleSwitch("--connect", v)
#
#
#    def addSwitch(self, switch):
#        self.assemble.add_switch(switch)
#        self.finalize.add_switch(switch)
#
#
#



