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
#        TODO set "glimmer_infile"="genovo_outfile" and "genovo_wdir"="glimmer_wdir"
        self.list_essential_param = ["parent_directory","genovo_infile","genovo_pdir","genovo_noI","genovo_thresh","glimmer_pdir"] # dont need outfile
        self.add_all(**kwargs)


    def add(self, k, v):
        self.all_setting[k]=v

    def print_all(self):
        for k in self.all_setting.iterkeys():
            print "key = %s, value = %s" %(k, self.all_setting[k])

    def get(self, key):
        return self.all_setting[key]

    def check(self,variable):
        isExist = self.check_variables_exist(variable, self.all_setting[variable])
        return isExist

    def check_variables_exist(self, parameter, all_params, isExist=True):
        all_params = [self.list_valid_param, self.list_essential_param]
        for parameter in all_params:
            isExist = self.check(parameter, all_params, isExist)
            if os.path.exists(parameter):
                isExist=isExist and True

    def add_all(self, **kwargs):
        for k in kwargs.iterkeys():
            self.all_setting[k] = kwargs[k]
