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


    def add_all_param(self, **kwargs):
        self.setting.add_all(**kwargs)


    def get_all_par(self):
        return self.setting.all_setting


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

    def _addRandom(self, program, ext):
        self.all_outfiles[program]=ext

    def update_genovo_setting(self):
        self.setting.add("genovo_outfile",self.genovo_a.outfile)


    def init_program(self):
#        self.setting.check()
        self.genovo_a = RunGenovo.create_genovo(self.setting.get_genovo())
        print self.setting.get_glimmer()
        self.update_genovo_setting()

        print self.setting.get_glimmer()
        self.glimmer_a = RunGlimmer.create_glimmer(self.setting.get_glimmer() )
#        self.blast_a = RunBlast()

#        genovo = RunGenovo(infile=infile_var, outfile = outfile_var, pdir = self.data_dir, noI=10, thresh=100, checkExist=True)



    def init_program2(self):
    #        self.setting.check()
        self.genovo_a = RunGenovo.create_genovo(self.setting.get_all_par("genovo"))
        print self.setting.get_glimmer()
        self.update_genovo_setting()

        print self.setting.get_glimmer()
        self.glimmer_a = RunGlimmer.create_glimmer(self.setting.get_all_par("glimmer"))
    #        self.blast_a = RunBlast()

    def init_program3(self):
    #        self.setting.check()
        self.genovo_a = RunGenovo.create_genovo2(self.setting)
        print self.setting.get_glimmer()
        self.update_genovo_setting()

        print self.setting.get_glimmer()
#        self.glimmer_a = RunGlimmer.create_glimmer2(self.setting)

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


