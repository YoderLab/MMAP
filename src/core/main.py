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
import sys

import Bio
import numpy
import scipy

from core.assembler.software_assembler import SoftwareAssembler
from core.utils import path_utils
from argparse import HelpFormatter
from _ast import TryExcept
import warnings


class CustomSingleMetavarFormatter(argparse.HelpFormatter):

    def __init__(self, prog,
                 indent_increment=2,
                 max_help_position=50,
                 width=None):
        super(CustomSingleMetavarFormatter, self).__init__(prog, indent_increment, max_help_position, width)

#     self._max_help_position = 50
    def _format_action_invocation(self, action):
        if not action.option_strings:
            metavar, = self._metavar_formatter(action, action.dest)(1)
            return metavar
        else:
            parts = []
            # if the Optional doesn't take a value, format is:
            #    -s, --long
            if action.nargs == 0:
                parts.extend(action.option_strings)

            # if the Optional takes a value, format is:
            #    -s ARGS, --long ARGS
            # change to
            #    -s, --long ARGS
            else:
                default = action.dest.upper()
                args_string = self._format_args(action, default)
                for option_string in action.option_strings:
                    # parts.append('%s %s' % (option_string, args_string))
                    parts.append('%s' % option_string)
                parts[-1] += ' %s' % args_string
            return ', '.join(parts)






# print "data dir:\t", data_dir
def main():
    print __name__


if __name__ == "__main__":



    parser = argparse.ArgumentParser(prog="MMAP", formatter_class=CustomSingleMetavarFormatter)
#                                     usage='%(prog)s -i INFILE -c CONTROL [OPTIONS]'

    group1 = parser.add_argument_group('Global arguments')
    group1.add_argument(
        "-i", "--infile", metavar="INFILE", dest="infile",
        required=True, help="Infile for genovo")
    group1.add_argument(
        "-c", "--control", metavar="CONTROL", dest="control_file",
        required=True, help="Control File contains all settings")

    parser.add_argument("-d", "--debug", action="count", default=0,
                        help="increase debugging level")
    # debug level 1 - external program output only
    # debug level 2 - external program output and errors

#
#     subparsers = parser.add_subparsers(
#         title='subcommands', description='valid subcommands',
#         help='additional help')
#     parser_create = subparsers.add_parser('summary', help="MINE stats", formatter_class=CustomSingleMetavarFormatter)
#     parser_create.set_defaults(which='MINE')
#     parser_create.add_argument("-i", "--infileDir", metavar="INDIR", dest="infile_dirs",
#         required=True, help="Infile for MINE")
#
#     group1 = parser_create.add_argument_group('Global arguments')
# #     group1.add_argument(
# #         "-i", "--infile", metavar="INFILE", dest="infile",
# #         required=True, help="Infile for genovo")
#     group1.add_argument(
#         "-c", "--control", metavar="CONTROL", dest="control_file",
#         required=True, help="Control File contains all settings")
#
# #         '--first_name', required=True, help='First Name')
# #     parser_create.add_argument(
# #         '--last_name', required=True, help='Last Name')
#     parser_process = subparsers.add_parser('process', help="Genovo, Glimmer, Blast", formatter_class=CustomSingleMetavarFormatter)
#     parser_process.add_argument(
#         "-i", "--infile", metavar="INFILE", dest="infile",
#         required=True, help="Infile for genovo")
#     #     parser_delete = subparsers.add_parser('delete')
# #     parser_delete.set_defaults(which='delete')
# #     parser_delete.add_argument(
# #         'id', help='Database ID')
# #     args = vars(parser.parse_args())


#     test_run_dir = path_utils.get_data_dir() + "BenchMark3/"
#     cFile = test_run_dir + "Lac_5k_2/control"

#     test_run_dir = path_utils.get_data_dir() + "BenchMark3/Lac_5k_0/"
# test_run_dir = path_utils.get_data_dir() + "BenchMark2/Lac_20k_0/"
#     cFile = "/home/steven/Postdoc/Project_Lemur/MMAP/data/BenchMark10/10k_0/control"


    try:
        args = parser.parse_args()
    except IOError as e:
        print e
#         warnings.warn(e)
        sys.exit(8)

    CWD = os.getcwd()
    data_dir = path_utils.get_data_dir(CWD)
    print CWD
    print data_dir


    if args.debug >= 2:
        print "Debug level 2"
    if args.debug >= 1:
        print "NumPy version %s" % numpy.__version__
        print "SciPy version %s" % scipy.__version__
        print "Bio version %s at %s" % (Bio.__version__, Bio.__path__)

    else:
        pass
#        print "v==0"
    args.debug = 1
    assembler = SoftwareAssembler.create_from_args(args)
#     sys.exit(12)
    assembler.run()


#    cFile = test_run_dir + "Lac_5k_MINE/control"
#    args = parser.parse_args([cFile])
#
#    assembler = SoftwareAssembler.create_from_args(args)
#    assembler.run()
#    print "=== END MAIN ==="

