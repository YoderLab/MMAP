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
from core.component import run_MINE


__author__ = 'erinmckenney'


class SoftwareAssembler(object):

    def __init__(self, setting=None, debug=0):
        """
        create the following:
        Genovo class object
        Glimmer class object

        in_geno
        out_ge == in_glim
        pdir_gen ~ pdit_gli

        out_gli
        """
#        if setting == None:
#            print "fghj"
#            self.setting = Setting(**kwargs)
#        else:
        self.setting = setting
        self.init_program()
        self.debug = debug


#    def add_all_param(self, **kwargs):
#        self.setting.add_all(**kwargs)

    @classmethod
    def create_from_args(cls, args):
        setting = Setting.create_setting_from_file(args.controlFile)
        assembler = cls(setting, args.debug)
        return assembler


    def get_all_par(self):
        return self.setting.all_setting

    def get(self, key):
        return self.setting.get(key)

    def update_genovo_setting(self):
        self.setting.add("genovo_outfile", self.genovo.outfile)

    def update_glimmer_setting(self):
        self.setting.add("glimmer_infile", self.glimmer.infile)
        self.setting.add("glimmer_outfile", self.glimmer.outfile)
#        self.setting.add("extract_outfile", self.glimmer.orfs_file)

    def update_blast_setting(self):
        self.setting.add("blast_infile", self.glimmer.outfile)
        self.setting.add("blast_outfile", self.blast.outfile)
#        try:
#            self.setting.add("blast_merged_file", self.blast.merged_file)
#        except:
#            pass
##    def update_mine_setting(self):
#        self.setting.add("mine_infile", self.blast.outfile)

    def init_program(self):
#        self.metasim = RunMetaSim.create_metasim_from_setting(self.setting)
        if self.setting.run_mine:
            self.mine = RunMINE.create_class_from_setting(self.setting)
        else:
            self.genovo = RunGenovo.create_genovo_from_setting(self.setting)
            self.update_genovo_setting()

            self.glimmer = RunGlimmer.create_glimmer_from_setting(self.setting)
            self.update_glimmer_setting()

            self.blast = RunBlast.create_blast_from_setting(self.setting)
            self.update_blast_setting()

#        if self.setting.get("mine_pdir") is not None:


#        try:

#        except StandardError as e:
#            print e



    def run(self, debug=0):

#        self.metasim.run(debug=0)
        #TODO: add metasim.run back later.
        #    fix MetaSim outfile name (can't overwrite program default)
        #    use -454 error model!!

#        self.debug = 1
#        self.setting.print_all()

        if self.setting.run_mine:

            self.mine.run(self.debug)
        else:
            self.genovo.run(self.debug)
            self.glimmer.run(self.debug)
            self.blast.run(self.debug)
        print "=== Done ==="
