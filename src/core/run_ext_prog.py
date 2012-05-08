'''
Created on Jan 23, 2012

@author: Steven Wu
'''
import subprocess
import os
import sys



def get_platform():   
    """
    ignore windows now
    """
    sys_platform = sys.platform 
    if sys_platform.startswith('linux'):
        platform="linux"
    elif sys_platform.startswith('darwin'):
        platform="mac"
    else:
        print "Unsupport OS: %s" % sys_platform
        sys.exit(-1)
    return platform






class runExtProg(object):
    '''
    self.program_name: program_name
    self._switch: [list], contain all switches required to run the program_name
        self.parameter = property(_switch) 
    self.cwd: working directory
    self.output: capture output message
    self.errors: capture error message
    '''
    platform = get_platform()
    

    def __init__(self, p, pdir=None, length=0, checkOS=False):

        self.program_name = p

        self.init_switch(length)
        self.cwd = pdir
        self.checkPlatform(checkOS)
        


    def set_param_at(self, param, position):
        self._switch[position - 1] = str(param)


    def init_switch(self, leng):
        self._switch = [None]*leng

    def get_switch(self):
        return self._switch


    """
    ignore here here
    """
    def set_switch(self, s):
        self.reset_switch()
        self.add_switch(s);
        
    parameters = property( get_switch, set_switch, doc="switch/parameters" ) 
    
    
    def run(self):
        self._command = [self.program_name]
        self._command.extend(self._switch)
        print(self._command, self.cwd)
        p = subprocess.Popen(self._command,stdout= subprocess.PIPE, stderr=subprocess.PIPE, cwd = self.cwd )
        self.output, self.errors = p.communicate()
#        print self.output, self.errors


    '''
    ignore below for now
    '''
    def checkPlatform(self, checkOS):
        """
        Check platform, only check program_name start with "./". so `ls` still work
        ALWAYS append "_platform" to program_name 
        """
        if self.cwd is None and checkOS:
            raise TypeError("Error: no value assigned to self.cwd. Current value = %s" %self.cwd)
#            sys.exit(4)

        if checkOS or self.program_name.find("./") is 0:
            self.name_only = self.program_name[2:len(self.program_name)]
            self.name_only = self.name_only + "_" + runExtProg.platform

            if os.path.exists(self.cwd+self.name_only):
                self.program_name = "./"+self.name_only
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


    
    def updateSwitch(self, switchName, switchValue):
        switchValue = str(switchValue)
        if switchName in self._switch:
            self._index = self._switch.index(switchName)
            self._switch[self._index + 1] = switchValue
            self._switch[self._index+1] = switchValue
        else:
            self.add_switch([switchName, switchValue])
            

    def toggleSwitch(self, switchName, switchValue=None):
        """
        toggle on/off a switch parameter
        switchValue = 1 == on
        switchValue = 0 == off
        """
        
        if switchName in self._switch:
            if (switchValue is None) or (not switchValue):
                self._index = self._switch.index(switchName)
                self._switch.remove(switchName)
        else:
            if switchValue or (switchValue is None):
                self.add_switch(switchName)


    
    
'''
Global
'''


def which(program):

    fpath, fname = os.path.split(program)
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
        



