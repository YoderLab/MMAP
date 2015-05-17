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

BLASTX = './blastx'
BLASTX_OUTFMT = "10 std stitle"
INT_FILE_EXT = '.tmp.csv'
ALL_EXTS = ['.csv']

DB_SWITCH_POSITION = 1          # -db
DB_FILE_POSITION = 2
QUERY_SWITCH_POSITION = 3       # -query
INFILE_POSITION = 4
OUT_SWITCH_POSITION = 5         # -out
OUTFILE_POSITION = 6
EVALUE_SWITCH_POSITION = 7      # -evalue
EVALUE_POSITION = 8
SEG_SWITCH_POSITION = 9         # -seg
SEG_POSITION = 10
OUTFMT_SWITCH_POSITION = 11     # -outfmt
OUTFMT_POSITION = 12

class RunBlast(RunComponent):
    """
    run BLAST

    """
    def __init__(self, infile, pdir, wdir=None, outfile=None, check_exist=True, seg=None, e_value='1e-15', blast_db=None):
        """

        :param infile: The input sequence to blast
        :param pdir: program dir
        :param wdir: working dir?
        :param outfile: output file to write csv summary
        :param check_exist: check if files exist
        :param e_value: threshhold to provide to blast
        :param seg: perform SEG filtering
        :param blast_db: the local NCBI formatted blast databae
        :return: an initialized RunBlast
        """
        self.all_exts = ALL_EXTS
        self.e_value = e_value
        self.seg = seg or "yes"
        self.blast_db = blast_db
        self.parameter_check(pdir, wdir, infile, outfile, check_exist, ".csv")
        self.intermediate_file = infile + INT_FILE_EXT
        self.blastx = runExtProg(BLASTX, pdir=self.pdir, length=12, check_OS=True)
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
                    seg=setting.get("blast_seg"),
                    blast_db=setting.get("blast_db"))
        return blast

    @classmethod
    def create_blast_from_setting(cls, setting_class):
        """
        Class method
        Create RunBlast from Setting class
        """
        setting = setting_class.get_pars("blast")
        blast = RunBlast.create_blast(setting)
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
        self.blastx.set_param_at('-seg', SEG_SWITCH_POSITION)
        self.blastx.set_param_at(self.seg, SEG_POSITION)
        self.blastx.set_param_at('-outfmt', OUTFMT_SWITCH_POSITION)
        self.blastx.set_param_at(BLASTX_OUTFMT, OUTFMT_POSITION)

    def is_complete(self, debug):
        return self.is_file_exist(self.outfile, debug=debug)

    def run(self, debug=False):
        # Two stages
        # 1. Run local blast
        # 2. extract GO terms

        if self.is_complete(debug):
            print "===Warning!!! Blast outfiles already exists, skip Blast!!!==="
            return

        print 'Running blastx'
        self.blastx.run(debug)
        extract(self.intermediate_file, self.outfile)
        # Should be complete now.
        if not self.is_complete(debug):
            raise(StandardError("Blast did not complete, output file does not exist"))

