"""
require Biopython - 1.58
require numpy - 1.6.1
require SciPy - 0.10.0
require hcluster - 0.2 http://code.google.com/p/scipy-cluster/
"""
from Bio import SeqIO
#from Bio import Seq
import go_connector
#import sequence; reload(sequence)
#from sequence import *
from sequence import Sequence

import sys


import numpy
import scipy
from hcluster import pdist, linkage, dendrogram
import hcluster

print __name__
 

print numpy.__version__
print scipy.__version__
#print hcluster.__dict__
##print hcluster.__doc__
#print hcluster.__file__
#print hcluster.__name__
#print hcluster.__path__


data = "8332116"
data = "GO:0006468"
data = "MALVAGLSMRSGASHLVVSLAPMMAHRRFISDAAKSKLNDGPGFGEFVSGNVPLTPKALK"
data = "MALVAGLSMRSGASHLVVSLAPMMAHRRFISDAAKSKLNDGPGFGEFVSGNVPLTPKALKRKQRLRLPEWVKTDVPAGKNFARIKGNLRDLKLHTVCEEARCPNIGECWGGAEGTATATIMLMGDECTRGCRFCSIKTNKAPAPLDVDEPAHTAAAVAAWGLDYVVLTSVDRDDLPDGGSNHFASTVIELKKRKPEILVECLTPDFSGVYEDIARVAVSGLDVFAHNMETVESLTPSVRD"
data = "GTGTTCTACAGAGAGAAGCGTAGAGCAATAGGCTGTATTTTGAGAAAGCTGTGTGAGTGGAAAAGTGTACGGATTCTGGAAGCTGAATGCTGTGCAGATCATATCCATATGCTTGTGGAGATCCCGCCCAAAATGAGCGTATCAGGCTTTATGGGATATCTGAAAGGGAAAAGCAGTCTGATGCCTTACGAGCAGTTTGGTGATTTGAAATTCAAATACAGGAACAGGGAGTTCTGGTGCAGAGGGTATTACGTCGATACGGTGGGTAAGAACACGGCGAAGATACAGGATTACATAAAGCACCAGCTTGAAGAGGATAAAATGGGAGAGCAGTTATCGATTCCCTATCCGGGCAGCCCGTTTACGGGCCGTAAGTAA"


## import seq
infile = "/home/sw167/Postdoc/Project_Lemur/Data/AE014075_sub.fasta"
infile = "/home/sw167/Postdoc/Project_Lemur/Data/AE014075_subSmall.fasta"

#records = (SeqIO.parse(infile, "fasta"))
#records = list(SeqIO.parse(infile, "fasta"))
#record_dict = SeqIO.to_dict(SeqIO.parse(infile, "fasta"))

## use index for large file
record_index = SeqIO.index(infile, "fasta")
len(record_index)
sorted(record_index)

#print record_index["lcl|AE014075.1_gene_1"].format("fasta")
#testS = record_index["lcl|AE014075.1_gene_1"]

data = record_index["lcl|AE014075.1_gene_1"].seq ## short no result
## maybe change from *** NONE *** to 
##  Sorry, your BLAST query returned no results. Please see the raw BLAST data for full details.
data = record_index["lcl|AE014075.1_gene_2"].seq ## good
data = record_index["lcl|AE014075.1_gene_3"].seq ## TODO long need implement waiting time

#data = str(data)
#data = data+data+data+data+data+data

#for i in sorted(record_index): print i

## do more test here later
try:
    v = float("12.33")
except ValueError as e:
    print 'Exception error is: %s' % e;
    print "c0", sys.exc_info()[0], sys.exc_info()[1]
    raise
    
    
    




e_value_cut_off = 1e-15

data = record_index["lcl|AE014075.1_gene_2"].seq ## good
seq = Sequence(data)
seq = go_connector.blast_AmiGO(seq)
seq = go_connector.extract_ID(seq)

seq = go_connector.parse_go_term(seq, e_value_cut_off) 
print seq.all_terms




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
    run_blast()
    
    
    
#if __name__ == "__main__":
#    main()

#save_file = open("testWaitResult2.html", "w")
#save_file.write(seq.webPage)  
#save_file.close()


#
#
#import go_connector
#
#
#reload(go_connector)
#seq = go_connector.parse_go_term(seq) 
#seq.all_terms
#
#
#
#seq = Sequence(data)
#print len(seq.data)
#
#seq = go_connector.blast_AmiGO(seq)
#seq = go_connector.extract_ID(seq)
##if seq.is_match:
