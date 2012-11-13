"""
Created on Feb 13, 2012

@author: Steven Wu
"""
import os
from Bio import SeqIO
import csv
from core.connector import go_connector
from core.sequence import Sequence
from core.component.run_component import RunComponent

class RunBlast(RunComponent):
    """
    run BLAST
    take record parameter, assumed files read from Bio.SeqIO.index
    Bio.SeqIO.index returns a dictionary like object.

    TODO(Steven Wu): copy/pasted from old main.py. Add test class
    """
    def __init__(self, records, e_value, wdir, outfile=None):
        """
        Constructor
        records: collection of Bio.SeqRecord.SeqRecord
                can be created by Bio.SeqIO.index
                OR dict(key=Bio.SeqRecord.SeqRecord, ...)
        """
        print "weNFASMDN",outfile, wdir
        self.results = dict()
        self.record_index = records
        self.e_value_cut_off = e_value
        self.wdir = wdir
        self.outfile = self.wdir + outfile


    @classmethod
    def create_blast_from_file(cls, filename, e_value, wdir, outfile):
        """
        Class method
        Create RunGlimmer from Setting class
        """
        if os.path.exists(filename):
            record_index = SeqIO.index(filename, "fasta")
            blast = cls(record_index, e_value, wdir, outfile=outfile)
            return blast
        else:
            raise IOError("Blast infile %s does not exist!!! " % filename)
#        setting = setting_class.get_all_par("glimmer")
#        glimmer = RunGlimmer.create_glimmer(setting)




    def run(self):

        print("Running AmiGO:BLAST")

        for key in self.record_index:

            self.seq = Sequence(self.record_index[key].seq) #Bio.SeqRecord.SeqRecord

            self.seq = go_connector.blast_AmiGO(self.seq)
            self.seq = go_connector.extract_ID(self.seq)
            self.seq = go_connector.parse_go_term(self.seq, self.e_value_cut_off)
#            self.seq.all_terms
            self.results[key] = self.seq
            new_dict = self.init_dict(self.results, 0)
            self.counter = self.update_counter_from_dictionaries(new_dict, self.results)
            new_outfile = self.init_output(self.counter,0)
            self.sample = self.update_sample_from_counters(new_outfile, self.counter)
            self.outfile = RunBlast.output_csv()

    @classmethod
    def create_blast_from_setting(cls, setting_class):
        setting = setting_class.get_all_par("blast")
        blast = RunBlast.create_blast_from_file(setting)
        return blast
        pass


    def init_dict(self, allterms, default_value=0):
        default_dict = dict()
        master_value = set([])
        for v in allterms.values():
            master_value=master_value | v

        for k in master_value:
        #            new_dict.setdefault(k, default_value)
            default_dict[k]=default_value
        return default_dict

    def update_counter_from_dictionaries(self, counter, allterms):
    #        print allterms
    #        print(allterms.values())
        for v in allterms.values():
            counter = self.update_counter_from_set(counter,v)

    def update_counter_from_set(self, counter, each_set):
        for k in each_set:
            counter[k] += 1
        return counter
#        for i in self.results.values():
#            print(i.all_terms)

#TODO: Save / export results as a .csv file (= MINE input)

    def init_output(self, counter, default_value=0):
        new_sample = dict()
        master_file = set([])
        for v in counter.values():
            master_file=master_file | v

        for k in master_file:
        #            new_dict.setdefault(k, default_value)
            new_sample[k]=default_value
        return new_sample

    def update_sample_from_counters(self, sample, counter):
        for v in counter.values():
            sample = self.update_sample_from_set(sample, v)

    def update_sample_from_set(self, sample, each_set):
        for k in each_set:
            sample[k]= sample[k]+1
        return sample
    #        for i in self.results.values():
#            print(i.all_terms)

    def output_csv(self, header, template):
        """template should be a dictionary object
        """
        with open(self.outfile, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_NONE)
#            writer.writerow(template)
#            dict.
            firstrow = ["GOterm", header]
            writer.writerow(firstrow)
            for key in template.iterkeys():
                temp=[key, template[key]]
                print temp, type(temp)
                writer.writerow(temp)


    def update_output_csv(self, header, template, existing_csv):
        """
        template = dictionary object
        header = header
        existing_csv = "filename" full path
        """
        with open(self.outfile, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_NONE)
            all_GOterms = set()
            with open(existing_csv, 'rb') as f:
                reader = csv.reader(f)
                for i, row in enumerate(reader):
                    if i==0:
                        zeroes = len(row)-1
                        row.append(header)
                    else:
                        key = row[0]
                        all_GOterms.add(key)
                        if template.has_key(key):
                            row.append(template[key])
                        else:
                            row.append(0)
                    writer.writerow(row)
                print all_GOterms
                for key in template.iterkeys():
                    if key not in all_GOterms:
                        newlist = [key]
                        newlist.extend(["0"]*zeroes)
                        newlist.append(template[key])
                        print newlist
                        writer.writerow(newlist)
#
#                    adder = csv.reader(template)
#
#            if "%s"%key not in f:
#                print key, "is not in the existing csv"
#                #                            add new row with key in row[0]
#                #                            row.append(0) for previous values
#                #                            row.append(key) in "current" location
#                row[0].append(key)
#
#            print i, key, row