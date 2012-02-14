"""
Created on Feb 1, 2012

@author: Steven Wu
"""

from core.run_ext_prog import runExtProg
from Bio import SeqIO

class RunMetaIDBA(object):
    """
    classdocs
    """


    def __init__(self, infile, outfile=None, pdir=None):
        """
        Constructor
        """
        self.pdir = pdir
        self.infile = infile
        self.outfile = outfile
        self.metaIDBA = runExtProg("./metaidba", pdir=self.pdir)
        self.setSwitchRead(self.infile)
        self.setSwitchOutput(self.outfile)
        

        
#    def setSwitch(self, switch):
#        self.metaIDBA.get_switch(switch)

    def run(self):
        self.metaIDBA.run()
    
    def readContig(self, outfile=None):
        """
        TODO: add parse record method
        """
        if outfile is None:
            outfile = self.pdir+self.outfile
        
        self.record = SeqIO.index(outfile+"-contig.fa","fasta")
    
    def getRecord(self):
        return self.record
    
    
    def getSwitch(self):
        return self.metaIDBA.get_switch()


    def setSwitchRead(self, v):
        """
          -r, --read arg         read file
        """
        self.metaIDBA.updateSwitch("--read", v)     
        
    def setSwitchOutput(self, v):
        """
          -o, --output arg (=out)    prefix of output
        """
        self.metaIDBA.updateSwitch("--output", v)     
        
    def setSwitchMinK(self, v): 
        """
        --mink arg (=25)      minimum k value
        """   
        self.metaIDBA.updateSwitch("--mink", v)       
    
    def setSwitchMaxK(self, v):   
        """
        --maxk arg (=50)      maximum k value
        """ 
        self.metaIDBA.updateSwitch("--maxk", v)

    def setSwitchMinCount(self, v):    
        """
        --minCount arg (=2)    filtering threshold for each k-mer
        """
        self.metaIDBA.updateSwitch("--minCount", v)

    def setSwitchCover(self, v):    
        """
        --cover arg (=0)      the cutting coverage for contigs
        """
        self.metaIDBA.updateSwitch("--cover", v)

    def setSwitchMinPairs(self, v):  
        """
        --minPairs arg (=5)  minimum number of pair-end connections to join two components
        """  
        self.metaIDBA.updateSwitch("--minPairs", v)
        
    def setSwitchPrefixLength(self, v):    
        """
        --prefixLength arg (=3)  length of the prefix of k-mer used to split k-mer table
        """
        self.metaIDBA.updateSwitch("--prefixLength", v)
        
    def setToggleConnect(self, v=None):
        """ 
        #    --connect         use paired-end reads to connect components
        #    
        """
        self.metaIDBA.toggleSwitch("--connect", v)           
    

    def addSwitch(self, switch):
        self.metaIDBA.add_switch(switch)

    



