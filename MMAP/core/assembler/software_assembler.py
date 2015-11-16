"""
Created on April 16, 2012

@author: Erin McKenney and Steven Wu
"""
from core.component.run_MetaSim import RunMetaSim
from core.component.run_genovo import RunGenovo
from core.component.run_glimmer import RunGlimmer
# from core.component.run_BLAST import RunBlast #TODO at some stage, it should be able to run both versions
from core.component.run_local_BLAST import RunBlast
from core.component.run_MINE import RunMINE
from core.setting import Setting
from core.component import run_BLAST
from core.component.run_xgenovo import RunXGenovo



__author__ = 'erinmckenney'


class SoftwareAssembler(object):

    def __init__(self, setting=None, debug=0):
        """
        create the following:
        Genovo class object
        Glimmer class object

        in_genovo
        in_glimmer == out_genovo
        out_glimmer
        """
#        if setting == None:
#            print "fghj"
#            self.setting = Setting(**kwargs)
#        else:
        self.setting = setting
        self.init_program()
        self.debug = debug



    @classmethod
    def create_from_args(cls, args):
        setting = Setting.create_setting_from_file(args)
        assembler = cls(setting, args.debug)
        return assembler


    def get_all_par(self):
        return self.setting.all_setting

    def get(self, key):
        return self.setting.get(key)


    def init_program(self):
#         self.metasim = RunMetaSim.create_metasim_from_setting(self.setting)
        if self.setting.run_mine:
            self.mine = RunMINE.create_class_from_setting(self.setting)
        else:
            if self.setting.get("assembler_prog") is "genovo":
                self.assembler = RunGenovo.create_genovo_from_setting(self.setting)
            elif self.setting.get("assembler_prog") is "xgenovo":
                self.assembler = RunXGenovo.create_xgenovo_from_setting(self.setting)

            self.glimmer = RunGlimmer.create_glimmer_from_setting(self.setting)
#             self.blast = run_BLAST.RunBlast.create_blast_from_setting(self.setting)
            self.blast = RunBlast.create_blast_from_setting(self.setting)



    def run(self):

        # self.metasim.run(debug=0)
        # TODO: add metasim.run back later.
        #    fix MetaSim outfile name (can't overwrite program default)
        #    use -454 error model!!

        if self.setting.run_mine:
            self.mine.run(self.debug)
        else:
            self.assembler.run(self.debug)
            self.glimmer.run(self.debug)
            self.blast.run(self.debug)
        print "=== Done ==="




#     def _update_genovo_setting(self):
#         print "Set genevo", self.setting.get("genovo_outfile"), self.genovo.outfile
#         self.setting.add("genovo_outfile", self.genovo.outfile)
#
#     def _update_glimmer_setting(self):
#         print "Update glimmer", self.glimmer.infile, self.glimmer.outfile
#         print "SETTING glimmer", self.setting.get("glimmer_infile"), self.setting.get("glimmer_outfile")
#         self.setting.add("glimmer_infile", self.glimmer.infile)
#         self.setting.add("glimmer_outfile", self.glimmer.outfile)
# #        self.setting.add("extract_outfile", self.glimmer.orfs_file)
#
#     def _update_blast_setting(self):
#         self.setting.add("blast_infile", self.glimmer.outfile)
#         self.setting.add("blast_outfile", self.blast.outfile)
#
#     def _update_mine_setting(self):
#         self.setting.add("mine_infile", self.blast.outfile)
