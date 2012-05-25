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

    def __init__(self, infile, outfile=None, pdir="./"):
        """
        Constructor
        """
        self.pdir = pdir
        self.infile = infile
        self.outfile = outfile
        if self.outfile is None:
            self.outfile = infile

        self.metaIDBA = runExtProg("./metaidba", pdir=self.pdir)
        self.set_switch_read(self.infile)
        self.set_switch_output(self.outfile)

    def run(self):
        self.metaIDBA.run()
        self.outfile = self.pdir + self.outfile + "-contig.fa"

    def read_contig(self, outfile=None):
        if outfile is None:
            outfile = self.pdir + self.outfile + "-contig.fa"
        try:
            self.record = SeqIO.index(outfile, "fasta")
        except IOError as e:
            raise IOError("Exception error is: %s" % e)

    def get_record(self):
        return self.record

    def get_switch(self):
        return self.metaIDBA.get_switch()

    def set_switch_read(self, v):
        """
          -r, --read arg         read file
        """
        self.metaIDBA.updateSwitch("--read", v)

    def set_switch_output(self, v):
        """
          -o, --output arg (=out)    prefix of output
        """
        self.metaIDBA.updateSwitch("--output", v)

    def set_switch_min_k(self, v):
        """
        --mink arg (=25)      minimum k value
        """
        self.metaIDBA.updateSwitch("--mink", v)

    def set_switch_max_k(self, v):
        """
        --maxk arg (=50)      maximum k value
        """
        self.metaIDBA.updateSwitch("--maxk", v)

    def set_switch_min_count(self, v):
        """
        --minCount arg (=2)    filtering threshold for each k-mer
        """
        self.metaIDBA.updateSwitch("--minCount", v)

    def set_switch_cover(self, v):
        """
        --cover arg (=0)      the cutting coverage for contigs
        """
        self.metaIDBA.updateSwitch("--cover", v)

    def set_switch_min_pairs(self, v):
        """
        --minPairs arg (=5)  minimum number of pair-end connections
        to join two components
        """
        self.metaIDBA.updateSwitch("--minPairs", v)

    def set_switch_prefix_length(self, v):
        """
        --prefixLength arg (=3)  length of the prefix of k-mer used to
        split k-mer table
        """
        self.metaIDBA.updateSwitch("--prefixLength", v)

    def set_toggle_connect(self, v=None):
        """
        --connect         use paired-end reads to connect components
        """
        self.metaIDBA.toggleSwitch("--connect", v)

    def add_switch(self, switch):
        self.metaIDBA.add_switch(switch)



