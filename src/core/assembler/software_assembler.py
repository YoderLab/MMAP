"""
Created on April 16, 2012

@author: Erin McKenney and Steven Wu
"""
from core.component.run_MetaSim import RunMetaSim
from core.component.run_genovo import RunGenovo
from core.component.run_glimmer import RunGlimmer
from core.component.run_BLAST import RunBlast
from core.component.run_MINE import RunMINE
from core.setting import Setting


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
        self.setting = Setting(**kwargs)

    def add_all_param(self, **kwargs):
        self.setting.add_all(**kwargs)

    def get_all_par(self):
        return self.setting.all_setting

    def update_genovo_setting(self):
        self.setting.add("genovo_outfile", self.genovo.outfile)

    def init_program(self):
        self.metasim = RunMetaSim.create_metasim_from_setting(self.setting)
        self.genovo = RunGenovo.create_genovo_from_setting(self.setting)
        self.update_genovo_setting()
        self.glimmer = RunGlimmer.create_glimmer_from_setting(self.setting)
        self.blast = RunBlast.create_blast_from_setting(self.setting)
        self.mine = RunMINE.create_mine_from_setting(self.setting)

    def run(self):

        self.metasim.run()
        file_tag = self.setting.get("wdir") + self.setting.get("metasim_infile")
        if (self.metasim.check_outfiles_exist(file_tag) and
            self.metasim.is_file_exist(self.setting.get("metasim_outfile"))):
            pass
#          self.genovo.run()
        file_tag = self.setting.get("wdir") + self.setting.get("genovo_infile")
        if (self.genovo.check_outfiles_exist(file_tag) and
            self.genovo.is_file_exist(self.setting.get("genovo_outfile"))):
            # and os.path.exists(self.genovo.readFinalizeOutfile):
            self.glimmer.run()
        else:
            raise(IOError("Missing genovo output"))




        if self.glimmer.check_outfiles_exist(self.setting.get("glimmer_outfile")):
            self.blast.run()
        else:
            raise(IOError("Missing glimmer output"))
        if self.blast.check_outfiles_exist(self.setting.get("blast_outfile")):
            self.MINE.run()
        else:
            raise(IOError("Missing GO output"))




