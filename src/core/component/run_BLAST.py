"""
Created on Feb 13, 2012

@author: Steven Wu
"""
from core.connector import go_connector
from core.sequence import Sequence


class RunBlast(object):
    """
    run BLAST
    take record parameter, assumed files read from Bio.SeqIO.index
    Bio.SeqIO.index returns a dictionary like object.

    TODO(Steven Wu): copy/pasted from old main.py. Add test class
    """
    def __init__(self, records, e_value):
        """
        Constructor
        records: collection of Bio.SeqRecord.SeqRecord
                can be created by Bio.SeqIO.index
                OR dict(key=Bio.SeqRecord.SeqRecord, ...)
        """
        self.results = dict()
        self.record_index = records
        self.e_value_cut_off = e_value

    def run(self):

        print("Running AmiGO:BLAST")

        for key in self.record_index:

            self.seq = Sequence(self.record_index[key].seq) #Bio.SeqRecord.SeqRecord

            self.seq = go_connector.blast_AmiGO(self.seq)
            self.seq = go_connector.extract_ID(self.seq)
            self.seq = go_connector.parse_go_term(self.seq, self.e_value_cut_off)
#            self.seq.all_terms
            self.results[key] = self.seq

#        for i in self.results.values():
#            print(i.all_terms)


