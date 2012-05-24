"""
Created on Feb 29, 2012

@author: Erin McKenney and Steven Wu
"""
from core.component.run_component import RunComponent

from core.run_ext_prog import runExtProg
from Bio import SeqIO
import os

INFILE_POSITION = 1
INFILE_FINALIZE_POSITION = 3

class RunGenovo(RunComponent):
    """
    classdocs

    """

    def __init__(self, infile, noI, thresh, pdir, wdir=None, outfile=None, checkExist = True):
        """
        Constructor
        TODO: implement finalize
        TODO: read/parse/check output
        
        """

#        super(RunGenovo, self).__init__()
        self.allextw=[".status", ".dump1", ".dump.best"]

        if pdir.endswith("/"):

            self.pdir=pdir
        else:
            self.pdir = pdir+"/"


        self.wdir = wdir
        ## TODO (Steven): use this to demonstrate refactor
        if self.wdir is None:
            self.wdir = self.pdir

        self.infile_class_var = self.wdir+infile


        if outfile is None:
            self.outfile = self.generate_outfile_name(self.infile_class_var,"_out.fasta")
        else:
            self.outfile = self.wdir+outfile

        if checkExist:
            self.check_infile_exist()


        self.assemble = runExtProg("./assemble", pdir=self.pdir, length=2, checkOS=True)
        self.finalize = runExtProg("./finalize", pdir=self.pdir, length=3, checkOS=True)
        self.setInfileName(self.infile_class_var)
        self.set_number_of_iter(noI)
#        print self.assemble.get_switch()
#
#        self.testRandom()
        self.set_finalize_outfile(self.outfile)
        self._set_cutoff(thresh)


    @classmethod
    def create_genovo(cls, setting):
#        :"test_run_infile.fasta", = self.data_dir, :10, 
        genovo = cls(infile=setting.get("genovo_infile"), noI=setting.get("genovo_noI"), thresh=setting.get("genovo_thresh"),
                     pdir=setting.get("genovo_pdir"), wdir=setting.get("wdir") ,outfile=setting.get("genovo_outfile"),
                    checkExist=setting.get("check_exist"))
#        infile, noI, thresh, pdir, wdir=None, outfile=None, checkExist = True):
#        """
#        ["parent_directory","genovo_infile","genovo_pdir","genovo_noI","genovo_thresh","glimmer_pdir"] # dont need outfile
#        self.add_all(**kwargs)
        return genovo

    @classmethod
    def create_genovo_from_setting(cls, setting_class):
    #        :"test_run_infile.fasta", = self.data_dir, :10,
        setting = setting_class.get_all_par("genovo")
        genovo = RunGenovo.create_genovo(setting)
#        genovo = cls(infile=setting.get("genovo_infile"), noI=setting.get("genovo_noI"), thresh=setting.get("genovo_thresh"),
#            pdir=setting.get("genovo_pdir"), wdir=setting.get("wdir") ,outfile=setting.get("genovo_outfile"),
#            checkExist=setting.get("check_exist"))
        #        infile, noI, thresh, pdir, wdir=None, outfile=None, checkExist = True):
        #        """
        #        ["parent_directory","genovo_infile","genovo_pdir","genovo_noI","genovo_thresh","glimmer_pdir"] # dont need outfile
        #        self.add_all(**kwargs)
        return genovo



    def set_number_of_iter(self, param):

        if param>0 and isinstance( param, ( int, long ) ):
            self.assemble.set_param_at(param, 2)
        else:
            raise TypeError, "Error: unacceptable value for param: %s" %param



    def setInfileName(self, infile):
        """
        type anything here
        TODO: check valid infile, infile exist or not
        """
#        if os.path.isdir(infile) != True:
#            infile = self.wdir+infile
#            print("setInfile to", infile)
      
        self.assemble.set_param_at(infile, INFILE_POSITION)
        self.finalize.set_param_at(infile+".dump.best",INFILE_FINALIZE_POSITION)


    def set_finalize_outfile(self, outfile):
        self.finalize.set_param_at(outfile, 2)
