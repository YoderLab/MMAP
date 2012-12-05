"""
Created on June 6, 2012
@author: Erin McKenney
"""
from Bio import SeqIO
from core.component.run_component import RunComponent
from core.run_ext_prog import runExtProg
    # TODO: in Python we would have to type
    # >>>import xstats.MINE
    # How do we import the wrapper here? (Or do we need to at all?)

# Full command-line sequence will read as
# java -jar MINE.jar "infile" 'style' cv=## c=## <jobID>
    # style = '-allPairs', '-adjacentPairs', '-masterVariable i' '-onePair i j' <indexing starts with 0>
    # cv = % of records that must contain data for two variables to be compared <default = 0>
    # c = factor by which # of clumps may outnumber # of x-axis columns <default = 15>
    # notify = # of variable pairs to analyze before printing a status message as Status.csv output file <default = 100>
    # jobID = string to identify job
MINE = "java"# -jar MINE.jar" # MINE command call
offset = 2
INFILE_POSITION = 1 + offset
COMPARISON_STYLE_POSITION = 2 + offset
CV_THRESHOLD_POSITION = 3 + offset
CLUMPS_POSITION = 4 + offset
JOB_ID_POSITION = 5 + offset

ALL_EXTS = [",Results.csv", ",Status.txt"]

class RunMINE(RunComponent):
    """
    classdocs
    """

    def __init__(self, infile, pdir, jobID, wdir=None, comparison='-allPairs', cv=0, c=15, check_exist=True):
        """
        Constructor
        """
#        self.infile = wdir + infile
#        self.outfile = jobID
        if jobID is None:
            self.jobID = "out"
        else:
            self.jobID = jobID
        self.all_exts = ALL_EXTS
        self.parameter_check(pdir, wdir, infile, infile, check_exist, jobID)
#        if self.check_outfiles_with_filetag_exist(self.outfile) and check_exist:
#            raise IOError("Warning: outfiles exist!")
        self.mine = runExtProg(MINE, pdir=self.pdir, length=5 + offset , check_OS=True)
        self.mine.set_param_at("-jar", 1)
        self.mine.set_param_at("MINE.jar", 2)
        self.init_prog(comparison, cv, c)

#
#    @classmethod
#    def create_mine(cls, setting):
#        """
#        Class method
#        Create RunGlimmer from dict()
#        """
#        mine = cls(infile=setting.get("mine_infile"),
#            pdir=setting.get("mine_pdir"),
#            wdir=setting.get("wdir"),
#            comparison=setting.get("mine_comparison_style"),
#            cv=setting.get("mine_cv"),
#            c=setting.get("mine_clumps"),
#            jobID=setting.get("mine_outfile"),
#            check_exist=setting.get("check_exist"))
#        return mine

    @classmethod
    def create_mine_from_setting(cls, setting_class):
        """
        Class method
        Create RunMINE from Setting class
        """
        setting = setting_class.get_all_par("mine")
        mine = cls(infile=setting.get("mine_infile"),
            pdir=setting.get("mine_pdir"),
            wdir=setting.get("wdir"),
            comparison=setting.get("mine_comparison_style"),
            cv=setting.get("mine_cv"),
            c=setting.get("mine_clumps"),
            jobID=setting.get("mine_outfile"),
            check_exist=setting.get("check_exist"))
        return mine

    def init_prog(self, style, cv, c):
        self.set_infile_name(self.infile)
        self.set_outfile_tag()
        self.set_comparison_style(style)
        self.set_cv_threshold(cv)
        self.set_clumping_factor(c)
#
    def set_infile_name(self, infile):
        """
        type anything here
        TODO: check valid infile, infile exist or not
        """
        infile = "%s" % self.infile
        self.mine.set_param_at(infile, INFILE_POSITION)

    def set_comparison_style(self, style):
#        if set to acceptable parameter (3 choices),
        self.mine.set_param_at(style, COMPARISON_STYLE_POSITION)
#        else:
#           raise ValueError("Error: comparison style is currently set to invalid setting: %s. Must be set to -x, -y, or -z." % style

    def set_cv_threshold(self, c):
        v = self.check_valid_value(c, float)
            #
        if 1 > v >= 0 and isinstance(v, float):
            self.mine.set_param_at(v, CV_THRESHOLD_POSITION)
        else:
            raise ValueError("Error: cv value is set to : %s" % v)


    def set_clumping_factor(self, c):
        v = self.check_valid_value(c, int)
        if v > 0 and isinstance(v, (int, long)):
            self.mine.set_param_at(v, CLUMPS_POSITION)
        else:
            raise ValueError("Error: clumping factor set to : %s" % v)


    def set_outfile_tag(self):
        if self.jobID is None:
            self.jobID = "out"
        arg = "id=%s" % self.jobID
        self.mine.set_param_at(arg, JOB_ID_POSITION)

#def read_outfile(self):
#        """
#        ** Not sure how to check this file-type.
#        """
#        self.record_index = SeqIO.index(self.outfile, "csv")
#        return self.record_index


    def run(self, debug=False):
        #TODO: Figure out how to run MINE using the Python wrapper... command in the README file is below--but how to incorporate?
#        import xstats.MINE
#        for a, b, scores in xstats.MINE.analyze_file("Spellman.csv", xstats.MINE.MASTER_VARIABLE, 0, cv = 0.7):
#            print a, b, scores
#        analyze_file (fn, method = None, master_variable = None, cv = 0.0, exp = 0.6, c = 15)
        self.mine.run(debug)

    def get_switch(self):
        return self.mine._switch
