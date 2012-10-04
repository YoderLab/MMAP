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
from core.component.run_genovo import RunGenovo
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



def setup_database():

    infile = data_dir + "AE014075_subSmall100.fasta"
    infile = data_dir + "MetaSim_bint-454.20e39f4c.fna"
    record_index = SeqIO.index(infile, "fasta") # use index for large file

    return record_index


def main():
    print __name__





    m = [ [[]] * 3, [[]] * 3,[[]] * 3, [[]] * 3]
    print m[0]
    print m[0][0]
    print m[0][1]
    print m[1]
    print m[2]
    print m[3]
    print len(m)
    print( len(m[0]) )
    print range(12)
    for i in range( 4 ):
        for j in range(3):
            print "i: ", i, "j: ", j
            m[i][j] = i*3 + j

    print "===="
    print m[0]
    print m[1]
    print m[2]
    print m[3]

#    print m










#    time_profile()
    e_value_cut_off = 1e-15
    record_index = setup_database()
#    test_single(record_index, e_value_cut_off)
#    run_blast(record_index, e_value_cut_off)

    """
    run Genovo then blast
    TODO(Steven Wu): rewrite it with better way to connect them 
    """
#    infile = "MetaSim_bint-454.20e39f4c.fna"
    infile_var = "wdir_all_reads.fa"
    outfile = "testout"
    genovo_dir = "/Users/erinmckenney/Desktop/Pipeline/metaLem/data/Genovo/test_data"
#    Genovo = RunGenovo(infile=infile_var, outfile=outfile, pdir=genovo_dir, no_iter=3, thresh=250)



    """
    Code below allows you to change the assemble variables individually
    and tests to make sure changed variables go to correct position
    """
#    print len(Genovo.assemble._switch)
#    Genovo.setNumberOfIter(10)
#    print "set iterations to 10", Genovo.assemble.get_switch()
#
#    infile_var="newname.fasta"
##    print infile
##    Genovo = RunGenovo(infile=infile_var, pdir = data_dir, noI=3, thresh=250)
#    Genovo.setInfileName(infile_var)
#    print Genovo.assemble.get_switch()

    """
    Now try to do same thing for finalize: write 3 methods to
    save variables separately, and test with print commands.
    """
#    print len(Genovo.finalize._switch)
#    print "set Cutoff to 250a", Genovo.finalize.get_switch()
#    Genovo.setCutoff(16.5)
#    print "set Cutoff to 16.5", Genovo.finalize.get_switch()
#    Genovo.setCutoff(-16)
#    print "set Cutoff to -16", Genovo.finalize.get_switch()

#    infile_var = "VICTORY!!!.fasta"
##    print infile
##    Genovo = RunGenovo(infile=infile_var, pdir = data_dir, noI=3, thresh=250)
#    Genovo.set_infile_name(infile_var)
#
#    print Genovo.finalize.get_switch()

#    Genovo = RunGenovo(infile=infile_var, outfile=outfile, pdir=genovo_dir, no_iter=3, thresh=250, check_exist=False)
#    Genovo.set_outfile("sdif")
#    print "set outfile to sdif", Genovo.finalize.get_switch()
#    Genovo2 = RunGenovo(infile=infile_var, pdir=genovo_dir, no_iter=3, thresh=250, check_exist=False)   ## outfile == None
#    print "outfile = None = out.test", Genovo2.finalize.get_switch()
#    Genovo2.set_cutoff(-2.3)

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


