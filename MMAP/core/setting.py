import ConfigParser
import StringIO
import os

from core.amigo import go_connector
from core.component import run_genovo, run_MINE, run_glimmer, run_local_BLAST
from core.utils import path_utils
import sys
import glob


__author__ = 'erinmckenney'

list_essential_metasim_only = [
    "metasim_pdir", "metasim_model_infile", "metasim_taxon_infile", "metasim_no_reads"]
list_essential_genovo_only = ["genovo_pdir"]
list_essential_glimmer_only = ["glimmer_pdir"]  # dont need outfile
list_essential_blast_only = ["blast_pdir", "blast_db"]
list_essential_mine_only = ["mine_pdir", "mine_infile", "csv_files"]

list_all_essentials = []
# list_all_essentials.extend(list_essential_metasim_only)
list_all_essentials.extend(list_essential_genovo_only)
list_all_essentials.extend(list_essential_glimmer_only)
list_all_essentials.extend(list_essential_blast_only)
# list_all_essentials.extend(list_essential_mine_only)

list_optional_shared = ["check_exist"]
list_optional_metasim_only = ["metasim_outfile"]
list_optional_genovo_only = ["genovo_infile", "genovo_outfile", "genovo_noI", "genovo_thresh"]
list_optional_glimmer_only = ["glimmer_infile", "glimmer_outfile"]
list_optional_blast_only = [
    "blast_infile", "blast_batch_size", "blast_e_value", "blast_outfile",
    "blast_thread"
    ]
list_optional_mine_only = [
    "mine_comparison_style", "mine_cv", "mine_exp", "mine_clumps", "mine_jobID"]
list_optional_internal_only = ["master_tag"]

list_all_optionals = []
list_all_optionals.extend(list_optional_shared)
list_all_optionals.extend(list_optional_metasim_only)
list_all_optionals.extend(list_optional_genovo_only)
list_all_optionals.extend(list_optional_glimmer_only)
list_all_optionals.extend(list_optional_blast_only)
list_all_optionals.extend(list_optional_mine_only)


list_ess_par = {
    "metasim": list_essential_metasim_only,
    "genovo": list_essential_genovo_only,
    "glimmer": list_essential_glimmer_only,
    "blast": list_essential_blast_only,
    "mine": list_essential_mine_only,
    "all": list_all_essentials
}

list_optional_par = {
    "shared": list_optional_shared,
    "metasim": list_optional_metasim_only,
    "genovo": list_optional_genovo_only,
    "glimmer": list_optional_glimmer_only,
    "blast": list_optional_blast_only,
    "mine": list_optional_mine_only,
    "all": list_all_optionals
}
all_programs = ["genovo", "glimmer", "blast"]


def parse_control_file2(control_file):
    print("Parsing control file: %s" % control_file)
    config_parser = ConfigParser.SafeConfigParser()
    control_file = os.path.expanduser(os.path.expandvars(control_file))
#     print args.controlFile, os.path.expandvars(args.controlFile), config_file
#     with open(config_file) as cf:
# lines = "[config]" + "".join(cf.readlines());
#         lines = "[config]" + "".join(cf.read_all())
#         print lines
#         a = config_parser.readfp(lines)

    config = StringIO.StringIO()

    with open(control_file) as cf:
        inconf = cf.read()
        if not (inconf.find("[") is 0 and inconf.find("]") > 0):
            config.write('[Parameters]\n')


    config.write(inconf)
    config.seek(0, os.SEEK_SET)

    config_parser.readfp(config)
    all_arguments = dict()

    for s in config_parser.sections():
        #         print s, config_parser.items(s)
        for kv in config_parser.items(s):
            all_arguments[kv[0]] = kv[1]

#     print all_arguments
    return all_arguments


def parse_control_file(filepath):
    print("=Parsing control file: %s" % filepath)
    all_arguments = dict()
    infile = open(filepath)
    for line in infile:
        line = line.strip()
        if line.startswith("#") or line == "":
            pass
        else:
            location = line.find("=")
            key = line[0:location].strip()
            value = line[location + 1:len(line)].strip()
#            print line, "z", key, "z", value
            all_arguments[key] = value
    return all_arguments


class Setting(object):

    def __init__(self, run_mine=False, **kwargs):

        self.all_setting = dict()
        self.add_all(**kwargs)
#         self.debug = False
        self.run_mine = run_mine

    @classmethod
    def create_setting_from_file(cls, args):
        """
        TODO: switch between genovo+glimmer+blast and MINE

        ignore metasim for now
        do we need genovo+glimmer+blast+MINE?
        """
#         print type(args.control_file), dir(args.control_file)
#         print args.control_file.closed, args.control_file.name

        try:

            if args.control_file is "control":
                print "Use control file at ./control"
