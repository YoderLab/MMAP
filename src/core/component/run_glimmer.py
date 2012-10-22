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
COORDS_POSITION = 2
SYMBOL_POSITION = 3
ORFS_POSITION = 4

ALL_EXTS = [".coords", ".detail", ".icm", ".longorfs", ".motif",
            ".predict", ".run1.detail", ".run1.predict", ".train", ".upstream", ".orfs"]


class RunGlimmer(RunComponent):
    """
    classdocs
    """


    def __init__(self, infile, pdir, wdir=None, outfile=None,  check_exist=True):
        """
        Constructor
        """
        self.all_exts = ALL_EXTS
        self.parameter_check(pdir, wdir, infile, outfile, check_exist, "_out")
        self.generate_orfs_name( )
        self.glimmer = runExtProg(GLIMMER, pdir=self.pdir, length=2, check_OS=True)
        self.extract = runExtProg(EXTRACT, pdir=self.pdir, length=4, check_OS=True)
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

    def init_prog(self):
        self.set_infile_name(self.infile)
        self.set_outfile_tag(self.outfile)
        self.set_coords(self.coords)
        self.set_orfs(self.orfs)

    def set_infile_name(self, infile):
        self.glimmer.set_param_at(infile, INFILE_POSITION)
        self.extract.set_param_at(infile, INFILE_POSITION)

    def set_outfile_tag(self, outfile):
        self.glimmer.set_param_at(outfile, OUTFILE_POSITION)

    def set_coords(self, file):
        self.extract.set_param_at(file, COORDS_POSITION)

    def set_orfs(self, file):
        self.extract.set_param_at(" > ", SYMBOL_POSITION)
        self.extract.set_param_at(file, ORFS_POSITION)

    def generate_orfs_name(self):
        """
        infile name
            check if it exist
            overwrite or not
        if os.path.exists(  self.cwd+self.name_only  ):
        if os.path.exists(  full_file_path  ):
        """

        location = self.outfile.rfind(".")
        if location is -1:
            namebase = self.outfile
        else:
            namebase = self.outfile[0:location]
        self.orfs = namebase + ".orfs"
        self.coords = namebase + ".coords"
#            print "!!!!!!", self.orfs


    def run(self, debug=False):
        self.glimmer.run(debug)

        """
#    TODO: once outfiles are created, use terminal command to extract ORFs and pipe to fasta for BLAST
#        ./multi-extract tpall.fna iterated2.run1.predict > ~/Desktop/Pipeline/metaLem/data/Glimmer/mac/tpall_output.fasta
        """
        self.extract.run(True)
        filehandler = open(self.orfs,'w')
        filehandler.write (self.extract.output)
        filehandler.close()

    def get_switch(self):
#        print "*****", self.extract._switch
        return self.extract._switch







