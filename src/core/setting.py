
__author__ = 'erinmckenney'
#infile, pdir, wdir, comparison, cv=0, c=15, outfile, check_exist=True
list_essential_shared = ["parent_directory"]
list_essential_metasim_only = ["metasim_pdir", "metasim_model_infile", "metasim_taxon_infile", "metasim_no_reads"]
list_essential_genovo_only = ["genovo_infile", "genovo_pdir", "genovo_noI", "genovo_thresh"]
list_essential_glimmer_only = ["glimmer_pdir"]  # dont need outfile
list_essential_blast_only = ["blast_wdir"] #TODO: double-check whether this should be blast_pdir or wdir
list_essential_mine_only = [ "mine_pdir", "mine_comparison_style"]

list_all_essentials = []
list_all_essentials.extend(list_essential_shared)
list_all_essentials.extend(list_essential_metasim_only)
list_all_essentials.extend(list_essential_genovo_only)
list_all_essentials.extend(list_essential_glimmer_only)
list_all_essentials.extend(list_essential_blast_only)
list_all_essentials.extend(list_essential_mine_only)

list_optional_shared = ["wdir", "checkExist"]
list_optional_metasim_only = ["metasim_outfile"]
list_optional_genovo_only = ["genovo_outfile"]
list_optional_glimmer_only = ["glimmer_infile", "glimmer_outfile", "extract_outfile"]
list_optional_blast_only = ["blast_infile", "blast_e_value", "blast_outfile"]
list_optional_mine_only = ["mine_infile", "mine_cv", "mine_clumps", "mine_jobID"]

list_all_optionals = []
list_all_optionals.extend(list_optional_shared)
list_all_optionals.extend(list_optional_metasim_only)
list_all_optionals.extend(list_optional_genovo_only)
list_all_optionals.extend(list_optional_glimmer_only)
list_all_optionals.extend(list_optional_blast_only)
list_all_optionals.extend(list_optional_mine_only)


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
    "all" : list_all_optionals
}


class Setting(object):

    def __init__(self, **kwargs):
        """
        """
#        self.a = list_all_essentials2
#        self.b = list_all_essentials
        self.all_setting = dict()
        self.add_all(**kwargs)
        self.debug = False


    @classmethod
    def create_setting_from_controlfile(cls, controlfile):




        setting = cls(parent_directory=controlfile.get("parent_directory"),
            metasim_pdir=controlfile.get("metasim_pdir"),
            metasim_model_infile=controlfile.get("metasim_model_infile"),
            metasim_taxon_infile=controlfile.get("metasim_taxon_infile"),
            metasim_no_reads=controlfile.get("metasim_no_reads"),
            genovo_infile=controlfile.get("genovo_infile"),
            genovo_pdir=controlfile.get("genovo_pdir"),
            genovo_noI=controlfile.get("genovo_noI"),
            genovo_thresh=controlfile.get("genovo_thresh"),
            glimmer_pdir=controlfile.get("glimmer_pdir"),
            blast_wdir=controlfile.get("blast_wdir"),
            mine_pdir=controlfile.get("mine_pdir"),
            mine_comparison_style=controlfile.get("mine_comparison_style"))

        keys=controlfile.all_arguments.keys()
#        print keys
        for parameter in list_all_optionals:

            if parameter in keys:
                setting.add(parameter, controlfile.get(parameter))
#                print parameter


            #            wdir=controlfile.get("wdir"),
#            checkExist=controlfile.get("checkExist"),
#            metasim_outfile=controlfile.get("metasim_outfile"),
#            genovo_outfile=controlfile.get("genovo_outfile"),
#            glimmer_infile=controlfile.get("glimmer_infile"),
#            glimmer_outfile=controlfile.get("glimmer_outfile"),
#            extract_outfile=controlfile.get("extract_outfile"),
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

    def print_all(self):
        print "all_keys", self.all_setting.keys()
        for k in self.all_setting.iterkeys():
            print "key = %s, value = %s" % (k, self.all_setting[k])

    def get(self, key):
#        print "Q", key, type(key), self.all_setting[key]
        return self.all_setting[key]

    def check_all_optional_parameter(self, program_name, is_all_exist, optional):
        """
        default glimmer_infile = genove_outfile
        default checkExist = Ture (not None)
        """
        if is_all_exist:

            for c in optional:
                """
                TODO: error from raise, not here. 
                is_all_exist is a boolean, doesn't contain any info, 
                therefore we need to go one level above
                """
                if self.debug:
                    print ("checking %s" % c)
                if not self._check_variables_exist(c):
                    self.add(c, None)
        else:
            raise KeyError("not all key exist")

        if program_name is "glimmer":
            if self.all_setting["glimmer_infile"] is None:
                self.all_setting["glimmer_infile"] = self.all_setting["genovo_outfile"]

        if program_name is "blast":
            if self.all_setting["blast_infile"] is None:
                self.all_setting["blast_infile"] = self.all_setting["extract_outfile"]
            if self.all_setting["blast_e_value"] is None:
                self.all_setting["blast_e_value"] = "1e-15"

        if program_name is "mine":
            if self.all_setting["mine_infile"] is None:
                self.all_setting["mine_infile"] = self.all_setting["blast_outfile"]

        if self.all_setting["checkExist"] is None:
            self.all_setting["checkExist"] = True

    def get_all_par(self, program_name):
        is_all_exist = self._check(list_ess_par[program_name] + list_ess_par["shared"])
        optional = list_optional_par[program_name] + list_optional_par["shared"]
        self.check_all_optional_parameter(program_name, is_all_exist, optional)

        return self.all_setting

    def _check(self, variable):
        for v in variable:
            isExist = self._check_variables_exist(v)
            if isExist == False:
                if self.debug:
                    print("==Error== %s doesn't exist" % v)
                return isExist

        return True

    def _check_variables_exist(self, v):
        for key in self.all_setting.iterkeys():
            if v == key:
                return True

        return False

    def _get_metasim(self):
        is_all_exist = self._check(list_essential_metasim_only + list_essential_shared)

        optional = list_optional_metasim_only + list_optional_shared

        self.check_all_optional_parameter("metasim", is_all_exist, optional)

        return self.all_setting

    def _get_genovo(self):
        essential = list_essential_genovo_only + list_essential_shared
        is_all_exist = self._check(essential)

        optional = list_optional_genovo_only + list_optional_shared
        self.check_all_optional_parameter("genovo", is_all_exist, optional)

        return self.all_setting

    def _get_glimmer(self):
        is_all_exist = self._check(list_essential_glimmer_only + list_essential_shared)

        optional = list_optional_glimmer_only + list_optional_shared
        self.check_all_optional_parameter("glimmer", is_all_exist, optional)

        return self.all_setting

    def _get_blast(self):
        is_all_exist = self._check(list_essential_blast_only + list_essential_shared)

        optional = list_optional_blast_only + list_optional_shared
        self.check_all_optional_parameter("blast", is_all_exist, optional)
        return self.all_setting

    def _get_mine(self):
        is_all_exist = self._check(list_essential_mine_only + list_essential_shared)

        optional = list_optional_mine_only + list_optional_shared
        self.check_all_optional_parameter("mine", is_all_exist, optional)

        return self.all_setting
