import os

__author__ = 'erinmckenney'


class Setting(object):


    def __init__(self, **kwargs):
        """
        refactor to _all.setting

        """
        self.all_setting = dict()
#        self.add("parent_directory",pdir)
#        self.add("genovo_infile",infile)
#        self.add("genovo_noI",noI)
#        self.add("genovo_thresh",thresh)
#        self.add("genovo_outfile",outfile)
#        self.add("glimmer_infile","genovo_outfile")
#        self.add("glimmer_outfile",outfile)

#        self.list_valid_param = ["parent_directory","genovo_infile","genovo_pdir","genovo_wdir","genovo_noI","genovo_thresh","genovo_outfile","glimmer_infile","glimmer_pdir","glimmer_wdir","glimmer_outfile"]
#        TODO set "_glimmer_infile"="genovo_outfile" and "genovo_wdir"="glimmer_wdir"
        self.list_essential_shared = ["parent_directory"]
        self.list_essential_genovo_only = ["genovo_infile","genovo_pdir","genovo_noI","genovo_thresh"]
        self.list_essential_glimmer_only = ["glimmer_pdir"] # dont need outfile
        self.list_optional_shared = ["wdir", "checkExist"]
        self.list_optional_genovo_only = ["genovo_outfile",]
        self.list_optional_glimmer_only = ["glimmer_infile","glimmer_outfile"]
        self.list_ess_par = {
            "shared":self.list_essential_shared,
            "genovo":self.list_essential_genovo_only,
            "glimmer":self.list_essential_glimmer_only
        }

        self.list_optional_par = {
            "shared":self.list_optional_shared,
            "genovo":self.list_optional_genovo_only,
            "glimmer":self.list_optional_glimmer_only
        }
        self.add_all(**kwargs)


    def add(self, key, value):
        self.all_setting[key]=value

    def print_all(self):
        print "all_keys", self.all_setting.keys()
        for k in self.all_setting.iterkeys():
            print "key = %s, value = %s" %(k, self.all_setting[k])

    def get(self, key):
        return self.all_setting[key]

    def get_all_par(self, program_name):
        print "inside get_all_par\t", program_name
        is_all_exist =  self._check(self.list_ess_par[program_name]) and self._check(self.list_ess_par["shared"])
        optional = [self.list_optional_par[program_name,"shared"]]
        if is_all_exist:
            print "inside optional loop"
            for c in optional:
                if not self._check([c]):
                    self.add(c, None)
        else:
            raise KeyError("not all key exist")
        return self.all_setting

    def get_genovo(self):
        print("\n ** in setting.get_genove() **")
        essential = [self.list_essential_genovo_only, self.list_essential_shared ]
        print("list_essential_only:\t%s" %self.list_essential_genovo_only)
        print("list_essential_shared:\t%s" %self.list_essential_shared)
        print("essential variable:\t%s" %essential)
        
        # test each for loop explicitly
#        for v in self.list_essential_genovo_only:
#            print("print each par in genovo_only:\t%s" %v)
#        for v in self.list_essential_shared:
#            print("print each par in shared_only:\t%s" %v)
#        for v in essential:
#            print("print each par in essential:\t%s" %v)
        
        
        is_all_exist =  self._check(essential)
        optional = [self.list_optional_genovo_only, self.list_optional_shared]
        if is_all_exist:
            for c in optional:
                print "checking optional parameter\t", c
                if not self._check([c]):
                    self.add(c, None)
        else:
            print "passed loop"
            raise KeyError("not all key exist")
        return self.all_setting

    def get_glimmer(self):
        is_all_exist =  self._check(self.list_essential_glimmer_only) and self._check(self.list_essential_shared)
        self.all_setting["glimmer_infile"] = self.all_setting["genovo_outfile"]
        optional = [self.list_optional_glimmer_only, self.list_optional_shared]
        if is_all_exist:
#            print "asdfghjk"
            for c in optional:
                if not self._check([c]):
                    self.add(c, None)
        else:
#            print "not alll key exist"
            raise KeyError("not all key exist")
        return self.all_setting
#
    def _check(self, variable):
        print("\n **in setting._check()**\n variable: %s" %variable)
        for v in variable:
            print("check each v inside for loop\t%s" %v)
            isExist = self._check_variables_exist(v)
            if isExist == False:
                return isExist

#            print "is_existr\t", isExist#, self.all_setting[variable])
        return True

#        return isExist



    def _check_variables_exist(self, v):#, isExist=True):
        for key in self.all_setting.iterkeys():
#            print "matching keys\t", key
            if v==key:
                return True
#            else:
#                return False
#        print "end checking"
        return False

#        isExist = self.all_setting[v]
#        all_params = [self.list_valid_param, self.list_essential_param]
#        for parameter in self.list_essential_genovo:
#            isExist = self.check(parameter, all_params, isExist)
#                isExist=isExist and True

    def add_all(self, **kwargs):
        for k in kwargs.iterkeys():
            self.all_setting[k] = kwargs[k]
