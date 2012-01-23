'''

@author: Steven Wu

require Biopython - 1.58
require numpy - 1.6.1
require SciPy - 0.10.0

not require hcluster - 0.2 http://code.google.com/p/scipy-cluster/
not require matplotlib - 1.1.0 http://matplotlib.sourceforge.net/ 
    matplotlib (and its dep) is only required to plot dendrogram (with "ipython -pylab") 

'''
import sys
import os


from core.connector import go_connector
from core.sequence import Sequence
from core.dist.matching_distance import MatchingDistance
from core.utils import path_utils


import numpy
import scipy
import Bio
from Bio import SeqIO

print "NumPy version %s" % numpy.__version__
print "SciPy version %s" % scipy.__version__
print "Bio version %s" % Bio.__version__

CWD = os.getcwd()
data_dir = path_utils.get_data_dir(CWD)
print data_dir

def test_single(record_index, e_value_cut_off):
  
    data = record_index["lcl|AE014075.1_gene_3"].seq ## good
    seq = Sequence(data)
    seq = go_connector.blast_AmiGO(seq)
    seq = go_connector.extract_ID(seq)
    
    seq = go_connector.parse_go_term(seq, e_value_cut_off)
    print "test set", seq.each_term 
    print "test set", seq.all_terms
    
    dist_method = MatchingDistance()
    dist_matirx = dist_method.cal_dist(seq)
    print dist_matirx



def run_blast(record_index, e_value_cut_off):
    
    results = dict()
    for key in record_index:
        seq = Sequence(record_index[key].seq)
        print len(seq.data)
    
        seq = go_connector.blast_AmiGO(seq)
        seq = go_connector.extract_ID(seq)
        seq = go_connector.parse_go_term(seq, e_value_cut_off) 
    
        seq.all_terms    
        results[key] = seq
    

    for i in results.values(): 
        print i.all_terms







def setup_database():
    
    infile = data_dir+"AE014075_subSmall100.fasta"
    infile = data_dir+"AE014075_subTiny5.fasta"
    #records = (SeqIO.parse(infile, "fasta"))
    #records = list(SeqIO.parse(infile, "fasta"))
    #record_dict = SeqIO.to_dict(SeqIO.parse(infile, "fasta"))
    record_index = SeqIO.index(infile, "fasta") # use index for large file
    
    #print record_index["lcl|AE014075.1_gene_1"].format("fasta")
#    data = record_index["lcl|AE014075.1_gene_1"].seq ## short no result
    ## TODO mismatch
    ## maybe change from *** NONE *** to 
    ##  Sorry, your BLAST query returned no results. Please see the raw BLAST data for full details.
#    data = record_index["lcl|AE014075.1_gene_2"].seq ## good
#    data = record_index["lcl|AE014075.1_gene_3"].seq ## long search time, implemented waiting time
    
    #data = str(data)
    #data = data+data+data+data+data+data
    
    ## do more test here later
    ##Test try...except..raise
    #try:
    #    v = float("12.33")
    #except ValueError as e:
    #    print 'Exception error is: %s' % e;
    #    print "c0", sys.exc_info()[0], sys.exc_info()[1]
    #    raise
    return record_index
    


def main():
    print __name__
    e_value_cut_off = 1e-15
    record_index = setup_database()
#    test_single(record_index, e_value_cut_off)
#    run_blast(record_index, e_value_cut_off)


if __name__ == "__main__":
    main()


