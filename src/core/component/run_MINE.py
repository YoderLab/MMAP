"""
Created on June 6, 2012
@author: Erin McKenney
"""
from Bio import SeqIO
from core.component.run_component import RunComponent
from core.run_ext_prog import runExtProg
import csv
import os
from core.component import run_component
from core.utils import path_utils
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
MINE = "java"  # -jar MINE.jar" # MINE command call
offset = 2
INFILE_POSITION = 1 + offset
COMPARISON_STYLE_POSITION = 2 + offset
CV_THRESHOLD_POSITION = 3 + offset
EXP_POSITION = 4 + offset
CLUMPS_POSITION = 5 + offset
JOB_ID_POSITION = 6 + offset

ALL_EXTS = [",Results.csv", ",Status.txt"]


DEFAULT_CV = 0.0
DEFAULT_EXP = 0.6
DEFAULT_CLUMPS = 15

class RunMINE(RunComponent):
    """
    classdocs
    """

    def __init__(self, infile, pdir, wdir, comparison='-allPairs',
                 cv=DEFAULT_CV, exp=DEFAULT_EXP, clumps=DEFAULT_CLUMPS,
                 jobID="out", check_exist=True,
                 csv_files=None):
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
        self.parameter_check(pdir, wdir, infile, infile, False, "")

        if not self.infile.endswith(".csv"):
            self.infile = self.infile + ".csv"
        self.outfile = self.infile + "," + self.jobID
        if self.check_outfiles_with_filetag_exist(self.outfile) and check_exist:
            raise IOError("Warning: outfiles exist!")

        self.mine = runExtProg(MINE, pdir=self.pdir, length=6 + offset, check_OS=True)
        self.mine.set_param_at("-jar", 1)
        self.mine.set_param_at("MINE.jar", 2)
        self.init_prog(comparison, cv, exp, clumps)

        self.csv_files = csv_files
        if self.csv_files is not None:
            for i, c in enumerate(self.csv_files):
                self.csv_files[i] = path_utils.check_wdir_prefix(self.wdir, c)
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
    def create_class_from_setting(cls, setting_class):
        """
        Class method
        Create RunMINE from Setting class
        """
        setting = setting_class.get_pars("mine")
        mine = cls(infile=setting.get("mine_infile"),
            pdir=setting.get("mine_pdir"),
            wdir=setting.get("wdir"),
            comparison=setting.get("mine_comparison_style"),
            cv=setting.get("mine_cv"),
            exp=setting.get("mine_exp"),
            c=setting.get("mine_clumps"),
            jobID=setting.get("mine_outfile"),
            csv_files=setting.get("csv_files"),
            check_exist=setting.get("check_exist"))
        return mine

    def init_prog(self, style, cv, exp, c):
        self.set_infile_name()
        self.set_comparison_style(style)
        self.set_cv_threshold(cv)
        self.set_exp(exp)
        self.set_clumping_factor(c)
        self.set_jobID()
#
    def set_infile_name(self):
        self.mine.set_param_at(self.infile, INFILE_POSITION)

    def set_comparison_style(self, style):
#        if set to acceptable parameter (3 choices),
        self.mine.set_param_at(style, COMPARISON_STYLE_POSITION)
#        else:
#           raise ValueError("Error: comparison style is currently set to invalid setting: %s. Must be set to -x, -y, or -z." % style

    def set_exp(self, exp):
        v = self.check_valid_value(exp, float)
        if v > 0 and isinstance(v, float):
            self.mine.set_param_at("exp=%s" % (v), EXP_POSITION)
        else:
            raise ValueError("Error: exp value is set to : %s" % v)


    def set_cv_threshold(self, c):
        v = self.check_valid_value(c, float)
        if 1 > v >= 0 and isinstance(v, float):
            self.mine.set_param_at("cv=%s" % (v), CV_THRESHOLD_POSITION)
        else:
            raise ValueError("Error: cv value is set to : %s" % v)


    def set_clumping_factor(self, c):
        v = self.check_valid_value(c, int)
        if v > 0 and isinstance(v, (int, long)):
            self.mine.set_param_at("c=%s" % (v), CLUMPS_POSITION)
        else:
            raise ValueError("Error: clumping factor set to : %s" % v)


    def set_jobID(self):
        arg = "id=%s" % self.jobID
        self.mine.set_param_at(arg, JOB_ID_POSITION)

# def read_outfile(self):
#        """
#        ** Not sure how to check this file-type.
#        """
#        self.record_index = SeqIO.index(self.outfile, "csv")
#        return self.record_index


    def run(self, debug=False):
        # TODO: Figure out how to run MINE using the Python wrapper... command in the README file is below--but how to incorporate?
#        import xstats.MINE
#        for a, b, scores in xstats.MINE.analyze_file("Spellman.csv", xstats.MINE.MASTER_VARIABLE, 0, cv = 0.7):
#            print a, b, scores
#        analyze_file (fn, method = None, master_variable = None, cv = 0.0, exp = 0.6, c = 15)
        if self.csv_files is not None:
            merge_output_csv_to_MINE(self.infile, self.csv_files, True)
        self.mine.run(debug)

    def get_switch(self):
        return self.mine._switch



def merge_output_csv_to_MINE(outfile, csv_files, isMINE=True):
    """
    csv_files = list of csv files
    """
    print "MINE: merging csv files to %s. From csv_list: %s" % (outfile, csv_files)
    header = []
    if not isMINE:
        header.append("GOterm")
    template = dict()
    for zeroes, infile in enumerate(csv_files):
        all_new_key = []
        with open(infile, 'rb') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                print row
                if i == 0:
#                        zeroes = len(row) - 1
                    index = row[1].rfind(os.sep) + 1
                    if index > -1:
                        row[1] = row[1][index:]
                    header.append("%s_%d" % (row[1], zeroes))
                else:
                    key = row[0]
                    all_new_key.append(key)
                    if key in template:
                        template[key].append(row[1])
                    else:
                        newlist = ([0] * zeroes)
                        newlist.append(row[1])
                        template[key] = newlist

            for key in template:
                if key not in all_new_key:
                    template[key].append(0)
    with open(outfile, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_NONE)
        writer.writerow(header)
        if isMINE:
            for row in template.values():
                writer.writerow(row)
        else:
            for key in template:
                temp = [key]
                temp.extend(template[key])
                writer.writerow(temp)
