from core.setting import Setting

__author__ = 'erinmckenney'

import unittest
import random
#from ..src import sequence
from core.sequence import Sequence




class TestSetting(unittest.TestCase):

    def setUp(self):

        pass


    def tearDown(self):
        pass

#    @unittest.skip("demonstrating skipping")
    def test_Setting_set_param(self):
        setting = Setting()
        setting.add_all(infle="asdf", outfile="zxcv", noI=2)
        setting.print_all()

    def test_add_value(self):
        b=[1,2,3,4,5]
        print(b)
        b=self.add_value(1,2,3,4,5)
        print(b)

    def add_value(self, *arg):
        self.ass
        print "inside add_value"
        a= [0,0]
        print type(arg)
        for i in arg:
            print a.append(i)

        print "exit add_value"
        return a

#            (arg)