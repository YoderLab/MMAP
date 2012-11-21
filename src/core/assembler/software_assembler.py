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

    def init_program(self):
        self.metasim = RunMetaSim.create_metasim_from_setting(self.setting)
        self.genovo = RunGenovo.create_genovo_from_setting(self.setting)
        self.update_genovo_setting()
        self.glimmer = RunGlimmer.create_glimmer_from_setting(self.setting)
        self.update_glimmer_setting()

#        self.blast = RunBlast.create_blast_from_setting(self.setting)
        #TODO: check blast setting, except for record_index
#        self.mine = RunMINE.create_mine_from_setting(self.setting)
        #TODO: fix MINE/Blast setting

    def run(self):

        self.metasim.run(debug=0)
        file_tag = self.setting.get("wdir") + self.setting.get("metasim_outfile")
        if (self.metasim.check_outfiles_exist(file_tag)):

            self.genovo.run(debug=True)
        else:
            raise(IOError("Missing MetaSim output %s \t %s" %file_tag))

        file_tag = self.setting.get("wdir") + self.setting.get("genovo_infile")
        if (self.genovo.check_outfiles_exist(file_tag) and
            self.genovo.is_file_exist(self.setting.get("genovo_outfile"))):
            # and os.path.exists(self.genovo.readFinalizeOutfile):
            self.glimmer.run()
        else:
            raise(IOError("Missing Genovo output %s \t %s" %(self.genovo.check_outfiles_exist(file_tag) ,
                                                             self.genovo.is_file_exist(self.setting.get("genovo_outfile"))
            )))

        if self.glimmer.check_outfiles_exist(self.setting.get("glimmer_outfile")):
            self.blast = RunBlast.create_blast_from_setting(self.setting) #FIXME
            self.blast.run()
        else:
            raise(IOError("Missing Glimmer output"))

        if self.blast.check_outfiles_exist(self.setting.get("blast_outfile")):
            self.mine = RunMINE.create_mine_from_setting(self.setting) #FIXME:
            self.mine.run()
        else:
            raise(IOError("Missing GO output"))




