import os

__author__ = 'erinmckenney'


def check_dir_ending(tdir):
#    print "444444444",tdir
    if not tdir.endswith("/"):
        tdir += "/"
#        print "+++++++",tdir
    else:
        tdir = tdir
    return tdir
#    print "????????", tdir


class RunComponent(object):
    #FIXME: check outfile name for wdir path before adding wdir to self.outfile
    def __init__(self):
        pass
#        self.all_exts=[]

    def parameter_check(self, pdir, wdir, infile, outfile, check_exist, outfile_tag):
        self.check_dirs(pdir, wdir, check_exist)
        self.generate_outfile_name(infile, outfile, outfile_tag)
        self.check_file_exist(self.infile, check_exist)


    def check_file_exist(self, file, check_exist):
        if check_exist:
            if not self.is_file_exist("", file, True):
                raise IOError("Error: file does not exist. %s" % (file))

    def check_dirs(self, pdir, wdir, check_exist):
        self.pdir = check_dir_ending(pdir)
        if wdir is None:
            self.wdir = self.pdir
#            print "33333333", self.wdir
        else:
            self.wdir = wdir
        self.wdir = check_dir_ending(self.wdir)
#        print "5555555", self.wdir
        self._check_dir_exist(check_exist)

    def _check_dir_exist(self, check_exist):
        if check_exist:
            if not os.path.exists(self.wdir):
                raise(IOError("Error: invalid working directory: %s" % self.wdir))
            if not os.path.exists(self.pdir):
                raise(IOError("Error: invalid program directory: %s" % self.pdir))


    def check_valid_value(self, s, convert):
#        FIXME: handle int/float rounding and "int"/"float" properly

        try:
            v = convert(s)
#            print s, v, type(s), type(v)
            if str(v) != str(s):
                raise(ValueError("ValueError: %s " % s))
        except ValueError as e:
            raise ValueError("%s: converting %s to %s" % (e, s, convert))
#        except TypeError as e:
#            raise e
#            if type(s) is str:
#                raise(TypeError("TypeError: %s is str" % s))
#            else:
#                raise(ValueError("ValueError: %s%s " % (e, s)))
        return v

    def generate_outfile_name(self, infile, outfile, outfile_tag):
        """
        infile name
            check if it exist
            overwrite or not
        if os.path.exists(  self.cwd+self.name_only  ):
        if os.path.exists(  full_file_path  ):
        """


        if infile.find(self.wdir) > -1:
            self.infile = infile
        else:
            self.infile = self.wdir + infile


        if outfile is None:
            location = self.infile.rfind(".")
            if location is -1:
                self.outfile = self.infile
            else:
                self.outfile = self.infile[0:location]
#            print "qq", self.infile, self.wdir  , outfile_tag


            if outfile_tag is not None:
                self.outfile = self.outfile + outfile_tag
#            print "mm", self.outfile
        else:
            if outfile.find(self.wdir) > -1:
                self.outfile = outfile
            else:
                self.outfile = self.wdir + outfile

    def check_outfiles_with_filetag_exist(self, outfile_tag):
        """
        check with default exts for each program
        """
        is_exist = self.is_multi_files_exist(outfile_tag, self.all_exts)
        return is_exist

    def is_multi_files_exist(self, file_tag, all_exts, is_exist=True):
        """
        check multiple files exists
        must provide all_exts as []
        return boolean
        """
        for ext in all_exts:
            is_exist = self.is_file_exist(file_tag, ext, is_exist)
        return is_exist

    def is_file_exist(self, file_tag, ext="", is_exist=True):
        """
        check if one file exist
        return boolean
        """
        test_file = "%s%s" % (file_tag, ext)
#        print "%%is_file_exist%%%%%%%%%%%", test_file
        if os.path.exists(test_file):
            is_exist = is_exist and True
        else:
            is_exist = False
            print is_exist, test_file, os.path.exists(test_file)

        return is_exist

