'''

@author: Steven Wu

dependency: 
NumPy version 1.8.2
SciPy version 0.12.1
Bio version 1.65

Example: change to ./src/ folder


python src/core/main.py -h;python src/core/main.py summary -h; python src/core/main.py process -h;
python src/core/main.py -h
python src/core/main.py summary -h
python src/core/main.py process -h

python src/core/main.py process -i data/example/MMAP_example.fasta
python src/core/main.py summary -m data/example/


'''

import argparse
import os
import sys

import Bio
import numpy
import scipy

from core.assembler.software_assembler import SoftwareAssembler
from __init__ import __version__, __author__, __description__


MMAP_DESCRIPTION = __description__
MMAP_VERSION = __version__
MMAP_AUTHOR = __author__

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



def main():
    print __name__

if __name__ == "__main__":



    parser = argparse.ArgumentParser(
        prog="MMAP",
        description=MMAP_DESCRIPTION,
        formatter_class=CustomSingleMetavarFormatter,
#         formatter_class=argparse.RawDescriptionHelpFormatter,
        )
    version_string = "%(prog)s " + MMAP_VERSION

    parser.add_argument(
        "-v", "--version",
        action='version',
        version=version_string,
        help="Print MMAP version"
        )

    # debug level 1 - external program output only
    # debug level 2 - external program output and errors
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument(
        "-d", "--debug", action="count", default=0,
        help="Debugging level. Available options: -d, -dd [default: 0]")
    common_parser.add_argument(
        "-c", "--control", metavar="",
        dest="control_file",
        default="./control",
        help="Control File contains all settings [default ./control]")

#

    subparsers = parser.add_subparsers(
        title='subcommands',
        metavar="<subcommand>",
        dest='sub_command',
        description="Available subcommands: ",  # To view help info of a command, use '<command> -h/--help'",
        help="To view help info of a command, use '<subcommand> -h/--help'",  # "Print usage and help info.
#         formatter_class=CustomSingleMetavarFormatter
        )

#     help_str = "Print usage and help info. To view help info of a command, use '<command> -h/--help'"
#     parser_help = subparsers.add_parser('help', help=help_str)

    parser_summary = subparsers.add_parser(
        'summary', parents=[common_parser],
        help="Calculate MINE statistics",
        formatter_class=CustomSingleMetavarFormatter)
#     parser_summary.set_defaults(which='MINE')
    parser_summary_required = parser_summary.add_argument_group('Required arguments')
    parser_summary_required.add_argument(
        "-m", "--mine_csv", metavar="", dest="csv_dir",
        required=True, help="Folders contains *.csv files for MINE. MINE will summarise all *.csv files (except the one produced by MINE) in this directory")

    parser_summary.add_argument(
        "-t", "--temp_mine", metavar="", dest="mine_infile",
        help="temporary MINE input file [default tempMineInfile]", default="tempMineInfile")
    parser_summary.add_argument(
        "--overwrite", dest="mine_overwrite",
        help="overwrite MINE result files", action='store_true')



    parser_process = subparsers.add_parser(
        'process', parents=[common_parser],
        help="Run Genovo, Glimmer, Blast",
        formatter_class=CustomSingleMetavarFormatter)
    parser_summary_required = parser_process.add_argument_group('Required arguments')
    parser_summary_required.add_argument(
        "-i", "--infile", metavar="", dest="infile",
        required=True, help="Infile for genovo (fasta format)")



    try:
        args = parser.parse_args()
        #     args = vars(parser.parse_args())
    except IOError as e:
        print e
#         warnings.warn(e)
        sys.exit(8)

#     data_dir = path_utils.get_data_dir(CWD)
#     print data_dir
    args.debug = 2
    if args.debug == 2:
        print "Debug level 2"
        print "All args:", args
    elif args.debug == 1:
        print "Debug level 1"
        CWD = os.getcwd()
        print "Current working directory %s" % CWD
        print "NumPy version %s" % numpy.__version__
        print "SciPy version %s" % scipy.__version__
        print "Bio version %s at %s" % (Bio.__version__, Bio.__path__)


    assembler = SoftwareAssembler.create_from_args(args)
#     sys.exit(12)
    assembler.run()


#
#    assembler = SoftwareAssembler.create_from_args(args)
#    assembler.run()
    print "== END MMAP=="

