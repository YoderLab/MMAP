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

    def __init__(self, setting=None):
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



    def add_all_param(self, **kwargs):
        self.setting.add_all(**kwargs)

    def get_all_par(self):
        return self.setting.all_setting

    def update_genovo_setting(self):
        self.setting.add("genovo_outfile", self.genovo.outfile)

    def update_glimmer_setting(self):
        self.setting.add("glimmer_infile", self.glimmer.infile)
        self.setting.add("glimmer_outfile", self.glimmer.outfile)
        self.setting.add("extract_outfile", self.glimmer.orfs)

    def update_blast_setting(self):
        self.setting.add("blast_infile", self.glimmer.orfs)
        self.setting.add("blast_outfile", self.blast.outfile)

#    def update_mine_setting(self):
#        self.setting.add("mine_infile", self.blast.outfile)

    def init_program(self):
        self.metasim = RunMetaSim.create_metasim_from_setting(self.setting)
        self.genovo = RunGenovo.create_genovo_from_setting(self.setting)
        self.update_genovo_setting()
        self.glimmer = RunGlimmer.create_glimmer_from_setting(self.setting)
        self.update_glimmer_setting()
        self.blast = RunBlast.create_blast_from_setting(self.setting)
        self.update_blast_setting()
        if self.setting.get("blast_comparison_file") is not None:
            self.mine = RunMINE.create_mine_from_setting(self.setting)
#        self.update_mine_setting()


    def run(self):

#        self.metasim.run(debug=0)
        #TODO: add metasim.run back later.
        file_tag = self.setting.get("wdir") + self.setting.get("metasim_outfile")
        if (self.metasim.check_outfiles_with_filetag_exist(file_tag)):

            self.genovo.run(debug=False)
        else:
            #TODO: fix MetaSim outfile name (can't overwrite program default)
            #TODO: use -454 error model!!
            raise(IOError("Missing MetaSim output %s" %file_tag))

        file_tag = self.setting.get("wdir") + self.setting.get("genovo_infile")
        if (self.genovo.check_outfiles_with_filetag_exist(file_tag) and
            self.genovo.is_file_exist(self.setting.get("genovo_outfile"))):
            # and os.path.exists(self.genovo.readFinalizeOutfile):
            self.glimmer.run()
        else:
            raise(IOError("Missing Genovo output %s \t %s" %(self.genovo.check_outfiles_with_filetag_exist(file_tag) ,
                                                             self.genovo.is_file_exist(self.setting.get("genovo_outfile"))
            )))

        if self.glimmer.check_outfiles_with_filetag_exist(self.setting.get("glimmer_outfile")):
#            self.blast = RunBlast.create_blast_from_setting(self.setting)
            self.blast.run()
        else:
            raise(IOError("Missing Glimmer output"))

        if self.setting.get("blast_comparison_file") is not None:
            if self.mine.is_file_exist(self.setting.get("mine_infile")):
                print "===running MINE==="
                self.mine.run(1)
            else:
                raise(IOError("Missing GO output\t %s" %self.setting.get("blast_outfile")))




