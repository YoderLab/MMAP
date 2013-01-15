"""
Created on Nov 7, 2012

@author: Erin McKenney
"""
#TODO: format correctly
import warnings
"""
#list_essential_shared
parent_directory:
#list_essential_metasim_only
metasim_pdir:
metasim_model_infile:
metasim_taxon_infile:
metasim_no_reads:
#list_essential_genovo_only
genovo_infile:
genovo_pdir:
genovo_noI:
genovo_thresh:
#list_essential_glimmer_only
glimmer_pdir:
#list_essential_blast_only
blast_wdir:
#list_essential_mine_only
mine_pdir:
mine_comparison_style:
#list_optional_shared
wdir:
checkExist:
#list_optional_metasim_only
metasim_outfile:
#list_optional_genovo_only
genovo_outfile:
#list_optional_glimmer_only
glimmer_infile:
glimmer_outfile:

#list_optional_blast_only
blast_infile:
blast_e_value:
blast_outfile:
#list_optional_mine_only
mine_infile:
mine_cv:
mine_clumps:
mine_jobID:
"""


class ControlFile(object):
    #TODO: check what happens if the same key shows up multiple times in the control file
    #FIXME: individual program directories should append to parent_directory [with some sort of check]
    def __init__(self, **kwargs):
        """
        """
        warnings.simplefilter('default')
        warnings.warn("deprecated class: ControlFile", DeprecationWarning)

        self.all_arguments = dict()
        self.debug = False

    def add_all(self, controlfile):
        infile = open(controlfile)
        for line in infile:
            line = line.strip()
            if line.startswith("#") or line == "":
                pass
            else:

                location = line.find("=")

                key = line[0:location].strip()
                value = line[location + 1:len(line)].strip()
#                print line, "z",key, "z",value
                self.all_arguments[key] = value


        return self.all_arguments


    def get_all_keys(self):
#        print key, self.all_arguments[key]
        return self.all_arguments.keys()

    def get(self, key):
#        print key, self.all_arguments[key]
        return self.all_arguments[key]