#                 args.control_file = "control"
            control_file = os.path.abspath(args.control_file)

            path_utils.check_file(control_file)
            all_pars = parse_control_file2(control_file)

            if args.sub_command == "process":
                print "Subcommand: process"
                infile = os.path.abspath(args.infile)
                wdir = os.path.dirname(infile)

                path_utils.check_file(infile)
                path_utils.check_directory(wdir)
                setting = cls(wdir=wdir)

                genovo_pdir_full = os.path.abspath(os.path.expanduser(all_pars["genovo_pdir"]))
                glimmer_pdir_full = os.path.abspath(os.path.expanduser(all_pars["glimmer_pdir"]))
                blast_pdir_full = os.path.abspath(os.path.expanduser(all_pars["blast_pdir"]))
                blast_db_full = os.path.abspath(os.path.expanduser(all_pars["blast_db"]))

                path_utils.check_directory(genovo_pdir_full)
                path_utils.check_directory(glimmer_pdir_full)
                path_utils.check_directory(blast_pdir_full)
    #                 path_utils.check_directory(blast_db_full)

                setting.add_all(
                    genovo_infile=infile,
                    genovo_pdir=genovo_pdir_full,
                    glimmer_pdir=glimmer_pdir_full,
                    blast_pdir=blast_pdir_full,
                    blast_db=blast_db_full
                )
                setting.check_parameters_program("genovo")
                setting.check_parameters_program("glimmer")
                setting.check_parameters_program("blast")

                setting._set_master_file_tag()

            elif args.sub_command == "summary":
                print "Subcommand: summary "
                csv_dir = os.path.abspath(args.csv_dir)  # wdir
                path_utils.check_directory(csv_dir)
                wdir = csv_dir

                setting = cls(wdir=wdir, run_mine=True)
                mine_pdir_full = os.path.abspath(os.path.expanduser(all_pars["mine_pdir"]))
#                 infile = path_utils.check_wdir_prefix(all_pars["wdir"], )

                infile = setting.generate_default_outfile_name(args.mine_infile, ".csv")
                infile = os.path.abspath(infile)  # #FIXME, should be able to do it better

                csv_list = []
                for name in glob.glob(wdir + '/*.csv'):
                    if name.find(args.mine_infile) > 0:
                        continue
                    if name.find("Results.csv") > 0 :
                        continue
                    if name.find("tmp.csv") > 0 :
                        continue
                    print "Found CSV file: ", name
                    csv_list.append(name)

                print "Total: %d CSV files in %s.\nPlease remove unwanted *.csv file and restart." % (len(csv_list), wdir)

                setting.add_all(
                    mine_pdir=mine_pdir_full,
                    mine_infile=infile,
                    csv_files=csv_list,
                    mine_overwrite=args.mine_overwrite
                )
                setting.check_parameters_program("mine")

        except KeyError as e:
#             raise KeyError("Missing essential setting", e)
            print "ERROR: Missing essential setting %s in control file:%s" % (e, control_file)
            if args.debug > 1:
                raise
            sys.exit(5)

        except IOError as e:
            print e
            if args.debug > 1:
                raise

            sys.exit(6)


#        keys = controlfile.all_arguments.keys()
#        print keys
        for parameter in list_all_optionals:
            if parameter in all_pars.keys():
                if args.debug > 0:
                    print "ADDING: ", parameter, all_pars[parameter]
                setting.add(parameter, all_pars[parameter])


        setting.print_all(args.debug)
        return setting

    def add_all(self, **kwargs):
        for k in kwargs.iterkeys():
            self.all_setting[k] = kwargs[k]

    def add(self, key, value):
        self.all_setting[key] = value

    def _set(self, key, value):
        self.all_setting[key] = value

    def print_all(self, level=0):
        if level > 1:
            print "Setting Summary: all_keys:", self.all_setting.keys()
        if level > 0:
            for k in sorted(self.all_setting.iterkeys()):
                print "key = %s, value = %s" % (k, self.all_setting[k])

    def get(self, key):
        return self.all_setting[key]

    def check_parameters_program(self, program):
        self._check_essential_keys(program)
        self._check_all_optional_keys(program)
        return self.all_setting

    def check_all_essential_keys(self):
        for program in all_programs:
            self._check_essential_keys(program)
        self._set_master_file_tag()

    def _check_essential_keys(self, program_name):
        par = list_ess_par[program_name]
        for v in par:
            isExist = self._check_variables_exist(v)
            if not isExist:
                raise KeyError("key does not exist: %s" % v)
        if program_name is "mine":
