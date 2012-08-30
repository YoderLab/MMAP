"""
Created on March 19, 2012

@author: Erin McKenney
"""

from core.component.run_component import RunComponent
from core.run_ext_prog import runExtProg

GLIMMER = "./g3-iterated.csh"
EXTRACT = "./multi-extract"
INFILE_POSITION = 1
OUTFILE_POSITION = 2
ORF_POSITION = 3

ALL_EXTS = [".coords", ".detail", ".icm", ".longorfs", ".motif",
            ".predict", ".run1.detail", ".run1.predict", ".train", ".upstream"]


class RunGlimmer(RunComponent):
    """
    classdocs
    """


    def __init__(self, infile, pdir, wdir=None, outfile=None, orfs=None, check_exist=True):
        """
        Constructor
        """
        self.all_exts = ALL_EXTS
        self.parameter_check(pdir, wdir, infile, outfile, check_exist, "_out")
        self.glimmer = runExtProg(GLIMMER, pdir=self.pdir, length=2, check_OS=True)
        self.extract = runExtProg(EXTRACT, pdir=self.pdir, length=3, check_OS=True)
        self.init_prog()

    @classmethod
    def create_glimmer(cls, setting):
        """
        Class method
        Create RunGlimmer from dict()
        """
        glimmer = cls(infile=setting.get("glimmer_infile"),
                      pdir=setting.get("glimmer_pdir"),
                      wdir=setting.get("wdir"),
                      outfile=setting.get("glimmer_outfile"),
                      check_exist=setting.get("check_exist"))
        return glimmer

    @classmethod
    def create_glimmer_from_setting(cls, setting_class):
        """
        Class method
        Create RunGlimmer from Setting class
        """
        setting = setting_class.get_all_par("glimmer")
        glimmer = RunGlimmer.create_glimmer(setting)
        return glimmer

    @classmethod
    def create_extract(cls, setting):
        """
        Class method
        Create RunGlimmer from dict()
        """
        extract = cls(infile=setting.get("glimmer_infile"),
            pdir=setting.get("extract_pdir"),
            wdir=setting.get("wdir"),
            outfile=setting.get("glimmer_outfile"),     # Needs to be .run1.predict outfile
            orfs=setting.get("extract_outfile")
            check_exist=setting.get("check_exist"))
        return extract

    @classmethod
    def create_extract_from_setting(cls, setting_class):
        """
        Class method
        Create RunGlimmer from Setting class
        """
        setting = setting_class.get_all_par("extract")
        extract = RunExtract.create_extract(setting)
        return extract

    def init_prog(self):
        self.set_infile_name(self.infile)
        self.set_outfile_tag(self.outfile)

    def set_infile_name(self, infile):
        self.glimmer.set_param_at(infile, INFILE_POSITION)
        self.extract.set_param_at(infile, INFILE_POSITION)

def set_outfile_tag(self, outfile):
        self.glimmer.set_param_at(outfile, OUTFILE_POSITION)
        self.extract.set_param_at(outfile, OUTFILE_POSITION)

def run(self):
        self.glimmer.run()

    def get_switch(self):
        return self.glimmer._switch
        return self.extract._switch


        """
#    TODO: once outfiles are created, use terminal command to extract ORFs and pipe to fasta for BLAST
#        ./multi-extract tpall.fna iterated2.run1.predict > ~/Desktop/Pipeline/metaLem/data/Glimmer/mac/tpall_output.fasta
        """






