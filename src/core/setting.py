from core.controlfile import ControlFile
from core.utils import path_utils
from core.utils.path_utils import check_wdir_prefix, check_program_dir
from core.amigo.go_connector import GOConnector
from core.amigo import go_connector
from core.component import run_genovo, run_MINE


__author__ = 'erinmckenney'
# infile, pdir, wdir, comparison, cv=0, c=15, outfile, check_exist=True
list_essential_shared = ["parent_directory", "wdir"]
# parent directory points to the program
# wdir points to the data,
# TODO: FIXME: these path should be able to take relative path with respect to the control file
list_essential_metasim_only = ["metasim_pdir", "metasim_model_infile", "metasim_taxon_infile", "metasim_no_reads"]
list_essential_genovo_only = ["genovo_infile", "genovo_pdir"]
list_essential_glimmer_only = ["glimmer_pdir"]  # dont need outfile
list_essential_blast_only = ["blast_pdir", "blast_db"]
list_essential_mine_only = ["mine_pdir", "mine_infile", "csv_files"]

list_all_essentials = []
list_all_essentials.extend(list_essential_shared)
# list_all_essentials.extend(list_essential_metasim_only)
list_all_essentials.extend(list_essential_genovo_only)
list_all_essentials.extend(list_essential_glimmer_only)
list_all_essentials.extend(list_essential_blast_only)
# list_all_essentials.extend(list_essential_mine_only)

list_optional_shared = ["checkExist"]
list_optional_metasim_only = ["metasim_outfile"]
list_optional_genovo_only = ["genovo_outfile", "genovo_noI", "genovo_thresh"]
list_optional_glimmer_only = ["glimmer_infile", "glimmer_outfile"]
list_optional_blast_only = ["blast_infile", "blast_batch_size", "blast_e_value", "blast_outfile"]
list_optional_mine_only = [ "mine_comparison_style", "mine_cv", "mine_exp", "mine_clumps", "mine_jobID"]
list_optional_internal_only = ["master_tag"]

list_all_optionals = []
list_all_optionals.extend(list_optional_shared)
list_all_optionals.extend(list_optional_metasim_only)
list_all_optionals.extend(list_optional_genovo_only)
list_all_optionals.extend(list_optional_glimmer_only)
list_all_optionals.extend(list_optional_blast_only)
list_all_optionals.extend(list_optional_mine_only)

list_all_ggm = []
list_all_ggm.extend(list_essential_shared)
list_all_ggm.extend(list_essential_genovo_only)
list_all_ggm.extend(list_essential_glimmer_only)
list_all_ggm.extend(list_essential_blast_only)
list_all_ggm.extend(list_optional_shared)
list_all_ggm.extend(list_optional_genovo_only)
list_all_ggm.extend(list_optional_glimmer_only)
list_all_ggm.extend(list_optional_blast_only)
list_all_ggm.extend(list_optional_internal_only)

list_ess_par = {
    "shared": list_essential_shared,
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
        self.debug = False
        self.run_mine = False


    @classmethod
    def create_setting_from_file(cls, filepath):
        """
        # TODO: switch between
        genovo+glimmer+blast
        and
        MINE
        
        ignore metasim for now
        
        do we need genovo+glimmer+blast+MINE?

# FIXME: check filename name for wdir path before adding wdir to self.filename        
        """
        all_pars = parse_control_file(filepath)


        try:
            pdir = check_program_dir(all_pars["parent_directory"])
            wdir = check_program_dir(pdir, all_pars["wdir"])
            setting = cls(parent_directory=pdir, wdir=wdir)

            if all_pars.has_key("mine_pdir"):
                setting.run_mine = True
                setting.add_all(
                                mine_pdir=check_program_dir(pdir, all_pars["mine_pdir"]),
                                mine_infile=all_pars["mine_infile"],
                                csv_files=all_pars["csv_files"]
                                )
            else:
                setting.add_all(
                                genovo_infile=all_pars["genovo_infile"],
                                genovo_pdir=check_program_dir(pdir, all_pars["genovo_pdir"]),
                                glimmer_pdir=check_program_dir(pdir, all_pars["glimmer_pdir"]),
                                blast_pdir=check_program_dir(pdir, all_pars["blast_pdir"]),
                                blast_db=all_pars["blast_db"]
                                )
                setting._set_master_file_tag()

        except KeyError as err:
            raise KeyError("Missing essential setting", err)


#        keys = controlfile.all_arguments.keys()
#        print keys
        for parameter in list_all_optionals:
            if parameter in all_pars.keys():
                setting.add(parameter, all_pars[parameter])


            #            wdir=controlfile.get("wdir"),
#            checkExist=controlfile.get("checkExist"),
#            metasim_outfile=controlfile.get("metasim_outfile"),
#            genovo_outfile=controlfile.get("genovo_outfile"),
#            glimmer_infile=controlfile.get("glimmer_infile"),
#            glimmer_outfile=controlfile.get("glimmer_outfile"),

#            blast_infile=controlfile.get("blast_infile"),
#            blast_e_value=controlfile.get("blast_e_value"),
#            blast_outfile=controlfile.get("blast_outfile"),
#            mine_infile=controlfile.get("mine_infile"),
#            mine_cv=controlfile.get("mine_cv"),
#            mine_clumps=controlfile.get("mine_clumps"),
#            mine_jobID=controlfile.get("mine_jobID"))
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
        par = list_ess_par[program_name] + list_ess_par["shared"]
        for v in par:
            isExist = self._check_variables_exist(v)
            if isExist == False:
                raise KeyError("key does not exist: %s" % v)
        if program_name is "mine":
            list_csv = self.get("csv_files").split(",")
            list_csv = [f.strip() for f in list_csv]
            self._set("csv_files", list_csv)

    def _check_all_optional_keys(self, program_name):
        """
        default glimmer_infile = genove_outfile
        default checkExist = Ture (not None)
        """
        optional = list_optional_par[program_name] + list_optional_shared
        for c in optional:
            if self.debug:
                print ("checking %s" % c)
            if not self._check_variables_exist(c):
                self.add(c, None)

        if program_name in "genovo":
            self._replace_none_with_defalut("genovo_noI", run_genovo.DEFAULT_GENOVO_NO_ITER)
            self._replace_none_with_defalut("genovo_thresh", run_genovo.DEFAULT_GENOVO_THRESH)


        if program_name is "glimmer":
            self._replace_none_with_defalut_par("glimmer_infile", "genovo_outfile")
#            if self.all_setting("glimmer_outfile") is None:
#                self.all_setting("glimmer_outfile") = self.get("master_tag") + ".output.glimmer"

        if program_name is "blast":
            self._replace_none_with_defalut_par("blast_infile", "glimmer_outfile")
            self._replace_none_with_defalut("blast_e_value", go_connector.DEFAULT_E_VALUE_CUT_OFF)
            self._replace_none_with_defalut("blast_batch_size", go_connector.DEFAULT_BATCH_SIZE)

        if program_name is "mine":

            self._replace_none_with_defalut("mine_comparison_style", "-allPairs")
            self._replace_none_with_defalut("mine_cv", run_MINE.DEFAULT_CV)
            self._replace_none_with_defalut("mine_exp", run_MINE.DEFAULT_EXP)
            self._replace_none_with_defalut("mine_clumps", run_MINE.DEFAULT_CLUMPS)
        self._replace_none_with_defalut("checkExist", True)

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




