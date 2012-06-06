import os

__author__ = 'erinmckenney'


def check_dir_ending(tdir):
    if not tdir.endswith("/"):
        tdir = tdir + "/"
    return tdir


class RunComponent(object):

    def __init__(self):
        pass
#        self.all_exts=[]

    def parameter_check(self, pdir, wdir, infile, outfile, check_exist,
                        outfile_tag):
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
            wdir = self.pdir
        self.wdir = check_dir_ending(wdir)
        self._check_dir_exist(check_exist)

    def _check_dir_exist(self, check_exist):
        if check_exist:
            if not os.path.exists(self.wdir):
                raise IOError("Error: invalid working directory: %s" % self.wdir)
            if not os.path.exists(self.pdir):
                raise IOError("Error: invalid program directory: %s" % self.pdir)

    def generate_outfile_name(self, infile, outfile, outfile_tag):
        """
        infile name
            check if it exist
            overwrite or not
        if os.path.exists(  self.cwd+self.name_only  ):
        if os.path.exists(  full_file_path  ):
        """
        self.infile = self.wdir + infile
        if outfile is None:
            location = infile.rfind(".")
            if location is -1:
                namebase = infile
            else:
                namebase = infile[0:location]
            self.outfile = self.wdir + namebase + outfile_tag
        else:
            self.outfile = self.wdir + outfile

    def check_outfiles_exist(self, outfile_tag):
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
        if os.path.exists(test_file):
            is_exist = is_exist and True
        else:
            is_exist = False

        return is_exist

