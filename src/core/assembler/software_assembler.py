"""
Created on April 16, 2012

@author: Erin McKenney and Steven Wu
"""

from core.component.run_Genovo import RunGenovo
from core.component.run_glimmer import RunGlimmer
from core.setting import Setting
import os
from core.component.run_metaIDBA import RunMetaIDBA
from core.utils import path_utils

__author__ = 'erinmckenney'


class SoftwareAssembler(object):

    def __init__(self, **kwargs):

        """
        create the following:
        Genovo class object
        Glimmer class object

        in_geno
        out_ge == in_glim
        pdir_gen ~ pdit_gli

        out_gli
        """
        self.setting = Setting()
#        self.set_all_param(**kwargs)
#        self.setting.add("genovo_infile",infile)
#        self.setting.add("genovo_outfile",outfile)
#        self.setting.add("asdfghjp",pdir) == fail
#        self.setting.add("glimmer_outfile",outfile)

#    def set_param(self, **kwargs):
#        for k in kwargs.iterkeys():
#            self.setting.add(k,kwargs[k])
#        self.setting.add("genovo_outfile",outfile)
#        self.setting.add("parent_pdir",pdir)


    def set_all_param(self, **kwargs):
        self.setting.add_all(kwargs)

#        If we create a dictionary of all extensions associated with a program,
#       we can define a generic function to check outfiles --> reduce code
    def check_outfiles(self, program, pdir, namebase):

        """
        TODO: reuse code from Genovo
        """
        #create dict of outfile extensions for programs
        self.all_outfiles = dict()
        for program in self.all_outfiles():
            if os.path.exists(pdir+namebase+self.all_outfiles+ext):
                pass

    def add(self, program, ext):
        self.all_outfiles[program]=ext



    def init_program(self):
        self.setting.check()
        self.genovo_a = RunGenovo(infile=self.setting.get("genovo_infile"), outfile=self.setting.get("genovo_outfile"),
            pdir=self.setting.get("genovo_pdir"), noI=self.setting.get("noI"), thresh=self.setting.get("thresh"))
        self.glimmer_a = RunGlimmer(infile=self.setting.get("glimmer_infile"), outfile=self.setting.get("glimmer_outfile"), pdir=self.setting.get("glimmer_pdir"))
#        self.blast_a = RunBlast()

#        genovo = RunGenovo(infile=infile_var, outfile = outfile_var, pdir = self.data_dir, noI=10, thresh=100, checkExist=True)
        
#    glimmer = RunGlimmer(infile=infile_var, outfile = outfile_var, pdir = self.data_dir)

    def run(self):
        self.genovo_a.run()
#        check_outfiles(genovo_a)
#        self.glimmer_a.run()
#        check_outfiles(glimmer_a)
        if self.genovo_a.check_outfiles_exist(self.setting.get("genovo_outfile")) and  os.path.exists(self.genovo_a.readFinalizeOutfile.record_index):
                self.glimmer_a.run()
        if self.glimmer_a.check_outfiles_exist(self.setting.get("glimmer_outfile")):
            pass
#            self.blast_a.run()


    def example_only(self):
        infile_var = "wdir_all_reads.fa"
        self.data_dir = path_utils.get_data_dir()+"Genovo/"
        self.working_dir = path_utils.get_data_dir()+"Genovo/test_data/"        
        genovo_p = RunGenovo(infile_var, pdir=self.data_dir, wdir=self.working_dir,  noI=1, thresh=10)
        glimmer_p = RunGlimmer(infile_var, pdir=self.data_dir+"Q", checkExist=False)
        blast_p = RunMetaIDBA(infile_var)
        
        all_p = [genovo_p, glimmer_p, blast_p]
        for p in all_p:
            print "aa",p.wdir
            p.setInfileName("QWER")
        
    def example2(self):
        all = ["aoue", (9,8,7,6), [1,2,3], {"a":1,"b":2}]
        for i in all:
            print type(i),"\t", len(i), i
            
        for i in (1,2,3):
            print i, i+i
            
        for i in "aoeu":
            print i, i+i
            
        all = [AA(), BB(), CC(), DD(), EE(), FF()]
        for i in all:
            print type(i)
            i.run()
            


class AA(object):
    def __init__(self):
        pass
    def run(self):
        print "AA running"
        print "zzzzz"
        
class BB(object):
    def run(self):
        print "BB running"
        for i in range(3):
            print i
        
        
class CC(BB):
    d = [1,2]
    def run(self):
        print "CC running"
        CC.d.extend(CC.d)
        print CC.d
        
class DD(object):
    def run(self):
        print "DD running"
        
        
class EE(DD):
    pass
#    def run(self):
#        super(DD)
#        

class FF(DD):
    def run(self):
        print "FF running"
        super(FF, self).run()

a = SoftwareAssembler(a=1, b=2)
a.example2()
