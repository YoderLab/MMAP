"""
Created on March 19, 2012

@author: Erin McKenney
"""

from core.component.run_component import RunComponent
from core.run_ext_prog import runExtProg

GLIMMER = "./g3-iterated.csh"
EXTRACT = "./extract"
INFILE_POSITION = 1
TEMP_OUTFILE_TAG_POSITION = 2
COORDS_POSITION = 2
SYMBOL_POSITION = 3
OUTFILE_POSITION = 4

ALL_EXTS = [".coords", ".detail", ".icm", ".longorfs", ".motif",
            ".predict", ".run1.detail", ".run1.predict", ".train", ".upstream"]  # , ".orfs"]


class RunGlimmer(RunComponent):
    """
    classdocs
    """


    def __init__(self, infile, pdir, wdir=None, outfile=None, check_exist=True):
        """
        Constructor
        """
        # FIXME: check outfile name for wdir path before adding wdir to self.outfile
        self.all_exts = ALL_EXTS
        self.parameter_check(pdir, wdir, infile, outfile, check_exist, ".glimmer")
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
        setting = setting_class.get_pars("glimmer")
        glimmer = RunGlimmer.create_glimmer(setting)
        return glimmer

    def init_prog(self):

        self.set_infile_name(self.infile)
#        self.set_temp_outfile_tag(self.outfile)
        self.set_outfile(self.outfile)

#        coords_file = self.outfile + ".coords"
#        self.set_coords(coords_file)


    def set_infile_name(self, infile):
        self.glimmer.set_param_at(infile, INFILE_POSITION)
        self.extract.set_param_at(infile, INFILE_POSITION)


    def set_outfile(self, outfile):
        self.glimmer.set_param_at(outfile, TEMP_OUTFILE_TAG_POSITION)
        self.extract.set_param_at(outfile + ".coords", COORDS_POSITION)
        self.extract.set_param_at(" > ", SYMBOL_POSITION)
        self.extract.set_param_at(outfile, OUTFILE_POSITION)



    def run(self, debug=False):
        """
#    TODO: once outfiles are created, use terminal command to extract ORFs and pipe to fasta for BLAST
#        ./multi-extract tpall.fna iterated2.run1.predict > ~/Desktop/Pipeline/metaLem/data/Glimmer/mac/tpall_output.fasta
        """
        isComplete = self.check_outfiles_with_filetag_exist(self.outfile, debug=False) and self.is_file_exist(self.outfile, debug=False)
        if isComplete:
            print "===Warning!!! Glimmer outfiles already exist, skip Glimmer!!!==="
        else:

            print "Running Glimmer..."
            self.glimmer.run(debug)
            print "Running Glimmer extract..."
            self.extract.run(debug)

            filehandler = open(self.outfile, 'w')
            newLine = ""
            count = 0
    #        print self.extract.output

            for line in self.extract.output:
                if line.startswith(">"):
                    newLine += (line + str(count) + "_")
                    count += 1
                else:
                    newLine += line
            filehandler.write(newLine)
            filehandler.close()

        self._isCompleted()

    def _isCompleted(self):
        isComplete = self.check_outfiles_with_filetag_exist(self.outfile) and self.is_file_exist(self.outfile)
        if not isComplete:
            raise(StandardError("Glimmer did not complete, not all output files exist"))


    def get_extract_switch(self):
#        print "*****", self.extract._switch
        return self.extract._switch







