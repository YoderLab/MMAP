'''

@author: Steven Wu

require Biopython - 1.58
require numpy - 1.6.1
require SciPy - 0.10.0
require hcluster - 0.2 http://code.google.com/p/scipy-cluster/
require matplotlib - 1.1.0 http://matplotlib.sourceforge.net/ 
    matplotlib (and its dep) is only required to plot dendrogram (with "ipython -pylab") 

'''
import sys
import os

from Bio import SeqIO
import go_connector
#import sequence; reload(sequence)
#from sequence import *
from sequence import Sequence


import numpy
import scipy



from core import hclust
from core.hclust import HClust

print numpy.__version__
print scipy.__version__
working_dir = "/home/sw167/Postdoc/Project_Lemur/Data/"





data = "8332116"
data = "GO:0006468"
data = "MALVAGLSMRSGASHLVVSLAPMMAHRRFISDAAKSKLNDGPGFGEFVSGNVPLTPKALK"
data = "MALVAGLSMRSGASHLVVSLAPMMAHRRFISDAAKSKLNDGPGFGEFVSGNVPLTPKALKRKQRLRLPEWVKTDVPAGKNFARIKGNLRDLKLHTVCEEARCPNIGECWGGAEGTATATIMLMGDECTRGCRFCSIKTNKAPAPLDVDEPAHTAAAVAAWGLDYVVLTSVDRDDLPDGGSNHFASTVIELKKRKPEILVECLTPDFSGVYEDIARVAVSGLDVFAHNMETVESLTPSVRD"
data = "GTGTTCTACAGAGAGAAGCGTAGAGCAATAGGCTGTATTTTGAGAAAGCTGTGTGAGTGGAAAAGTGTACGGATTCTGGAAGCTGAATGCTGTGCAGATCATATCCATATGCTTGTGGAGATCCCGCCCAAAATGAGCGTATCAGGCTTTATGGGATATCTGAAAGGGAAAAGCAGTCTGATGCCTTACGAGCAGTTTGGTGATTTGAAATTCAAATACAGGAACAGGGAGTTCTGGTGCAGAGGGTATTACGTCGATACGGTGGGTAAGAACACGGCGAAGATACAGGATTACATAAAGCACCAGCTTGAAGAGGATAAAATGGGAGAGCAGTTATCGATTCCCTATCCGGGCAGCCCGTTTACGGGCCGTAAGTAA"

print os.getcwd()


infile = working_dir+"AE014075_sub.fasta"
infile = working_dir+"AE014075_subSmall.fasta"
#records = (SeqIO.parse(infile, "fasta"))
#records = list(SeqIO.parse(infile, "fasta"))
#record_dict = SeqIO.to_dict(SeqIO.parse(infile, "fasta"))
record_index = SeqIO.index(infile, "fasta") # use index for large file

#print record_index["lcl|AE014075.1_gene_1"].format("fasta")
data = record_index["lcl|AE014075.1_gene_1"].seq ## short no result
## TODO mismatch
## maybe change from *** NONE *** to 
##  Sorry, your BLAST query returned no results. Please see the raw BLAST data for full details.
data = record_index["lcl|AE014075.1_gene_2"].seq ## good
data = record_index["lcl|AE014075.1_gene_3"].seq ## long search time, implemented waiting time

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
    
    

e_value_cut_off = 1e-15
def test_single():
  
    data = record_index["lcl|AE014075.1_gene_2"].seq ## good
    seq = Sequence(data)
    seq = go_connector.blast_AmiGO(seq)
    seq = go_connector.extract_ID(seq)
    
    seq = go_connector.parse_go_term(seq, e_value_cut_off) 
    print "test set", seq.all_terms




def run_blast():
    
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







def main():
    print __name__;
#    test_hclust()
#    test_single()
#    run_blast()
    
if __name__ == "__main__":
    main()


