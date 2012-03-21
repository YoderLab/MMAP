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
import sys
import numpy
import scipy
import Bio


from Bio import SeqIO
from core.component.run_Genovo import RunGenovo
from core.connector import go_connector
from core.sequence import Sequence
from core.dist.matching_distance import MatchingDistance
from core.utils import path_utils


#from core.component.run_metaIDBA import RunMetaIDBA
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

#TODO(Steven Wu): explain local vs global
#platform = run_ext_prog.get_platform()
#if sys.platform.startswith('linux'):
#    platform="linux"
#elif sys.platform.startswith('darwin'):
#    plateform="mac"
#else:
#    print "Unsupport OS: %s" % sys.platform
#    sys.exit(-1)
    
#Linux (2.x and 3.x)    'linux2'
#Windows    'win32'
#Mac OS X    'darwin'




def setup_database():
    
    infile = data_dir+"AE014075_subSmall100.fasta"
    infile = data_dir+"MetaSim_bint-454.20e39f4c.fna"
    record_index = SeqIO.index(infile, "fasta") # use index for large file
    
    return record_index
    
def main():

    e_value_cut_off = 1e-15
    record_index = setup_database()
#    test_single(record_index, e_value_cut_off)
#    run_blast(record_index, e_value_cut_off)

    """
    run Genovo then blast
    TODO(Steven Wu): rewrite it with better way to connect them
    TODO(Steven Wu): switch program_name for different OS, setup dir/names 
    TODO: check data_dir/program_dir
    
    """
#    infile = "MetaSim_bint-454.20e39f4c.fna"
    infile_var = "testMetaIDBA.fasta"
    Genovo = RunGenovo(infile=infile_var, pdir = data_dir, noI=3, thresh=250)
    print Genovo.assemble.get_switch()
#    print Genovo.__doc__
#    print Genovo.setInfileName.__doc__
    print len(Genovo.assemble._switch)
    Genovo.setNumberOfIter(10)
    print "set iterations to 10", Genovo.assemble.get_switch()

    infile_var="newname.fasta"
#    print infile
#    Genovo = RunGenovo(infile=infile_var, pdir = data_dir, noI=3, thresh=250)
    Genovo.setInfileName(infile_var)
    print Genovo.assemble.get_switch()

#
#    Genovo.setNumberOfIter(12.54)
#    print "set iterations to 10", Genovo.assemble.get_switch()
#
#    Genovo.setNumberOfIter(-85)
#    print "set iterations to 10", Genovo.assemble.get_switch()

#    Genovo.assemble
#    Genovo.finalize
#    Genovo.run()
##    metaIDBA = RunMetaIDBA(infile=infile, pdir = data_dir)
##    metaIDBA.setSwitchMinK(1)
##    metaIDBA.setSwitchMaxK(2)
##    metaIDBA.run()
#    records = Genovo.readContig()
#    Glimmer = RunGlimmer(infile=infile, pdir = data_dir)
#    Glimmer.g3Iterated
#    records = metaIDBA.readContig()
#    BLAST = RunBlast(records, e_value_cut_off) # dont have proper metaIDBA output file
#    BLAST = RunBlast(record_index, e_value_cut_off)
#    BLAST.run();

    
 

if __name__ == "__main__":
    main()


