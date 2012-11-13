"""
Created on Nov 7, 2012

@author: Erin McKenney
"""
#TODO: format correctly

list_essential_shared
"parent_directory":

list_essential_metasim_only
"metasim_pdir":
"metasim_model_infile":
"metasim_taxon_infile":
"metasim_no_reads":

list_essential_genovo_only
"genovo_infile":
"genovo_pdir":
"genovo_noI":
"genovo_thresh":

list_essential_glimmer_only
"glimmer_pdir":

list_essential_blast_only
"blast_wdir":

list_essential_mine_only
"mine_pdir":
"mine_comparison_style":

list_optional_shared
"wdir":
"checkExist":

list_optional_metasim_only
"metasim_outfile":

list_optional_genovo_only
"genovo_outfile":

list_optional_glimmer_only
"glimmer_infile":
"glimmer_outfile":
"extract_outfile":

list_optional_blast_only
"blast_infile":
"blast_e_value":
"blast_outfile":

list_optional_mine_only
"mine_infile":
"mine_cv":
"mine_clumps":
"mine_jobID":

class ControlFile(object):

    def __init__(self, **kwargs):
        """
        """
        self.all_arguments = dict()
#        self.add_all(**kwargs)
        self.debug = False

    def get(self, key):
        return self.all_arguments[key]