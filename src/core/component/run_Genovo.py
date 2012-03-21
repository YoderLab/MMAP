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
        """
        self.pdir = pdir
        self.infile = infile
        if outfile is None:
            self.outfile = infile
#
        self.assemble = runExtProg("./assemble", pdir=self.pdir, len=2)
        self.finalize = runExtProg("./finalize", pdir=self.pdir, len=3)
        self.setSwitchRead(self.infile)
        self.setNumberOfIter(noI,2)
#

        self.setSwitchOutput(self.outfile)
        self.setCutoff(thresh)


    def setSwitch(self, switch):
        self.assemble.get_switch(switch)
        self.finalize.get_switch(switch)

    def run(self):
        self.assemble.run()
        self.finalize.run()
    
    def readContig(self, outfile=None):
        if outfile is None:
            outfile = self.pdir+self.outfile
        self.record = SeqIO.index(outfile+"-contig.fa","fasta")
    
    def getRecord(self):
        return self.record


    def setSwitchOutput(self, v):
        """
          -o, --output arg (=out)    prefix of output
        """
        self.finalize.set_param_at(v+".fasta", 2)

    def setCutoff(self, v):
        """
        $CUTOFF      minimum contig length
        """
        self.finalize.set_param_at(v,1)
    
    def getSwitch(self):
        return self.assemble._switch
        return self.finalize._switch


    def setSwitchRead(self, v):
        """
          -r, --read arg         read file
        """
        self.assemble.add_switch(v)
        self.finalize.set_param_at(v+"dump.best",3)

        

        
    def setIterations(self, v):
        """
        N       number of iterations for assembly
        """   
        self.assemble.add_switch(v)
        self.finalize.add_switch(v)
    


    def setToggleConnect(self, v=None):
        """ 
        #    --connect         use paired-end reads to connect components
        #    
        """
        self.assemble.toggleSwitch("--connect", v)
        self.finalize.toggleSwitch("--connect", v)
    

    def addSwitch(self, switch):
        self.assemble.add_switch(switch)
        self.finalize.add_switch(switch)

    def setNumberOfIter(self, param, position):
        self.assemble.set_param_at(param,position)


    



