'''
Created on Jan 23, 2012

@author: Steven Wu
'''
import subprocess
import copy

class runExtProg(object):
    '''
    self.program: program name
    self._switch: [list], contain all switches required to run the program
    self.cwd: working directory
    self.output: capture output message
    self.errors: capture error message
    '''


    def __init__(self, p, pdir=None, len=0):
        
        self.program = [p]
        self.init_switch(len)
        self.cwd = pdir
        
    
    def add_switch(self, s):
        if isinstance(s, str):
            self._switch.append(s)
        elif isinstance(s, list):
            self._switch.extend(s)
#        print "add_switch: ",s,"\t==",self._switch
    
    def set_switch(self, s):    
        self.reset_switch()
        self.add_switch(s);
        
    def reset_switch(self):
        self._switch = list()

    def init_switch(self, len):
        self._switch = []*len

    def get_switch(self):
        return self._switch
        
    parameters = property( get_switch, set_switch, doc="switch/parameters" ) 
    
    
    def run(self):
        self._command = copy.copy(self.program)
        self._command.extend(self._switch)
        p = subprocess.Popen(self._command,stdout= subprocess.PIPE, stderr=subprocess.PIPE, cwd = self.cwd )
        self.output, self.errors = p.communicate()
        
    
    def updateSwitch(self, switchName, switchValue):
        switchValue = str(switchValue)
        if switchName in self._switch:
            self._index = self._switch.index(switchName)
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

    def set_param_at(self, param, position):
        self._switch[position-1]=param


                
