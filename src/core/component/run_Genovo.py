"""
Created on Feb 29, 2012

@author: Erin McKenney and Steven Wu
"""

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
        if outfile is None:
            self.outfile = infile
#
        self.assemble = runExtProg("./assemble", pdir=self.pdir, len=2)
#        self.finalize = runExtProg("./finalize", pdir=self.pdir, len=3)
        self.setInfileName(self.infile_class_var)
        self.setNumberOfIter(noI)
#        print self.assemble.get_switch()
#
        self.testRandom()
#        self.setSwitchOutput(self.outfile)
#        self.setCutoff(thresh)


    def setNumberOfIter(self, param):
        """
        TODO(Erin): check for invalid number
        """
        self.assemble.set_param_at(param, 2)


    def setInfileName(self, infile):
        """
        type anything here
        TODO: check valid infile
        """
        self.assemble.set_param_at(infile, 1)
    #        self.finalize.set_param_at(v+"dump.best",3)

    def testRandom(self):
        print "test method"
        print self.infile_class_var
#        print infile

        print "end test method"


    """
    ignore after this
    """
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
#    def setSwitchOutput(self, v):
#        """
#          -o, --output arg (=out)    prefix of output
#        """
#        self.finalize.set_param_at(v+".fasta", 2)
#
#    def setCutoff(self, v):
#        """
#        $CUTOFF      minimum contig length
#        """
#        self.finalize.set_param_at(v,1)
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



