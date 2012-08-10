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
MINE = "java -jar MINE.jar" # MINE command call
INFILE_POSITION = 1
COMPARISON_STYLE_POSITION = 2
CV_THRESHOLD_POSITION = 3
CLUMPS_POSITION = 4
JOB_ID_POSITION = 5

ALL_EXTS = ["Results.csv","Status.txt"]

class RunMINE(RunComponent):
    """
    classdocs
    """

    def __init__(self, infile, pdir, wdir, jobID, comparison='-allPairs', cv=0, c=15,  check_exist=True):
        """
        Constructor
        """
        self.infile = wdir+infile
        self.outfile = jobID
        self.all_exts = ALL_EXTS
        self.parameter_check(pdir, wdir, infile, self.outfile, check_exist,jobID)
        if self.check_outfiles_exist(self.outfile) and check_exist:
            raise IOError("Warning: outfiles exist!")
        self.mine = runExtProg(MINE, pdir=self.pdir, length=5, check_OS=True)
        self.init_prog(comparison, cv, c)


    @classmethod
    def create_mine(cls, setting):
        """
        Class method
        Create RunGlimmer from dict()
        """
        mine = cls(model_infile=setting.get("mine_infile"),
            pdir=setting.get("mine_pdir"),
            wdir=setting.get("wdir"),
            comparison=setting.get("mine_comparison_style"),
            cv=setting.get("mine_cv"),
            c=setting.get("mine_clumps"),
            jobID=setting.get("mine_outfile"),
            check_exist=setting.get("check_exist"))
        return mine

    @classmethod
    def create_mine_from_setting(cls, setting_class):
        """
        Class method
        Create RunMINE from Setting class
        """
        setting = setting_class.get_all_par("mine")
        mine = RunMINE.create_mine(setting)
        return mine

    def init_prog(self, style, cv, c):
        self.set_infile_name(self.infile)
        self.set_outfile_tag(self.outfile)
        self.set_comparison_style(style)
        self.set_cv_threshold(cv)
        self.set_clumping_factor(c)
#
    def set_infile_name(self, infile):
        """
        type anything here
        TODO: check valid infile, infile exist or not
        """
        infile = "%s" %self.infile
        self.mine.set_param_at(infile, INFILE_POSITION)

    def set_comparison_style(self, style):
#        if set to acceptable parameter (3 choices),
        self.mine.set_param_at(style, COMPARISON_STYLE_POSITION)
#        else:
#           raise ValueError("Error: comparison style is currently set to invalid setting: %s. Must be set to -x, -y, or -z." % style

    def set_cv_threshold(self, cv):
        if 1> cv >= 0 and isinstance(cv, float):
            self.mine.set_param_at(cv, CV_THRESHOLD_POSITION)
        else:
            if isinstance(cv, str):
                raise TypeError("Error: cv set as string: %s" % cv)
            else:
                raise ValueError("Error: unacceptable value for comparison threshold: %s" % cv)

    def set_clumping_factor(self, c):
        if c > 0 and isinstance(c, (int, long)):
            self.mine.set_param_at(c, CLUMPS_POSITION)
        else:
            if isinstance(c, str):
                raise TypeError("Error: clumping factor set as string: %s" % c)
            else:
                raise ValueError("Error: unacceptable value for clumping factor: %s" % c)

    def set_outfile_tag(self, jobID):
        self.mine.set_param_at(jobID, JOB_ID_POSITION)

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
