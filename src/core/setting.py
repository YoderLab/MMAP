__author__ = 'erinmckenney'


class Setting(object):


    def __init__(self):
        """
        refactor to _all.setting

        """
        self.all_setting = dict()
        self.all_setting.add("parent_directory",pdir)
        self.all_setting.add("genovo_infile",infile)
        self.all_setting.add("genovo_noI",noI)
        self.all_setting.add("genovo_thresh",thresh)
        self.all_setting.add("genovo_outfile",outfile)
        self.all_setting.add("glimmer_infile","genovo_outfile")
        self.all_setting.add("glimmer_outfile",outfile)

        self.list_valid_param["",""]

    def add(self, k, v):
        self.all_setting[k]=v

    def print_all(self):
        for k in self.all_setting.iterkeys():
            print "key = %s, value = %s" %(k, self.all_setting[k])

    def get(self, key):
        return self.all_setting[key]

    def check(self):
        pass

    def add_all(self, **kwargs):
        for k in kwargs.iterkeys():
            self.all_setting[k] = kwargs[k]
