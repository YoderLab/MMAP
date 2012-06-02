"""
Created on May 30, 2012
@author: Erin McKenney
"""

from core.component.run_component import RunComponent
from core.run_ext_prog import runExtProg

# Full command-line sequence will read as
# ./MetaSim cmd -mg /path.mconf -r### /path.mprf -d /path/output_directory
# <run MetaSim in command mode>
# <use empirical model with specified config file --> alternately, -4 --454 error model>
# <generate ### reads>
# <using specified taxon file or single genome seq in FASTA format>
# <specify output directory>
METASIM = "./MetaSim\ cmd" # .MetaSim cmd
MODEL_INFILE_POSITION = 1
NO_READS_POSITION = 2
TAXON_INFILE_POSITION = 3
OUTFILE_DIRECTORY_POSITION = 4

ALL_EXTS = [".fna"]

class RunMetaSim(RunComponent):
    """
    classdocs
    """

    def __init__(self, model_infile, no_reads, taxon_infile, pdir, wdir=None, outfile=None, check_exist=True):
        """
        Constructor
        """
        self.all_exts = ALL_EXTS
        self.parameter_check(pdir, wdir, model_infile, no_reads, taxon_infile, outfile, check_exist, "_out")
        self.metasim = runExtProg(METASIM, pdir=self.pdir, length=4, check_OS=True)
        self.init_prog()