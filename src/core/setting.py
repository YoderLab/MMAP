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

        self.list_valid_param = ["parent_directory","genovo_infile","genovo_pdir","genovo_wdir","genovo_noI","genovo_thresh","genovo_outfile","glimmer_infile","glimmer_pdir","glimmer_wdir","glimmer_outfile"]
#        TODO set "_glimmer_infile"="genovo_outfile" and "genovo_wdir"="glimmer_wdir"
        self.list_essential_shared = ["parent_directory"]
        self.list_essential_genovo = ["genovo_infile","genovo_pdir","genovo_noI","genovo_thresh"]
        self.list_essential_glimmer = ["glimmer_pdir"] # dont need outfile
        self.list_optional_genovo = ["wdir","genovo_outfile","checkExist"]
        self.list_optional_glimmer = ["glimmer_infile","wdir","glimmer_outfile","checkExist"]
        self.list_ess_par = {
            "list_genovo":self.list_essential_genovo,
            "list_glimmer":self.list_essential_glimmer
        }

        self.list_optional_par = {
            "list_genovo":self.list_optional_genovo,
            "list_glimmer":self.list_optional_glimmer
        }
        self.add_all(**kwargs)


    def add(self, k, v):
        self.all_setting[k]=v

    def print_all(self):
        print "all_keys", self.all_setting.keys()
        for k in self.all_setting.iterkeys():
            print "key = %s, value = %s" %(k, self.all_setting[k])

    def get(self, key):
        return self.all_setting[key]

    def get_all_par(self, program_name):
        print "inside get_all_par\t", program_name
        is_all_exist =  self.check(self.list_ess_par[program_name])

        if is_all_exist:
            print "asdfghjk not working"

        else:
            print "not alll key exist"
        #            raise ValueError("not alll key exist")
        return self.all_setting

    def get_genovo(self):
        is_all_exist =  self.check(self.list_essential_genovo)

        if is_all_exist:
            print "asdfghjk"
            for c in self.list_optional_genovo:
                if not self.check([c]):
                    self.add(c, None)
        else:
            print "not alll key exist"
#            raise ValueError("not alll key exist")
        return self.all_setting

    def get_glimmer(self):
        is_all_exist =  self.check(self.list_essential_glimmer)

        if is_all_exist:
            print "asdfghjk"
            for c in self.list_optional_glimmer:
                if not self.check([c]):
                    self.add(c, None)
        else:
            print "not alll key exist"
        #            raise ValueError("not alll key exist")
        return self.all_setting
#
    def check(self, variable):
        for v in variable:
            print "check\t", v
            isExist = self.check_variables_exist(v)
            if isExist == False:
                return isExist

#            print "is_existr\t", isExist#, self.all_setting[variable])
        return True

#        return isExist



    def check_variables_exist(self, v):#, isExist=True):
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
