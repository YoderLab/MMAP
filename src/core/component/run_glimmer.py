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




    @classmethod
    def create_glimmer(cls, setting):
    #        :"test_run_infile.fasta", = self.data_dir, :10,
        glimmer = cls(infile=setting.get("glimmer_infile"),
            pdir=setting.get("glimmer_pdir"), wdir=setting.get("wdir") ,outfile=setting.get("glimmer_outfile"),
            checkExist=setting.get("check_exist"))
        #        infile, noI, thresh, pdir, wdir=None, outfile=None, checkExist = True):
        #        """
        #        ["parent_directory","genovo_infile","genovo_pdir","genovo_noI","genovo_thresh","glimmer_pdir"] # dont need outfile
        #        self.add_all(**kwargs)
        return glimmer

    @classmethod
    def create_glimmer_from_setting(cls, setting_class):
    #        :"test_run_infile.fasta", = self.data_dir, :10,
        setting = setting_class.get_all_par("glimmer")
        glimmer = RunGlimmer.create_glimmer(setting)
        #        genovo = cls(infile=setting.get("genovo_infile"), noI=setting.get("genovo_noI"), thresh=setting.get("genovo_thresh"),
        #            pdir=setting.get("genovo_pdir"), wdir=setting.get("wdir") ,outfile=setting.get("genovo_outfile"),
        #            checkExist=setting.get("check_exist"))
        #        infile, noI, thresh, pdir, wdir=None, outfile=None, checkExist = True):
        #        """
        #        ["parent_directory","genovo_infile","genovo_pdir","genovo_noI","genovo_thresh","glimmer_pdir"] # dont need outfile
        #        self.add_all(**kwargs)
        return glimmer

    def run(self):
        self.glimmer.run()
#    def getRecord(self):
#        return self.record

    def get_switch(self):
        return self.glimmer._switch
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
