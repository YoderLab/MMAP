'''

@author: Steven Wu

require Biopython - 1.58
require numpy - 1.6.1
require SciPy - 0.10.0

not require hcluster - 0.2 http://code.google.com/p/scipy-cluster/
not require matplotlib - 1.1.0 http://matplotlib.sourceforge.net/ 
    matplotlib (and its dep) is only required to plot dendrogram (with "ipython -pylab") 


'''
from Bio import SeqIO
from core.assembler.software_assembler import SoftwareAssembler
from core.sequence import Sequence
from core.setting import Setting
from core.utils import path_utils
import Bio
import numpy
import os
import scipy



print "NumPy version %s" % numpy.__version__
print "SciPy version %s" % scipy.__version__
print "Bio version %s" % Bio.__version__

print Bio.__path__

CWD = os.getcwd()
data_dir = path_utils.get_data_dir(CWD)
print "data dir:\t", data_dir



def setup_database():

    infile = data_dir + "AE014075_subSmall100.fasta"
    infile = data_dir + "MetaSim_bint-454.20e39f4c.fna"
    record_index = SeqIO.index(infile, "fasta") # use index for large file

    return record_index


def main():
    print __name__

    test_run_dir = path_utils.get_data_dir() + "test_run/"


    filepath = test_run_dir + "first_test"
    setting = Setting.create_setting_from_file(filepath)
    assembler = SoftwareAssembler(setting)
    assembler.run()

    filepath = test_run_dir + "2_test"
    setting = Setting.create_setting_from_file(filepath)
    assembler = SoftwareAssembler(setting)
    assembler.run()


def mainBeachMark1():
    print __name__

    test_run_dir = path_utils.get_data_dir() + "benchMark1/"

#
#    cfile = test_run_dir + "primateA/benchMarkControl1"
#    test = ControlFile()
#    test.add_all(cfile)
#    setting = Setting.create_setting_from_controlfile(test)
#    print cfile, setting.all_setting
#    assembler = SoftwareAssembler(setting)
#    assembler.run()

    cfile = test_run_dir + "primateB/benchMarkControl1"
    setting = Setting.create_setting_from_file(cfile)
    print cfile, setting.all_setting
    assembler = SoftwareAssembler(setting)
    assembler.runMine()


    cfile = test_run_dir + "FPV/benchMarkControl1"
    setting = Setting.create_setting_from_file(cfile)
    print cfile, setting.all_setting
    assembler = SoftwareAssembler(setting)
#    assembler.run()


    cfile = test_run_dir + "primateC/benchMarkControl1"
    setting = Setting.create_setting_from_file(cfile)
    print cfile, setting.all_setting
    assembler = SoftwareAssembler(setting)
#    assembler.run()

    cfile = test_run_dir + "primateD/benchMarkControl1"
    setting = Setting.create_setting_from_file(cfile)
    print cfile, setting.all_setting
    assembler = SoftwareAssembler(setting)
#    assembler.run()

#    cfile = test_run_dir + "primateE/benchMarkControl1"
#    test = ControlFile()
#    test.add_all(cfile)
#    setting = Setting.create_setting_from_controlfile(test)
#    print cfile, setting.all_setting
#    assembler = SoftwareAssembler(setting)
#    assembler.run()


def mainBeachMark2():
    print __name__

    test_run_dir = path_utils.get_data_dir() + "BenchMark2/"
    filepath = test_run_dir + "Lac_5k_1/control"
    setting = Setting.create_setting_from_file(filepath)
    print file, setting.all_setting
    assembler = SoftwareAssembler(setting)
    assembler.run()

def runControlFile(filepath):
    setting = Setting.create_setting_from_file(filepath)
    print filepath, setting.all_setting
    assembler = SoftwareAssembler(setting)
    assembler.run()


if __name__ == "__main__":

#    mainBeachMark1()
    test_run_dir = path_utils.get_data_dir() + "BenchMark3/"
#    setting = Setting.create_setting_from_file(test_run_dir + "Lac_5k_2/control")
#    assembler = SoftwareAssembler(setting)
#    assembler.run()

    setting = Setting.create_setting_from_file(test_run_dir + "Lac_5k_0/control")
    assembler = SoftwareAssembler(setting)
#    assembler.run()

    setting = Setting.create_setting_from_file(test_run_dir + "Lac_5k_MINE/control")
    assembler = SoftwareAssembler(setting)
    assembler.run()

#    runControlFile(test_run_dir + "Both_25k_1/control")

#    runControlFile(test_run_dir + "Both_10k_1/control")
#    runControlFile(test_run_dir + "Both_10k_2/control")
#    runControlFile(test_run_dir + "Both_10k_3/control")

#    runControlFile(test_run_dir + "Ecoli_5k_1/control")
#    runControlFile(test_run_dir + "Ecoli_5k_2/control")
#    runControlFile(test_run_dir + "Ecoli_5k_3/control")

#    runControlFile(test_run_dir + "Lac_5k_1/control")
#    runControlFile(test_run_dir + "Lac_5k_2/control")
#    runControlFile(test_run_dir + "Lac_5k_3/control")

#    runControlFile(test_run_dir + "Lac_20k_0/control")
#    runControlFile(test_run_dir + "Lac_20k_1/control")
#    runControlFile(test_run_dir + "Lac_20k_2/control")
#    runControlFile(test_run_dir + "Lac_20k_3/control")
    pass
