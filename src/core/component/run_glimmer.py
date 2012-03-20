"""
Created on March 19, 2012

@author: Erin McKenney
"""


class RunGlimmer(object):
    """
    classdocs
    """


    def __init__(self, infile, outfile=None, pdir=None):
        """
        Constructor
        """
        self.pdir = pdir
        self.infile = infile
        if outfile is None:
            self.outfile = infile

        self.g3Iterated = runExtProg("./g3_iterated.csh", pdir=self.pdir)
        self.setSwitchRead(self.infile)
        self.setSwitchOutput(self.outfile)

#    def getRecord(self):
#        return self.record

#    def getSwitch(self):
#        return self.glimmer._switch

    def setSwitchRead(self, v):
        """
          -r, --read arg         read file
        """
        self.g3Iterated.add_switch(v)
        self.finalize.set_param_at(v+".fasta")

    def setSwitchOutput(self, v):
         """
          -o, --output arg (=out)    prefix of output
         """
         self.g3Iterated.set_param_at(v)