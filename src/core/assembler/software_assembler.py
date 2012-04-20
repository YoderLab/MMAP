"""
Created on April 16, 2012

@author: Erin McKenney and Steven Wu
"""
from PIL.Scripts.explode import infile
from core.component.run_Genovo import RunGenovo
from core.component.run_glimmer import RunGlimmer
from core.setting import Setting
from traits.trait_types import self

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





    def init_program(self):
        self.setting.check()
        self.genovo_a = RunGenovo(self.setting.get("genovo_infile"), outfile, pdir, noI, thresh)
        self.glimmer_a = RunGlimmer(infile, outfile, pdir)
#        genovo = RunGenovo(infile=infile_var, outfile = outfile_var, pdir = self.data_dir, noI=10, thresh=100, checkExist=True)

#    glimmer = RunGlimmer(infile=infile_var, outfile = outfile_var, pdir = self.data_dir)

    def run(self):
        self.genovo_a.run()
        if self.genovo_a.checkAssembleOutfilesExist(infile_var):
            self.glimmer_a.run()