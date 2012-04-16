__author__ = 'erinmckenney'


class Setting(object):


    def __init__(self):
        """
        refactor to _all.setting

        """
        self.all_setting = dict()
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
