"""
Created on Feb 13, 2012

@author: Steven Wu
"""
import os
from Bio import SeqIO
import csv
import datetime
from core.connector import go_connector
from core.sequence import Sequence
from core.component.run_component import RunComponent
from core.setting import Setting

ALL_EXTS = [".csv"]

class RunBlast(RunComponent):
    """
    run BLAST
    take record parameter, assumed files read from Bio.SeqIO.index
    Bio.SeqIO.index returns a dictionary like object.

    TODO(Steven Wu): copy/pasted from old main.py. Add test class
    """
    def __init__(self, e_value, wdir, infile=None, records=None, outfile=None, comparison_file=None):
        """
        Constructor
        records: collection of Bio.SeqRecord.SeqRecord
                can be created by Bio.SeqIO.index
                OR dict(key=Bio.SeqRecord.SeqRecord, ...)
        comparison_file = pre-exist result file
        merged_file = merged result
        """
#        print "weNFASMDN",outfile, wdir
        self.results = dict()
        self.wdir = wdir
        self.e_value_cut_off = e_value
        self.record_index = records
        self.generate_outfile_name(infile, records, outfile)
        if comparison_file is not None:
            self.comparison_file = self.wdir + comparison_file
            self.check_file_exist(self.comparison_file, True)
            self.merged_file = self.outfile + "_merge"

        self.all_exts = ALL_EXTS


    @classmethod
    def create_blast_from_file(cls, setting_class):
        """
        Class method
        Create RunGlimmer from Setting class
        """
#        print setting_class.all_setting
#        filename =setting_class.get("blast_infile")
#        if os.path.exists(filename):
#            record_index=SeqIO.index(filename, "fasta")
        blast = cls(
            e_value=setting_class.get("blast_e_value"),
            wdir=setting_class.get("blast_wdir"),
            infile=setting_class.get("blast_infile"),
            outfile=setting_class.get("blast_outfile"),
            comparison_file=setting_class.get("blast_comparison_file"))
        return blast
#        else:
#            raise IOError("Blast infile %s does not exist!!! " % filename)
#        setting = setting_class.get_all_par("glimmer")
#        glimmer = RunGlimmer.create_glimmer(setting)




    def run(self):

        print("Running AmiGO:BLAST")
        if self.record_index == None:
            self.record_index = SeqIO.index(self.infile, "fasta")

        all_orfs = dict()

        for key in self.record_index:

            self.seq = Sequence(self.record_index[key].seq) #Bio.SeqRecord.SeqRecord

            self.seq = go_connector.blast_AmiGO(self.seq)
            self.seq = go_connector.extract_ID(self.seq)
            self.seq = go_connector.parse_go_term(self.seq, self.e_value_cut_off)
#            self.seq.all_terms
            self.results[key] = self.seq


            all_orfs[key] = self.seq.all_terms

        new_dict = self.init_dict(all_orfs, 0)
        self.counter = self.update_counter_from_dictionaries(new_dict, all_orfs)
#        new_outfile = self.init_output(self.counter,0)
#        self.sample = self.update_sample_from_counters(new_outfile, self.counter)
#       hasattr

        self.output_csv(self.infile, self.counter)
        if hasattr(self, "comparison_file"):
            print "PRINT self.comparison_file", self.comparison_file
            self.update_output_csv(self.infile, self.counter)

    @classmethod
    def create_blast_from_setting(cls, setting_class):
        setting = setting_class.get_all_par("blast")
        blast = RunBlast.create_blast_from_file(setting)
        return blast



    def init_dict(self, allterms, default_value=0):
        default_dict = dict()
        master_value = set([])
        for v in allterms.values():
            master_value = master_value | v

        for k in master_value:
        #            new_dict.setdefault(k, default_value)
            default_dict[k] = default_value
        return default_dict

    def update_counter_from_dictionaries(self, counter, allterms):
    #        print allterms
    #        print(allterms.values())
        for v in allterms.values():
            counter = self.update_counter_from_set(counter, v)
        return counter

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
            master_file = master_file | v

        for k in master_file:
        #            new_dict.setdefault(k, default_value)
            new_sample[k] = default_value
        return new_sample

    def update_sample_from_counters(self, sample, counter):
        for v in counter.values():
            sample = self._update_sample_from_set(sample, v)

    def _update_sample_from_set(self, sample, each_set):
        for k in each_set:
            sample[k] = sample[k] + 1
        return sample
    #        for i in self.results.values():
#            print(i.all_terms)




    def generate_outfile_name(self, infile, records, outfile):
        """
        infile name
            check if it exist
            if yes, append <namebase>.#
        if os.path.exists(  self.cwd+self.name_only  ):
        if os.path.exists(  full_file_path  ):
        """

        if infile == None and records == None:
            raise TypeError("Neither Blast infile nor records variable exists!!! ")

        elif infile == None:
            now = datetime.datetime.now()
            namebase = now.strftime("%Y.%m.%d_%H.%M")

        elif records == None:
            if infile.find(self.wdir) > -1:
                self.infile = infile
            else:
                self.infile = self.wdir + infile
            namebase = None
        else:
            raise TypeError("Blast infile and records both exist! Pick one!")

        if outfile is not None:
            self.outfile = self.wdir + outfile
        elif namebase == None:
            self.outfile = self.infile
        else:
            self.outfile = self.wdir + namebase

        if self.outfile.endswith(".csv"):
            location = self.outfile.rfind(".")
            self.outfile = self.outfile[0:location]

        if not os.path.exists(self.outfile + ".csv"):
            self.outfile = self.outfile + ".csv"
        else:

            version = 1
            while os.path.exists(self.outfile + ".%s.csv" % version):
                version = version + 1
#            print "#####",self.outfile, location
            self.outfile = self.outfile + ".%s.csv" % version


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
                temp = [key, template[key]]

                writer.writerow(temp)


    def update_output_csv(self, header, template):
        """
        template = dictionary object
        header = header
        existing_csv = "filename" full path
        """
        with open(self.merged_file, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_NONE)
            all_GOterms = set()
            with open(self.comparison_file, 'rb') as f:
                reader = csv.reader(f)
                for i, row in enumerate(reader):
                    if i == 0:
                        zeroes = len(row) - 1
                        row.append(header)
                    else:
                        key = row[0]
                        all_GOterms.add(key)
                        if key in template:
                            row.append(template[key])
                        else:
                            row.append(0)
                    row.pop(0)
                    writer.writerow(row)
                print all_GOterms
                for key in template.iterkeys():
                    if key not in all_GOterms:
#                        newlist = [key]
                        newlist = (["0"] * zeroes)
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
