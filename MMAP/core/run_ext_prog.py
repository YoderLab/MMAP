'''
Created on Jan 23, 2012

@author: Steven Wu
'''
import os
import subprocess
import sys


def get_platform():
    """
    ignore windows now
    """
    sys_platform = sys.platform
    if sys_platform.startswith('linux'):
        platform = "linux"
    elif sys_platform.startswith('darwin'):
        platform = "mac"
    else:
        print "Unsupport OS: %s" % sys_platform
        sys.exit(-1)
    return platform


class runExtProg(object):
    '''
    self.program_name: program_name
    self._switch: [list], contain all switches required to run the program_name
        self.parameter = property(_switch)
    self.pdir: program directory
    self.output: capture output message
    self.errors: capture error message
    '''
    platform = get_platform()

    def __init__(self, p, pdir=None, length=0, check_OS=False):

        self.program_name = p
        self.init_switch(length)
        self.pdir = pdir
        self.check_platform(check_OS)

    def set_param_at(self, param, position):
        self._switch[position - 1] = str(param)

    def init_switch(self, leng):
        self._switch = [None] * leng

    def get_all_switches(self):
        return self._switch

    def set_switch(self, s):
        self.reset_switch()
        self.add_switch(s)

    parameters = property(get_all_switches, set_switch, doc="switch/parameters")

    def run(self, debug=False):
        """
        Different level of debugging output

        """
        self._command = [self.program_name]
        self._command.extend(self._switch)
        if debug:
            print("debug: _command:\t%s" % (self._command))
        p = subprocess.Popen(self._command, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, cwd=self.pdir)

        self.output, self.errors = p.communicate()
#         print debug
        # TODO Move debug message to each individual program, since they output very different things
        if debug == 1:
            print("debug - output message:\n%s\n===end===\n" % (self.output))
        elif debug > 1 :
            print("debug - output message:\n%s\nerrors message:\n%s \n===end===\n" %
                  (self.output, self.errors))


    def check_platform(self, check_OS):
        """
        Check platform, only check program_name start with "./". so `ls` still work
        ALWAYS append "_platform" to program_name
        """
        if self.pdir is None and check_OS:
            raise TypeError("Error: no value assigned to self.pdir. Current value = %s" % self.pdir)

        if check_OS or self.program_name.find("./") is 0:
            self.name_only = self.program_name[2:len(self.program_name)]
            self.name_only = self.name_only + "_" + runExtProg.platform
#             print check_OS, self.program_name, self.name_only, self.pdir + self.name_only
#             print os.path.join(self.pdir, self.name_only)
            if os.path.exists(os.path.join(self.pdir, self.name_only)):
#                 self.program_name = "./" + self.name_only
                self.program_name = os.path.join(self.pdir, self.name_only)
#                 self.program_name = "/" + self.name_only
#            else:
#                print "ignore platform"

    def add_switch(self, s):
        if isinstance(s, str):
            self._switch.append(s)
        elif isinstance(s, list):
            self._switch.extend(s)
#        print "add_switch: ",s,"\t==",self._switch

    def reset_switch(self):
        self._switch = list()

    def update_switch(self, name, value):
        value = str(value)
        if name in self._switch:
            index = self._switch.index(name)
            self._switch[index + 1] = value
        else:
            self.add_switch([name, value])

    def toggle_switch(self, name, value=None):
        """
        toggle on/off a switch parameter
        value = 1 == on
        value = 0 == off
        """

        if name in self._switch:
            if (value is None) or (not value):
                self._switch.remove(name)
        else:
            if value or (value is None):
                self.add_switch(name)

"""
Global
"""


def which(program):

    fpath, _ = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def is_exe(fpath):
    return os.path.exists(fpath) and os.access(fpath, os.X_OK)




