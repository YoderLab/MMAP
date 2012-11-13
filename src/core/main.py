'''

@author: Steven Wu

require Biopython - 1.58
require numpy - 1.6.1
require SciPy - 0.10.0

not require hcluster - 0.2 http://code.google.com/p/scipy-cluster/
not require matplotlib - 1.1.0 http://matplotlib.sourceforge.net/ 
    matplotlib (and its dep) is only required to plot dendrogram (with "ipython -pylab") 


'''
import os
import numpy
import scipy
import Bio


from Bio import SeqIO
from core import controlfile
from core.component.run_genovo import RunGenovo
from core.connector import go_connector
from core.sequence import Sequence
from core.dist.matching_distance import MatchingDistance
from core.utils import path_utils


from core.connector.go_connector import GOConnector
from core.component.run_BLAST import RunBlast
from core import run_ext_prog


print "NumPy version %s" % numpy.__version__
print "SciPy version %s" % scipy.__version__
print "Bio version %s" % Bio.__version__

print Bio.__path__

CWD = os.getcwd()
data_dir = path_utils.get_data_dir(CWD)
print "data dir:\t", data_dir



def setup_database():

    infile = data_dir + "AE014075_subSmall100.fasta"
    infile = data_dir + "MetaSim_bint-454.20e39f4c.fna"
    record_index = SeqIO.index(infile, "fasta") # use index for large file

    return record_index


def main():
    print __name__




if __name__ == "__main__":
    main()

#    TODO: read in all parameters from controlfile
#    TODO: feed paramters into setting class instance (below)
    # Should we use setting.get(), or write a controlfile.get()?

    @classmethod
    def create_setting_from_controlfile(cls, controlfile):
        setting = cls(parent_directory=controlfile.get("parent_directory"),
                    metasim_pdir=controlfile.get("parent_directory"),
                    metasim_model_infile=controlfile.get("metasim_model_infile"),
                    metasim_taxon_infile=controlfile.get("metasim_taxon_infile"),
                    metasim_no_reads=controlfile.get("metasim_no_reads"),
                    genovo_infile=controlfile.get("genovo_infile"),
                    genovo_pdir=controlfile.get("genovo_pdir"),
                    genovo_noI=controlfile.get("genovo_noI"),
                    genovo_thresh=controlfile.get("genovo_thresh"),
                    glimmer_pdir=controlfile.get("glimmer_pdir"),
                    blast_wdir=controlfile.get("blast_wdir"),
                    mine_pdir=controlfile.get("mine_pdir"),
                    mine_comparison_style=controlfile.get("mine_comparison_style"),
                    wdir=controlfile.get("wdir"),
                    checkExist=controlfile.get("checkExist"),
                    metasim_outfile=controlfile.get("metasim_outfile"),
                    genovo_outfile=controlfile.get("genovo_outfile"),
                    glimmer_infile=controlfile.get("glimmer_infile"),
                    glimmer_outfile=controlfile.get("glimmer_outfile"),
                    extract_outfile=controlfile.get("extract_outfile"),
                    blast_infile=controlfile.get("blast_infile"),
                    blast_e_value=controlfile.get("blast_e_value"),
                    blast_outfile=controlfile.get("blast_outfile"),
                    mine_infile=controlfile.get("mine_infile"),
                    mine_cv=controlfile.get("mine_cv"),
                    mine_clumps=controlfile.get("mine_clumps"),
                    mine_jobID=controlfile.get("mine_jobID"))
        return setting

    @classmethod
    def create_SoftwareAssembler_from_setting(cls, setting):
        assembler = cls(setting.get_all_par("all"))
        return assembler

#        TODO: call software_assembler.run()

