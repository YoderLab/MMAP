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


    def __init__(self, pdir, wdir, infile, outfile=None, check_exist=True):
        """
        Constructor
        """
        super(RunGlimmer, self).__init__(pdir, wdir, infile, check_exist)
        self.all_exts = ALL_EXTS
#         self.parameter_check(pdir, wdir, infile, outfile, check_exist, ".glimmer")
        self.outfile = self.check_outfile_filename(outfile, ".glimmer")

        self.glimmer = runExtProg(GLIMMER, pdir=self.pdir, length=2, check_OS=True)
        self.extract = runExtProg(EXTRACT, pdir=self.pdir, length=2, check_OS=True)
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
        self.extract.set_param_at(outfile + ".predict", COORDS_POSITION)
        # Capture by self.extract.output so won't be redirected
#         self.extract.set_param_at(" > ", SYMBOL_POSITION)
#         self.extract.set_param_at(outfile, OUTFILE_POSITION)


    def run(self, debug=False):
        """
#       once outfiles are created, use terminal command to extract ORFs and pipe to fasta for BLAST
#        ./multi-extract tpall.fna iterated2.predict > ~/Desktop/Pipeline/metaLem/data/Glimmer/mac/tpall_output.fasta
        """
        isComplete = self._isGlimmerCompleted(False) and self._isExtractCompleted(False)
        if isComplete:
            print "Warning!!! Glimmer outfiles already exist, skip Glimmer!!!"
        else:

            print "Running Glimmer..."
            self.glimmer.run(debug)
            self._isGlimmerCompleted(True)

            print "Running Glimmer extract..."
            self.extract.run(debug)

            newLine = ""
            count = 0
            for line in self.extract.output:
                if line.startswith(">"):
                    newLine += (line + str(count) + "_")
                    count += 1
                else:
                    newLine += line

            with open(self.outfile, 'w') as filehandler:
                filehandler.write(newLine)
                filehandler.close()

            self._isExtractCompleted(True)


    def _isGlimmerCompleted(self, is_raise_error=False):
        isComplete, missing_list = self.check_outfiles_with_filetag_exist(self.outfile, debug=is_raise_error)
        if is_raise_error and not isComplete:
            if len(missing_list) is 2 and self.outfile + ".predict" in missing_list and self.outfile + ".detail":
                raise(StandardError("Glimmer did not complete, *.glimmer.predict and *.glimmer.predict do NOT exit.\n"
                                    "Possible reason: Please check ELPH is install and set properly.\n"
                                    "Output Log: %s" % (self.glimmer.output)
                                    ))
            raise(StandardError("Glimmer did not complete, not all output files exist"))
        return isComplete

    def _isExtractCompleted(self, is_raise_error=False):
        isComplete = self.is_file_exist(self.outfile, debug=is_raise_error)
        if is_raise_error and not isComplete:
            raise(StandardError("Glimmer extract did not complete, *.glimmer does not exist"))
        return isComplete


    def get_all_switches(self):
        return (self.glimmer.get_all_switches(), self.extract.get_all_switches())







