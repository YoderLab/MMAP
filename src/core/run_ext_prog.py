'''
Created on Jan 23, 2012

@author: Steven Wu
'''
import subprocess
import copy

class runExtProg(object):
    '''
    self.program: program name
    self.switch: [list], contain all switches required to run the program
    self.cwd: working directory
    self.output: capture output message
    self.errors: capture error message
    '''


    def __init__(self, p):
        
        self.program = [p]
        self.reset_switch()
        self.cwd = None
        
    ## TODO: maybe convert self.switch to __switch
    def append_switch(self, s):
        if isinstance(s, str):
            self.switch.append(s)
        elif isinstance(s, list):
            self.switch.extend(s)
#        print "add_switch: ",s,"\t==",self.switch
    
    def set_switch(self, s):    
        self.reset_switch()
        self.append_switch(s);
        
    def reset_switch(self):
        self.switch = list()
        
    def run(self):
        self.__command = copy.copy(self.program)
        self.__command.extend(self.switch)
        p = subprocess.Popen(self.__command,stdout= subprocess.PIPE, stderr=subprocess.PIPE, cwd = self.cwd )
        self.output, self.errors = p.communicate()
        ## Note The data read is buffered in memory, so do not use this method if the data size is large or unlimited.
        
        