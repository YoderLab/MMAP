import ConfigParser
import StringIO
import os

from core.amigo import go_connector
from core.component import run_genovo, run_MINE
from core.utils import path_utils


__author__ = 'erinmckenney'

list_essential_metasim_only = [
    "metasim_pdir", "metasim_model_infile", "metasim_taxon_infile", "metasim_no_reads"]
list_essential_genovo_only = ["genovo_pdir"]
list_essential_glimmer_only = ["glimmer_pdir"]  # dont need outfile
list_essential_blast_only = []
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
    "blast_infile", "blast_batch_size", "blast_e_value", "blast_outfile"]
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
    print("Parsing control file: %s" % filepath)
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

    def __init__(self, **kwargs):

        self.all_setting = dict()
        self.add_all(**kwargs)
#         self.debug = False
        self.run_mine = False

    @classmethod
    def create_setting_from_file(cls, args):
        """
        TODO: switch between genovo+glimmer+blast and MINE

        ignore metasim for now
        do we need genovo+glimmer+blast+MINE?
        """
#         print type(args.control_file), dir(args.control_file)
#         print args.control_file.closed, args.control_file.name
        control_file = os.path.abspath(args.control_file)  # + "A"
        infile = os.path.abspath(args.infile)  # + "A"
        wdir = os.path.dirname(infile)

        try:
            path_utils.check_file(control_file)
            path_utils.check_file(infile)
            path_utils.check_directory(wdir)

            all_pars = parse_control_file2(control_file)
            setting = cls(wdir=wdir, genovo_infile=infile)

            if "mine_pdir" in all_pars:  # TODO fix MINE later
                setting.run_mine = True
                setting.add_all(
                    mine_pdir=os.path.abspath(all_pars["mine_pdir"]),
                    mine_infile=all_pars["mine_infile"],
                    csv_files=all_pars["csv_files"]
                )
            else:

                genovo_pdir_full = os.path.abspath(os.path.expanduser(all_pars["genovo_pdir"]))
                glimmer_pdir_full = os.path.abspath(os.path.expanduser(all_pars["glimmer_pdir"]))
                path_utils.check_directory(genovo_pdir_full)
                path_utils.check_directory(glimmer_pdir_full)

                setting.add_all(
                    genovo_pdir=genovo_pdir_full,
                    glimmer_pdir=glimmer_pdir_full
                )

                setting._set_master_file_tag()

        except KeyError as e:
#             raise KeyError("Missing essential setting", e)
            print "Missing essential setting %s" % e
            raise
        except IOError as e:
            print e
            raise


#        keys = controlfile.all_arguments.keys()
#        print keys
        for parameter in list_all_optionals:
            if parameter in all_pars.keys():
                setting.add(parameter, all_pars[parameter])

        for k, v in setting.all_setting.items():
            print k, v
        return setting

    def add_all(self, **kwargs):
        for k in kwargs.iterkeys():
            self.all_setting[k] = kwargs[k]

    def add(self, key, value):
        self.all_setting[key] = value

    def _set(self, key, value):
        self.all_setting[key] = value

    def print_all(self, level=0):
        print "all_keys", self.all_setting.keys()
        if level > 0:
            for k in sorted(self.all_setting.iterkeys()):
                print "key = %s, value = %s" % (k, self.all_setting[k])

    def get(self, key):
        return self.all_setting[key]

    def get_pars(self, program):
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
            list_csv = self.get("csv_files").split(",")
            list_csv = [f.strip() for f in list_csv]
            self._set("csv_files", list_csv)

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
            self._replace_none_with_defalut(
                "genovo_noI", run_genovo.DEFAULT_GENOVO_NO_ITER)
            self._replace_none_with_defalut(
                "genovo_thresh", run_genovo.DEFAULT_GENOVO_THRESH)

        if program_name is "glimmer":
            self._replace_none_with_defalut_par(
                "glimmer_infile", "genovo_outfile")
#            if self.all_setting("glimmer_outfile") is None:
# self.all_setting("glimmer_outfile") = self.get("master_tag") +
# ".output.glimmer"

        if program_name is "blast":
            self._replace_none_with_defalut_par(
                "blast_infile", "glimmer_outfile")
            self._replace_none_with_defalut(
                "blast_e_value", go_connector.DEFAULT_E_VALUE_CUT_OFF)
            self._replace_none_with_defalut(
                "blast_batch_size", go_connector.DEFAULT_BATCH_SIZE)

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
