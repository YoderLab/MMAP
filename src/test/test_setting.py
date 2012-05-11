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


    def test_Setting_get_genovo(self):
        setting = Setting()
        setting.add_all(genovo_infile="asdf", outfile="zxcv", genovo_thresh=2)
        setting.print_all()
        setting.get_genovo()
#        self.assertFalse(  )
#        print setting.get("genovo_outfile")
        setting = Setting()
        setting.add_all(genovo_infile="asdf", outfile="zxcv", genovo_noI=2)
#        setting.print_all()
        setting.get_genovo()
#        self.assertFalse(  )

        setting = Setting()
        setting.add_all(genovo_infile="asdf", genovo_thresh="zxcv", genovo_pdir="pdir", genovo_noI=2)
#        self.assertTrue(    )
        setting.get_genovo()
        setting.get("wdir")

        setting.get_all_par("list_genovo")

    def add_value(self, *arg):
#        self.ass
#        print "inside add_value"
        a= [0,0]
#        print type(arg)
#        for i in arg:
#            print a.append(i)

#        print "exit add_value"
        return a

#            (arg)
    foo = 9
    def test_example(self):
        print "example"
        foo = 3
        print "G", foo
#        global foo
#        foo=20
        print "G",TestSetting.foo
        
        print "== create class=="
        cVar = var()
        print "G",foo      
        print "C",cVar.foo
        print "S",var.foo

        print "== for loop== "
        for i in range(5):
            foo = i
            print foo

        global foo
        foo=20
        cVar.foo = 10
        print "== update class foo =="
        print "G",foo
        print "C",cVar.foo
        print "S",var.foo
        
        print "== update static foo =="
        var.foo = 30
        print "G",foo
        print "C",cVar.foo
        print "S",var.foo
        
        
    def test_example2(self):
        print "example2"
#        foo = 3
        print "G2", foo
#        global foo
#        foo=20
#        print "G",foo


        
        
                
        
foo = 2
foo=20
class var(object):
    foo = 1
    
    
    