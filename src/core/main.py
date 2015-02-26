'''

@author: Steven Wu

dependency: Biopython - 1.58
dependency: numpy - 1.6.1
dependency: SciPy - 0.10.0


Example:
change to ./src/ folder

cd src/
python core/main.py ../data/BenchMark3/Lac_5k_0/control
python core/main.py ../data/BenchMark3/Lac_5k_MINE/control

'''
import argparse
import os

import Bio
import numpy
import scipy

from core.assembler.software_assembler import SoftwareAssembler
from core.utils import path_utils
import ConfigParser
import sys
import StringIO


CWD = os.getcwd()
data_dir = path_utils.get_data_dir(CWD)
# print "data dir:\t", data_dir


def main():
    print __name__


if __name__ == "__main__":
    #     webpage = "aoeuaoeuoe\!-- session_id = 1231amigo122 --aoeu"
    #     wb = WebSession(webpage, "10")
    #     wb.query_page = webpage
    #     a = wb.get_session_id()
    #     print a

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "controlFile", help="Control File contains all settings")
    parser.add_argument("-d", "--debug", action="count", default=0,
                        help="increase debugging level")
    # debug level 1 - external program output only
    # debug level 2 - external program output and errors


#     test_run_dir = path_utils.get_data_dir() + "BenchMark3/"
#     cFile = test_run_dir + "Lac_5k_2/control"

#     test_run_dir = path_utils.get_data_dir() + "BenchMark3/Lac_5k_0/"
# test_run_dir = path_utils.get_data_dir() + "BenchMark2/Lac_20k_0/"
#     cFile = "/home/steven/Postdoc/Project_Lemur/MMAP/data/BenchMark10/10k_0/control"


#    args = parser.parse_args(["-h"])
#     args = parser.parse_args([cFile, "-d"])
    args = parser.parse_args()

    print "NumPy version %s" % numpy.__version__
    print "SciPy version %s" % scipy.__version__
    print "Bio version %s at %s" % (Bio.__version__, Bio.__path__)

    if args.debug >= 2:
        print "Debug level 2"
    elif args.debug == 1:
        pass
#        print "v==1"
    else:
        pass
#        print "v==0"

    assembler = SoftwareAssembler.create_from_args(args)

    sys.exit(2)
    assembler.run()


#    cFile = test_run_dir + "Lac_5k_MINE/control"
#    args = parser.parse_args([cFile])
#
#    assembler = SoftwareAssembler.create_from_args(args)
#    assembler.run()
#    print "=== END MAIN ==="
