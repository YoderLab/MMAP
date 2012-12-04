'''

@author: Steven Wu

require Biopython - 1.58
require numpy - 1.6.1
require SciPy - 0.10.0

not require hcluster - 0.2 http://code.google.com/p/scipy-cluster/
not require matplotlib - 1.1.0 http://matplotlib.sourceforge.net/ 
    matplotlib (and its dep) is only required to plot dendrogram (with "ipython -pylab") 


'''
import os
import numpy
import scipy
import Bio


from Bio import SeqIO
from core import controlfile
from core.assembler.software_assembler import SoftwareAssembler
from core.component.run_genovo import RunGenovo
from core.connector import go_connector
from core.controlfile import ControlFile
from core.sequence import Sequence
from core.dist.matching_distance import MatchingDistance
from core.setting import Setting
from core.utils import path_utils


from core.connector.go_connector import GOConnector
from core.component.run_BLAST import RunBlast
from core import run_ext_prog


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


    file="/Users/erinmckenney/Desktop/Pipeline/metaLem/data/test_run/first_test"
    test = ControlFile()
    test.add_all(file)
    setting=Setting.create_setting_from_controlfile(test)
    print setting.all_setting
    assembler = SoftwareAssembler(setting)
#    assembler.run()


    file="/Users/erinmckenney/Desktop/Pipeline/metaLem/data/test_run/second_test"
    test = ControlFile()
    test.add_all(file)
    setting=Setting.create_setting_from_controlfile(test)
    print setting.all_setting
    assembler = SoftwareAssembler(setting)
    assembler.run()


if __name__ == "__main__":
    main()


