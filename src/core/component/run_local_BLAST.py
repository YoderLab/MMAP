"""
Created on Feb 24, 2015

@author: Dan Leehr
"""
import csv
import datetime
import os
import warnings

from core.component.run_component import RunComponent
from core.run_ext_prog import runExtProg
from core.go_blast.extract_go_terms import extract
from core.utils import path_utils

BLASTX = './blastx'
BLASTX_OUTFMT = "10 std stitle"
BLASTX_SEG = "yes"
INT_FILE_EXT = '.tmp.csv'
DEFAULT_OUTFILE_EXT = ".blast.csv"
ALL_EXTS = ['.csv']

DB_SWITCH_POSITION = 1  # -db
DB_FILE_POSITION = 2
QUERY_SWITCH_POSITION = 3  # -query
INFILE_POSITION = 4
OUT_SWITCH_POSITION = 5  # -out
OUTFILE_POSITION = 6
EVALUE_SWITCH_POSITION = 7  # -evalue
EVALUE_POSITION = 8
THREAD_SWITCH_POSITION = 9  # -num_threads
THREAD_POSITION = 10
OUTFMT_SWITCH_POSITION = 11  # -outfmt
OUTFMT_POSITION = 12
SEG_SWITCH_POSITION = 13  # -seg
SEG_POSITION = 14

class RunBlast(RunComponent):
    """
    run BLAST

    """
    def __init__(self, infile, pdir, blast_db, wdir=None, outfile=None, check_exist=True, e_value='1e-15', blast_thread=1):
        """

        :param infile: The input sequence to blast
        :param pdir: program dir
        :param wdir: working dir?
        :param outfile: output file to write csv summary
        :param check_exist: check if files exist
        :param e_value: threshhold to provide to blast
        :param blast_db: the local NCBI formatted blast databae
        :return: an initialized RunBlast
        """
        super(RunBlast, self).__init__(pdir, wdir, infile)
        self.all_exts = ALL_EXTS
        self.e_value = e_value
        self.blast_db = blast_db
        self.blast_thread = blast_thread

        self.outfile = self.check_outfile_filename(outfile, ".blast.csv")
        self.intermediate_file = infile + INT_FILE_EXT
        # print "BLAST Setting", self.blast_db, self.infile, self.outfile, self.pdir
        self.blastx = runExtProg(BLASTX, pdir=self.pdir, length=14, check_OS=True)
        # step 2 is a python script.
        self.init_prog()

    @classmethod
    def create_blast(cls, setting):
        """
        Class method
        Create RunBlast from dict()
        """
        blast = cls(infile=setting.get("blast_infile"),
                    pdir=setting.get("blast_pdir"),
                    wdir=setting.get("wdir"),
                    outfile=setting.get("blast_outfile"),
                    check_exist=setting.get("check_exist"),
                    e_value=setting.get("blast_e_value"),
                    blast_db=setting.get("blast_db"),
                    blast_thread=setting.get("blast_thread"))
        return blast

    @classmethod
    def create_blast_from_setting(cls, setting_class):
        """
        Class method
        Create RunBlast from Setting class
        """
#         setting = setting_class.check_parameters_program("blast")
        blast = RunBlast.create_blast(setting_class.all_setting)
        return blast

    def init_prog(self):
        self.blastx.set_param_at('-db', DB_SWITCH_POSITION)
        self.blastx.set_param_at(self.blast_db, DB_FILE_POSITION)
        self.blastx.set_param_at('-query', QUERY_SWITCH_POSITION)
        self.blastx.set_param_at(self.infile, INFILE_POSITION)
        self.blastx.set_param_at('-out', OUT_SWITCH_POSITION)
        self.blastx.set_param_at(self.intermediate_file, OUTFILE_POSITION)
        self.blastx.set_param_at('-evalue', EVALUE_SWITCH_POSITION)
        self.blastx.set_param_at(self.e_value, EVALUE_POSITION)
        self.blastx.set_param_at('-num_threads', THREAD_SWITCH_POSITION)
        self.blastx.set_param_at(self.blast_thread, THREAD_POSITION)
        self.blastx.set_param_at('-outfmt', OUTFMT_SWITCH_POSITION)
        self.blastx.set_param_at(BLASTX_OUTFMT, OUTFMT_POSITION)
        self.blastx.set_param_at('-seg', SEG_SWITCH_POSITION)
        self.blastx.set_param_at(BLASTX_SEG, SEG_POSITION)


    def is_complete(self, debug):
        return self.is_file_exist(self.outfile, debug=debug)

    def run(self, debug=False):
        # Two stages
        # 1. Run local blast
        # 2. extract GO terms

        if self.is_complete(debug):
            print "==Warning: Blast outfiles exist, skip Blast!!!=="
            return

        print 'Running blastx.. debug', debug
        self.blastx.run(debug)
        extract(self.intermediate_file, self.outfile)
        # Should be complete now.
        if not self.is_complete(debug):
            raise(StandardError("Blast did not complete, output file does not exist"))




    def check_outfile_filename_noreplace(self, infile, records, outfile):
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




