
__author__ = 'erinmckenney'

list_essential_shared = ["parent_directory"]
list_essential_metasim_only = ["metasim_pdir","metasim_model_infile", "metasim_taxon_infile", "metasim_no_reads"]
list_essential_genovo_only = ["genovo_infile", "genovo_pdir", "genovo_noI", "genovo_thresh"]
list_essential_glimmer_only = ["glimmer_pdir"]  # dont need outfile
list_optional_metasim_only = ["metasim_outfile"]
list_optional_shared = ["wdir", "checkExist"]
list_optional_genovo_only = ["genovo_outfile", ]
list_optional_glimmer_only = ["glimmer_infile", "glimmer_outfile"]
list_ess_par = {
    "shared": list_essential_shared,
    "metasim": list_essential_metasim_only,
    "genovo": list_essential_genovo_only,
    "glimmer": list_essential_glimmer_only
}

list_optional_par = {
    "shared": list_optional_shared,
    "metasim": list_optional_metasim_only,
    "genovo": list_optional_genovo_only,
    "glimmer": list_optional_glimmer_only
}


class Setting(object):

    def __init__(self, **kwargs):
        """
        """
        self.all_setting = dict()
        self.add_all(**kwargs)

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
                if not self._check_variables_exist(c):
                    self.add(c, None)
        else:
            raise KeyError("not all key exist")

        if program_name is "glimmer":
            if self.all_setting["glimmer_infile"] is None:
                self.all_setting["glimmer_infile"] = self.all_setting["genovo_outfile"]

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