#             print  self.get("csv_files")
#             list_csv = self.get("csv_files").split(",")
#             list_csv = [f.strip() for f in list_csv]
#             self._set("csv_files", list_csv)
            self._set("csv_files", self.get("csv_files"))

    def _check_all_optional_keys(self, program_name):
        """
        default glimmer_infile = genove_outfile
        default check_exist = Ture (not None)
        """
        optional = list_optional_par[program_name] + list_optional_shared
        for c in optional:

            if not self._check_variables_exist(c):
                self.add(c, None)

        if program_name in "genovo":

            outfile = self.generate_default_outfile_name(self.all_setting.get("genovo_infile"), run_genovo.DEFAULT_OUTFILE_EXT)
            self._replace_none_with_defalut("genovo_outfile", outfile)
            self._replace_none_with_defalut(
                "genovo_noI", run_genovo.DEFAULT_GENOVO_NO_ITER)
            self._replace_none_with_defalut(
                "genovo_thresh", run_genovo.DEFAULT_GENOVO_THRESH)

        if program_name is "glimmer":
            self._replace_none_with_defalut_par(
                "glimmer_infile", "genovo_outfile")

            outfile = self.generate_default_outfile_name(self.all_setting.get("glimmer_infile"), run_glimmer.DEFAULT_OUTFILE_EXT)
            self._replace_none_with_defalut("glimmer_outfile", outfile)
#            if self.all_setting("glimmer_outfile") is None:
# self.all_setting("glimmer_outfile") = self.get("master_tag") +
# ".output.glimmer"

        if program_name is "blast":
            self._replace_none_with_defalut_par(
                "blast_infile", "glimmer_outfile")

            outfile = self.generate_default_outfile_name(self.all_setting.get("blast_infile"), run_local_BLAST.DEFAULT_OUTFILE_EXT)
            self._replace_none_with_defalut("blast_outfile", outfile)

            self._replace_none_with_defalut(
                "blast_e_value", go_connector.DEFAULT_E_VALUE_CUT_OFF)
            self._replace_none_with_defalut(
                "blast_batch_size", go_connector.DEFAULT_BATCH_SIZE)
            self._replace_none_with_defalut(
                "blast_thread", 1)

        if program_name is "mine":

            self._replace_none_with_defalut(
                "mine_comparison_style", "-allPairs")
            self._replace_none_with_defalut("mine_cv", run_MINE.DEFAULT_CV)
            self._replace_none_with_defalut("mine_exp", run_MINE.DEFAULT_EXP)
            self._replace_none_with_defalut(
                "mine_clumps", run_MINE.DEFAULT_CLUMPS)
        self._replace_none_with_defalut("check_exist", True)

    def _replace_none_with_defalut(self, check_key, default_value):
        if self.get(check_key) is None:
            self._set(check_key, default_value)

    def _replace_none_with_defalut_par(self, check_key, default_par_key):
        if self.get(check_key) is None:
            self._set(check_key, self.get(default_par_key))


    def generate_default_outfile_name(self, infile, outfile_tag):

        prefix = path_utils.remove_ext(infile)
        outfile = prefix + outfile_tag
        outfile = path_utils.check_wdir_prefix(self.all_setting.get("wdir"), outfile)
        return outfile

#    def _check(self, variable):
#        for v in variable:
#            isExist = self._check_variables_exist(v)
#            if isExist == False:
#                if self.debug:
#                    print("==Error== %s doesn't exist" % v)
#                return isExist
#
#        return True

    def _check_variables_exist(self, v):
        for key in self.all_setting.iterkeys():
            if v == key:
                return True

        return False

    def _set_master_file_tag(self):
        name = self.get("genovo_infile")
        name = path_utils.remove_ext(name)
        self._set("master_tag", name)


"""
## out dated. UPDATE required
#list_essential_metasim_only
metasim_pdir:
metasim_model_infile:
metasim_taxon_infile:
metasim_no_reads:
#list_essential_genovo_only
genovo_infile:
genovo_pdir:
genovo_noI:
genovo_thresh:
#list_essential_glimmer_only
glimmer_pdir:
#list_essential_blast_only
blast_wdir:
#list_essential_mine_only
mine_pdir:
mine_comparison_style:
#list_optional_shared
wdir:
check_exist:
#list_optional_metasim_only
metasim_outfile:
#list_optional_genovo_only
genovo_outfile:
#list_optional_glimmer_only
glimmer_infile:
glimmer_outfile:

#list_optional_blast_only
blast_infile:
blast_e_value:
blast_outfile:
#list_optional_mine_only
mine_infile:
mine_cv:
mine_clumps:
mine_jobID:
"""


class FakeSecHead(object):

    def __init__(self, fp):
        self.fp = fp
        self.sechead = '[asection]\n'

    def readline(self):
        if self.sechead:
            try:
                return self.sechead
            finally:
                self.sechead = None
        else:
            return self.fp.readline()
# usage:
#
# cp = ConfigParser.SafeConfigParser()
# cp.readfp(FakeSecHead(open('my.props')))
# print cp.items('asection')
