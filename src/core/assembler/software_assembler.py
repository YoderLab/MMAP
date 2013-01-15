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

    def get_all_par(self):
        return self.setting.all_setting

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
        #TODO: fix MetaSim outfile name (can't overwrite program default)
        #TODO: use -454 error model!!
        self.debug = 1
        self.setting.print_all()

        if self.setting.run_mine:

            self.mine.run(self.debug)
        else:
            self.genovo.run(self.debug)
            self.glimmer.run(self.debug)
            self.blast.run(self.debug)


#        file_tag = self.setting.get("wdir") + self.setting.get("genovo_infile")
#        if (self.genovo.is_file_exist(file_tag)):
#            self.genovo.run(self.debug)
#        else:
#            raise(IOError("Missing genovo infile %s" % file_tag))
#
#        self.debug = 1
#        file_tag = self.setting.get("wdir") + self.setting.get("genovo_infile")
#        if (self.genovo.check_outfiles_with_filetag_exist(file_tag) and
#                self.genovo.is_file_exist(self.setting.get("genovo_outfile"))):
##            self.glimmer.run(self.debug)
#            pass
#        else:
#            raise(IOError("Missing glimmer infiles %s \t %s" %
#                          (self.genovo.check_outfiles_with_filetag_exist(file_tag) ,
#                          self.genovo.is_file_exist(self.setting.get("genovo_outfile")))))

#        if self.glimmer.check_outfiles_with_filetag_exist(self.setting.get("glimmer_outfile")):
#            self.blast.run()
#        else:
#            raise(IOError("Missing Glimmer output"))



#
#        if self.setting.get("blast_comparison_file") is not None:
#            if self.mine.is_file_exist(self.setting.get("mine_infile")):
#                print "===running MINE==="
#                self.mine.run(1)
#            else:
#                raise(IOError("Missing GO output\t %s" % self.setting.get("blast_outfile")))


    def runMine(self):


#        f1 = "/home/sw167/Postdoc/Project_Lemur/MMAP/data/benchMark1/primateA/primateA_out_out.orfs.csv"
#        f2 = "/home/sw167/Postdoc/Project_Lemur/MMAP/data/benchMark1/primateB/primateB_out_out.orfs.csv"
#        f3 = "/home/sw167/Postdoc/Project_Lemur/MMAP/data/benchMark1/primateC/primateC_out_out.orfs.csv"
#        f4 = "/home/sw167/Postdoc/Project_Lemur/MMAP/data/benchMark1/primateD/primateD_out_out.orfs.csv"
#        f5 = "/home/sw167/Postdoc/Project_Lemur/MMAP/data/benchMark1/FPV/FPV-454_out_out.orfs.csv"

#        f12 = "/home/sw167/Postdoc/Project_Lemur/MMAP/data/benchMark1/f12.csv"
#        f123 = "/home/sw167/Postdoc/Project_Lemur/MMAP/data/benchMark1/f123.csv"
#        f1234 = "/home/sw167/Postdoc/Project_Lemur/MMAP/data/benchMark1/f1234.csv"

#        self.blast.merge_output_csv_to_MINE(f12, [f1, f2])
#        self.blast.merge_output_csv_to_MINE(f123, [f1, f3, f4])
#        self.blast.merge_output_csv_to_MINE(f1234, [f1, f2, f3, f4])
#        self.blast.merge_output_csv_to_MINE(f12345, [f1, f2, f3, f4, f5])

        file_dir = "/home/sw167/Postdoc/Project_Lemur/MMAP/data/BenchMark2/"
        fileMINE = "/home/sw167/Postdoc/Project_Lemur/MMAP/data/BenchMark2/combine.csv"
        self.blast.merge_output_csv_to_MINE(fileMINE, [
            file_dir + "Lac_5k_0/Lactobacillus-454_5k_0_out_out.orfs.csv",
            file_dir + "Lac_5k_1/Lactobacillus-454_5k_1_out_out.orfs.csv",
            file_dir + "Lac_5k_2/Lactobacillus-454_5k_2_out_out.orfs.csv",
            file_dir + "Lac_5k_3/Lactobacillus-454_5k_3_out_out.orfs.csv",
            "%sEcoli_5k_1/Escerichia_coli-454_1_out_out.orfs.csv" % file_dir,
            file_dir + "Ecoli_5k_2/Escerichia_coli-454_2_out_out.orfs.csv",
            file_dir + "Ecoli_5k_3/Escerichia_coli-454_3_out_out.orfs.csv",
            file_dir + "Both_10k_1/both-454_10k_1_out_out.orfs.csv",
            file_dir + "Both_10k_2/both-454_10k_2_out_out.orfs.csv",
            file_dir + "Both_10k_3/both-454_10k_3_out_out.orfs.csv"
            ])

        self.setting.add("mine_infile", fileMINE)
        self.setting.add("wdir", file_dir)
        self.mine = RunMINE.create_class_from_setting(self.setting)
#        self.setting.add("mine_infile", fileMINE)
        self.mine.run(1)



