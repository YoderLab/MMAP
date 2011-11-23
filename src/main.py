"""
require Biopython - 1.58
require numpy - 1.6.1
require SciPy - 0.10.0
require hcluster - 0.2 http://code.google.com/p/scipy-cluster/
require matplotlib - 1.1.0 http://matplotlib.sourceforge.net/ 
    matplotlib (and its dep) is only required to plot dendrogram (with "ipython -pylab") 

"""
import sys
import os

from Bio import SeqIO
import go_connector
#import sequence; reload(sequence)
#from sequence import *
from sequence import Sequence


import numpy
import scipy

from hcluster import *
from numpy.random import rand


print numpy.__version__
print scipy.__version__


def test_hcluster():
    X = rand(3,5)
#    X[0:5,:] *= 2
   
    #R = dendrogram(Z)
    #dendrogram(Z, color_threshold=1.8)

    Y=pdist(X, 'seuclidean')
    Z=linkage(Y, 'single')
    print "X:",X
    print "Y:",Y, type(Y),  Y.shape, Y.dtype
    print "Z:",Z
    
#    Y=numpy.ndarray(numpy.array([1.1,2.2,3.3,4.4]))
    Y= numpy.array(range(1,7))
    print "Y:",Y, type(Y),  Y.shape, Y.dtype
    print squareform(Y)
    Z=linkage(Y, 'single')

    print "Z:",Z
    print dendrogram(Z)
    
#    set1 = set([]) 
#    set2 = set(['GO:0016310', 'GO:0009067', 'GO:0005488', 'GO:0016597', 'GO:0016491', 'GO:0005737', 'GO:0006566', 'GO:0050661', 'GO:0040007', 'GO:0009570', 'GO:0005634', 'GO:0006520', 'GO:0019877', 'GO:0000166', 'GO:0016740', 'GO:0009097', 'GO:0009090', 'GO:0009088', 'GO:0016301', 'GO:0003824', 'GO:0008152', 'GO:0005886', 'GO:0055114', 'GO:0009507', 'GO:0008652', 'GO:0005829', 'GO:0006555', 'GO:0004412', 'GO:0005575', 'GO:0009089', 'GO:0005524', 'GO:0006531', 'GO:0009086', 'GO:0004072', 'GO:0009082'])
#    set3 = set(['GO:0004803', 'GO:0006313'])
#    set4 = set(['GO:0005125', 'GO:0016311', 'GO:0046360', 'GO:0003674', 'GO:0030170', 'GO:0004795', 'GO:0005737', 'GO:0006566', 'GO:0005615', 'GO:0016829', 'GO:0006520', 'GO:0005524', 'GO:0004765', 'GO:0003824', 'GO:0008150', 'GO:0070905', 'GO:0008152', 'GO:0009071', 'GO:0008652', 'GO:0006897', 'GO:0005829', 'GO:0005575', 'GO:0005576', 'GO:0009088', 'GO:0005515', 'GO:0005634'])
#    set5 = set(['GO:0005737', 'GO:0016310', 'GO:0009617', 'GO:0004413', 'GO:0000166', 'GO:0009620', 'GO:0009088', 'GO:0009570', 'GO:0009086', 'GO:0005524', 'GO:0009507'])
#    
    
    set1 = set([]) 
    set2 = set(['GO:001', 'GO:002', 'GO:003', 'GO:003', 'GO:004'])
    set3 = set(['GO:003', 'GO:004'])
    set4 = set(['GO:005', 'GO:006', 'GO:007'])
    set5 = set(['GO:005', 'GO:006', 'GO:009', 'GO:010', 'GO:100'])
    
    ##assuming set(s) store as list for now
    all_sets =  [set1, set2, set3, set4, set5]
    len_set = len(all_sets)
    Y = numpy.ndarray(shape=(len_set*(len_set-1)/2))
    Y= numpy.zeros(shape=(len_set*(len_set-1)/2), dtype=numpy.int32)
    for i, s in enumerate(all_sets):
        for j, t in enumerate( all_sets[(i+1):len_set] ):
#            print s, "and i:", i, "and t:", t 
#            print "%s and \t i:%d \t j:%d and t: %s" % (str(s), i ,j+i+1,str(t))
            Y[1+i+j] = len(s&t)

    
    print "Round Y:", Y
    print squareform(Y)
    Z=linkage(Y, 'single')
    
    print "Z:",Z, type(Z)
    print dendrogram(Z,no_plot=True)
    
#    Z = numpy.array([[1.0,2,3,4],[1.1,2.1,3.1,4.1],[1.2,2.2,5.2,6.2]]) 
#    print Z, dir(Z)
#    print dendrogram(Z,no_plot=True)
#    
    print "2&3", set2 & set3
    print "3-4", set3 - set4
    print "4-3", set4 - set3
    print "5-4", set5 - set4
    print "5|4", set5 | set4
    print "5^4", set5 ^ set4


    



data = "8332116"
data = "GO:0006468"
data = "MALVAGLSMRSGASHLVVSLAPMMAHRRFISDAAKSKLNDGPGFGEFVSGNVPLTPKALK"
data = "MALVAGLSMRSGASHLVVSLAPMMAHRRFISDAAKSKLNDGPGFGEFVSGNVPLTPKALKRKQRLRLPEWVKTDVPAGKNFARIKGNLRDLKLHTVCEEARCPNIGECWGGAEGTATATIMLMGDECTRGCRFCSIKTNKAPAPLDVDEPAHTAAAVAAWGLDYVVLTSVDRDDLPDGGSNHFASTVIELKKRKPEILVECLTPDFSGVYEDIARVAVSGLDVFAHNMETVESLTPSVRD"
data = "GTGTTCTACAGAGAGAAGCGTAGAGCAATAGGCTGTATTTTGAGAAAGCTGTGTGAGTGGAAAAGTGTACGGATTCTGGAAGCTGAATGCTGTGCAGATCATATCCATATGCTTGTGGAGATCCCGCCCAAAATGAGCGTATCAGGCTTTATGGGATATCTGAAAGGGAAAAGCAGTCTGATGCCTTACGAGCAGTTTGGTGATTTGAAATTCAAATACAGGAACAGGGAGTTCTGGTGCAGAGGGTATTACGTCGATACGGTGGGTAAGAACACGGCGAAGATACAGGATTACATAAAGCACCAGCTTGAAGAGGATAAAATGGGAGAGCAGTTATCGATTCCCTATCCGGGCAGCCCGTTTACGGGCCGTAAGTAA"

print os.getcwd()
working_dir = "/home/sw167/Postdoc/Project_Lemur/Data/"
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
#    test_hcluster()
    test_single()
#    run_blast()
    
if __name__ == "__main__":
    main()


