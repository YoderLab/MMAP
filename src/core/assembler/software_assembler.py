"""
Created on April 16, 2012

@author: Erin McKenney and Steven Wu
"""
from PIL.Scripts.explode import infile
from core.component.run_Genovo import RunGenovo
from core.component.run_glimmer import RunGlimmer
from core.setting import Setting
from traits.trait_types import self
import os

__author__ = 'erinmckenney'


class SoftwareAssembler(object):

    def __init__(self):

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
        self.setting.add("genovo_infile",infile)
        self.setting.add("genovo_outfile",outfile)
        self.setting.add("asdfghjp",pdir) == fail
        self.setting.add("glimmer_outfile",outfile)

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
        #create dict of outfile extensions for programs
        self.all_outfiles = dict()
        for program in self.all_outfiles():
            if.os.path.exists(pdir+namebase+self.all_outfiles.ext):
                pass

    def add(self, program, ext):
        self.all_outfiles[program]=ext



    def init_program(self):
        self.setting.check()
        self.genovo_a = RunGenovo(infile=self.setting.get("genovo_infile"), outfile, pdir, noI, thresh)
        self.glimmer_a = RunGlimmer(infile, outfile, pdir)
#        self.blast_a = RunBlast()

#        genovo = RunGenovo(infile=infile_var, outfile = outfile_var, pdir = self.data_dir, noI=10, thresh=100, checkExist=True)

#    glimmer = RunGlimmer(infile=infile_var, outfile = outfile_var, pdir = self.data_dir)

    def run(self):
        self.genovo_a.run()
#        check_outfiles(genovo_a)
#        self.glimmer_a.run()
#        check_outfiles(glimmer_a)
        if self.genovo_a.checkAssembleOutfilesExist(infile_var):
            if os.path.exists(self.genovo_a.readFinalizeOutfile.record_index):
                self.glimmer_a.run()
        if self.glimmer_a.checkG3OutfilesExist(outfile):
            pass
#            self.blast_a.run()
