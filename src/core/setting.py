
__author__ = 'erinmckenney'
#infile, pdir, wdir, comparison, cv=0, c=15, outfile, check_exist=True
list_essential_shared = ["parent_directory"]
list_essential_metasim_only = ["metasim_pdir", "metasim_model_infile", "metasim_taxon_infile", "metasim_no_reads"]
list_essential_genovo_only = ["genovo_infile", "genovo_pdir", "genovo_noI", "genovo_thresh"]
list_essential_glimmer_only = ["glimmer_pdir"]  # dont need outfile
list_essential_mine_only = [ "mine_pdir", "mine_comparison_style"]


list_optional_shared = ["wdir", "checkExist"]
list_optional_metasim_only = ["metasim_outfile"]
list_optional_genovo_only = ["genovo_outfile"]
list_optional_glimmer_only = ["glimmer_infile", "glimmer_outfile", "extract_outfile"]
list_optional_blast_only = ["blast_infile", "blast_e-value", "blast_outfile"]
list_optional_mine_only = ["mine_infile", "mine_cv", "mine_clumps", "mine_jobID"]

list_ess_par = {
    "shared": list_essential_shared,
    "metasim": list_essential_metasim_only,
    "genovo": list_essential_genovo_only,
    "glimmer": list_essential_glimmer_only,
    "mine": list_essential_mine_only
}

list_optional_par = {
    "shared": list_optional_shared,
    "metasim": list_optional_metasim_only,
    "genovo": list_optional_genovo_only,
    "glimmer": list_optional_glimmer_only,
    "mine": list_optional_mine_only
}


class Setting(object):

    def __init__(self, **kwargs):
        """
        """
        self.all_setting = dict()
        self.add_all(**kwargs)
        self.debug = False

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

#                TODO: once BLAST and GO code is integrated, set GO-term output = MINE infile

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
        is_all_exist = self._check(list_optional_blast_only + list_essential_shared)

        optional = list_optional_blast_only + list_optional_shared
        self.check_all_optional_parameter("blast", is_all_exist, optional)
        return self.all_setting

    def _get_mine(self):
        is_all_exist = self._check(list_essential_mine_only + list_essential_shared)

        optional = list_optional_mine_only + list_optional_shared
        self.check_all_optional_parameter("mine", is_all_exist, optional)

        return self.all_setting
