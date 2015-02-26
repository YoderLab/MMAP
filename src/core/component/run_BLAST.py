"""
Created on Feb 13, 2012

@author: Steven Wu
"""
import csv
import datetime
import os
import warnings

from Bio import SeqIO

from core.amigo.go_connector import GOConnector
from core.amigo.go_sequence import GoSequence
from core.component.run_component import RunComponent
from core.setting import Setting
from core.utils import path_utils


ALL_EXTS = [".csv"]
MINE_TAG = "_MINE"


class RunBlast(RunComponent):
    """
    run BLAST
    take record parameter, assumed files read from Bio.SeqIO.index
    Bio.SeqIO.index returns a dictionary like object.

    """
    def __init__(self, e_value, wdir, batch_size=20, infile=None, records=None, outfile=None, debug=False):
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
        self.e_threshold = e_value

        self.record_index = records
        self.check_filenames(infile, records, outfile)
        self.batch_size = self.check_valid_value(batch_size, int)
        self.debug = 1  # debug
#        if comparison_file is not None:
#            self.comparison_file = self.wdir + comparison_file
#            self.check_file_exist(self.comparison_file, True)
#            self.merged_file = path_utils.append_before_ext(self.outfile , MINE_TAG)

        self.all_exts = ALL_EXTS


    @classmethod
    def create_blast_from_file(cls, setting_class):
        """
        Class method
        Create RunGlimmer from Setting class
        """
#        print setting_class.all_setting
        filename = setting_class.get("blast_infile")
        if os.path.exists(filename):
            record_index = SeqIO.index(filename, "fasta")
            blast = cls(
                e_value=setting_class.get("blast_e_value"),
                wdir=setting_class.get("blast_wdir"),
                batch_size=setting_class.get("blast_batch_size"),
                records=record_index,
                outfile=setting_class.get("blast_outfile"),
                )
            return blast
        else:
            raise IOError("Blast infile %s does not exist!!! " % filename)


    @classmethod
    def create_blast_from_setting(cls, setting_class):

        setting = setting_class.get_pars("blast")

        blast = cls(
            wdir=setting.get("wdir"),
            e_value=setting.get("blast_e_value"),
            batch_size=setting.get("blast_batch_size"),
            infile=setting.get("blast_infile"),
            outfile=setting.get("blast_outfile"))
        return blast



    def run(self, debug=False):

        print("Running AmiGO:BLAST_Batch")

#        temp_output = open(self.outfile + "_temp", "w")
        if self.record_index == None:
            self.record_index = SeqIO.index(self.infile, "fasta")
            print "BLAST infile:%s" % self.infile
#         print self.wdir
        self.tempfile = self.wdir + "/AmiGO_Record.temp"
        go = GOConnector(seq_record=self.record_index, max_query_size=self.batch_size,
                         e_value_cut_off=self.e_threshold, tempfile=self.tempfile,
                         debug=self.debug)

        go.amigo_batch_mode()


        all_seqs = go.all_seqs
        all_orfs = dict()
        for seq in all_seqs:
            key = seq.seq_id
            self.results[key] = seq
            all_orfs[key] = seq.combined_terms
#            print this_seq
#            print this_seq.combined_terms
#            temp_output.write("%s \t %s\n" % (key, seq.combined_terms))
#            temp_output.flush()
#        temp_output.close()

        self.counter = self.create_counter(all_orfs)
#        new_outfile = self.init_output(self.counter,0)
#        self.sample = self.update_sample_from_counters(new_outfile, self.counter)
#       hasattr

        output_csv(self.outfile, self.header, self.counter)