#        self.finalize.__switch[1] = str(outfile)
#        print self.finalize.__dict__
#        self._switch[position - 1] = str(param)
    
    def _set_cutoff(self, v):

        if v>0 and isinstance(v, ( int, long ) ):
            self.finalize.set_param_at(v,1)
        else:
            if isinstance(v,str):
                raise TypeError('Error: cutoff set as string "%s"' %v)
            else:
                raise ValueError('Error: cutoff set to:',v)

#    def __le__(self, other):
#        return self.finalize.getNoCutOff() < other.fimalize.getNoCutOff()
#        a = RunG()
#        b = RunG()
#        a <= b
#        a < b

#    def generate_outfile_name(self, infile):
#        """
#        infile name
#               testAssemble.poiuyxcvbjkfastaaaasdfghjk
#        step1: testAssemble
#        step2: testAssemble_out.fasta
#        step3: self.pdir+testAssemble_out.fasta
#            check if it exist
#            overwrite or not
#
#
#        if os.path.exists(  self.cwd+self.name_only  ):
#        if os.path.exists(  full_file_path  ):
#        """
#        location=infile.rfind(".")
#        if location is -1:
#            namebase=infile
#        else:
#            namebase=infile[0:location]
##        print "location", location, infile, infile[0:location]
#        outfile=namebase+"_out.fasta"
#        return outfile



#    def check_infile_exist(self):
#        """
#         TODO: add code to check if these exist
#         check if self.pdir exist
#         check if infile exist
#         check if outfile already exist
#
#         use
#         if os.path.exists( fileName ):
#        """
##        Attempt to refactor code:
##        This chunk should take care of directory and infile check
##        self.infile_path="%s%s" % (self.wdir, self.infile_class_var)
#        querylist = [self.wdir, self.infile_class_var]
#        for item in querylist:
#            if not os.path.exists(item):
#                raise IOError("Error: %s does not exist" %item)
#
###        This chunk checks for a valid directory.
##        print "Directory set to:",self.pdir
##        if os.path.exists(self.pdir):
##            print "Valid directory."
##        else:
###            print
###            sys.exit(-1)
##            raise IOError, "Error: invalid directory:%s" %self.pdir
###        If the directory is valid, this chunk makes sure the infile exists.
##        self.infile_path="%s%s" % (self.pdir, self.infile_class_var)
##        print "Infile path set to:",self.infile_path
##        if os.path.exists(self.infile_path):
##            print "Infile exists."
##        else:
##            print "Error: infile does not exist."
##            raise IOError
##        This chunk makes sure you won't overwrite an existing outfile.
#        self.outfile_path="%s%s" % (self.wdir, self.outfile)
#        if os.path.exists(self.outfile_path):
#            raise IOError("WARNING: outfile already exists!!!")
#        #TODO: come back to this later.
##            Can rename the file, raise a different error, etc.
#        else:
#            pass

#    def check_outfiles_exist(self,  outfile_tag):
        """
        TODO: check if standard outfile from ./assemble exist
        
        start with self.infile_class_var (test_infile.fasta)
        should have 3 output
            test_infile.fasta.status
            test_infile.fasta.dump1
            test_infile.fasta.dump.best
            
        ./assemble_linux test_infile.fasta 1
        still generate test_infile.fasta.status
        
        check 
        *.status
        *.dump1
        *.dump.best
        exist
        
        """
#        allextw=[".status", ".dump1", ".dump.best"]
#        isExist = self.check_multiple_outfiles_existence( outfile_tag, allextw)
#        return isExist


 
    def readFinalizeOutfile(self):
        """
        use SeqIO.index(file, "fast") to read the result seq file, generated from ./finalize
        TODO: check outfile exist, properly generated by ./finalize 
        """
        self.record_index = SeqIO.index(self.outfile, "fasta")
        return self.record_index
    

    def run(self):
        self.assemble.run()
        self.finalize.run()


#


