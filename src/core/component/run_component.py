import os
from core.utils import path_utils
import warnings

__author__ = 'erinmckenney'


def check_dir_ending(tdir):
    if not tdir.endswith("/"):
        tdir += "/"
#    else:
#        tdir = tdir
    return tdir


class RunComponent(object):

    def __init__(self, pdir, wdir, infile, check_exist=True):
        self.pdir = pdir
        self.wdir = wdir
        self.infile = infile
        self.check_exist = check_exist



#        self.all_exts=[]


    def check_valid_value(self, s, convert):

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

    def check_outfile_filename(self, outfile, outfile_tag):
        """
        infile name
            check if it exist
            overwrite or not
        if os.path.exists(  self.cwd+self.name_only  ):
        if os.path.exists(  full_file_path  ):
        """

        if outfile is None:
            prefix = path_utils.remove_ext(self.infile)
            outfile = prefix + outfile_tag

        outfile = path_utils.check_wdir_prefix(self.wdir, outfile)
        return outfile



    def check_outfiles_with_filetag_exist(self, outfile_tag, debug=True):
        """
        check files with default extensions for each program exist
        Return: is_exist: boolean
                missing_list: list of missing files
        """
        is_exist, missing_list = self._is_multi_files_exist(outfile_tag, self.all_exts, debug=debug)
        return is_exist, missing_list



    def is_file_exist(self, test_file, debug=True):
        """
        check if one file exist
        Return: boolean
        """

        if os.path.exists(test_file):
            is_exist = True
        else:
            is_exist = False
            if debug:
                print("FileNotFound %s" % test_file)  # , os.path.exists(test_file)

        return is_exist



    def _is_multi_files_exist(self, file_tag, all_exts, is_exist=True, debug=True):
        """
        check multiple files exists
        must provide all_exts as []
        return boolean
        """
        all_files_exist = True
        missing_file_list = []
        for ext in all_exts:
            filename = file_tag + ext
            is_exist = self.is_file_exist(filename, debug)
            all_files_exist = all_files_exist and is_exist
            if not is_exist:
                missing_file_list.append(filename)
        return all_files_exist, missing_file_list

    def _check_dir_exist(self, check_exist):
        if check_exist:
            if not os.path.exists(self.wdir):
                raise(IOError("Error: invalid working directory: %s" % self.wdir))
            if not os.path.exists(self.pdir):
                raise(IOError("Error: invalid program directory: %s" % self.pdir))




    def parameter_check(self, outfile, outfile_tag):
        warnings.warn("Deprecated method ", DeprecationWarning)
#         self.check_dirs(pdir, wdir, check_exist)
        self.check_outfile_filename(outfile, outfile_tag)
#         self.check_file_exist(self.infile, check_exist)


    def check_file_exist(self, filename, check_exist):
        warnings.warn("Deprecated method ", DeprecationWarning)
        if check_exist:
            path_utils.check_file(filename)

    def check_dirs(self, pdir, wdir, check_exist):
        warnings.warn("Deprecated method. New setting check all folders first before pares it ", DeprecationWarning)
        self.pdir = check_dir_ending(pdir)
        if wdir is None:
            self.wdir = self.pdir
        else:
            self.wdir = wdir
        self.wdir = check_dir_ending(self.wdir)
        self._check_dir_exist(check_exist)