#        if hasattr(self, "comparison_file"):
#            print "PRINT self.comparison_file", self.comparison_file
#            self.update_output_csv(self.infile, self.counter)


    def run_single(self, debug=0):
        warnings.simplefilter('always')
        warnings.warn("Deprecated method: run_BLAST.run_single\nBLAST single sequence, slow!! ", DeprecationWarning)

        print("Running AmiGO:BLAST")

        temp_output = open(self.outfile + "_temp", "w")
        if self.record_index == None:
            self.record_index = SeqIO.index(self.infile, "fasta")

        all_orfs = dict()

        for key in self.record_index:
            print key
            this_seq = GoSequence(key, self.record_index[key].seq)  # Bio.SeqRecord.SeqRecord
            this_seq.blast_AmiGO()
            this_seq.extract_ID()
            this_seq.parse_go_term(self.e_threshold)
#            seq.combined_terms
            self.results[key] = this_seq
            all_orfs[key] = this_seq.combined_terms
#            print this_seq
#            print this_seq.combined_terms
            temp_output.write("%s \t %s\n" % (key, this_seq.combined_terms))
#            temp_output.flush()
#        temp_output.close()

        self.counter = self.create_counter(all_orfs)
#        new_outfile = self.init_output(self.counter,0)
#        self.sample = self.update_sample_from_counters(new_outfile, self.counter)
#       hasattr

        output_csv(self.outfile, self.header, self.counter)
#        if hasattr(self, "comparison_file"):
#            print "PRINT self.comparison_file", self.comparison_file
#            self.update_output_csv(self.infile, self.counter)

    def create_counter(self, all_orfs):
        new_dict = self.init_dict(all_orfs, 0)
        counter = self.update_counter_from_dictionaries(new_dict, all_orfs)
        return counter

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
#            print(i.combined_terms)

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
#            print(i.combined_terms)




    def check_filenames(self, infile, records, outfile):
        """
        infile name
            check if it exist
            if yes, append <namebase>.#
        if os.path.exists(  self.cwd+self.name_only  ):
        if os.path.exists(  full_file_path  ):
        """

        if infile == None and records == None:
            raise TypeError("Neither Blast infile nor records variable exists!!! ")

        elif infile is None:
            now = datetime.datetime.now()
            namebase = now.strftime("%Y.%m.%d_%H.%M")

        elif records is None:
            self.infile = path_utils.check_wdir_prefix(self.wdir, infile)
            namebase = None
        else:
            raise TypeError("Blast infile and records both exist! Pick one!")


        if outfile is not None:
            if outfile.endswith(".csv"):
                location = outfile.rfind(".")
                outfile = outfile[0:location]
            self.outfile = path_utils.check_wdir_prefix(self.wdir, outfile)
        elif namebase is None:
            self.outfile = path_utils.remove_ext(self.infile) + ".blast"
        else:
            self.outfile = self.wdir + namebase
        self.header = os.path.basename(self.outfile)

        if not os.path.exists(self.outfile + ".csv"):
            self.outfile = self.outfile + ".csv"
        else:
            version = 1
            while os.path.exists(self.outfile + ".%s.csv" % version):
                version = version + 1
#            print "#####",self.outfile, location
            self.outfile = self.outfile + ".%s.csv" % version





def output_csv(outfile, header, template):
    """template should be a dictionary object
    """
    with open(outfile, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_NONE)
#            writer.writerow(template)
#            dict.
        firstrow = ["GOterm", header]
        writer.writerow(firstrow)
        for key in template.iterkeys():
            temp = [key, template[key]]
            writer.writerow(temp)


def _update_output_csv(outfile, header, template, existing_csv):
    """
    template = dictionary object
    header = header
    existing_csv = "filename" full path
    """
    warnings.simplefilter('always')
    warnings.warn("Deprecated method: run_BLAST._update_output_csv", DeprecationWarning)

    with open(outfile, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_NONE)
        all_GOterms = set()
        with open(existing_csv, 'rb') as f:
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
#                    row.pop(0)
                writer.writerow(row)
#                print all_GOterms
            for key in template.iterkeys():
                if key not in all_GOterms:
                    newlist = [key]
                    newlist.extend([0] * zeroes)
                    newlist.append(template[key])

                    writer.writerow(newlist)
