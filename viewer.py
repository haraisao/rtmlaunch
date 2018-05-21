#!/usr/bin/env python

import sys
import Tkinter
#import threading

import ScrolledText


class RedirectText(object):
    def __init__(self, text_ctrl):
        self.output = text_ctrl

    def write(self, string):
        self.output.configure(state = 'normal')
        self.output.insert(Tkinter.END, string)
        self.output.configure(state = 'disabled')

class OutViewer(object):
    def __init__(self):
        self.root = Tkinter.Tk()
        self.frame = Tkinter.Frame(self.root)
        self.frame.pack()
  
        self.scrtxt = ScrolledText.ScrolledText(self.frame, state='disabled')
        self.scrtxt.configure(font='TkFixedFont')
        self.scrtxt.pack()


        self.rdtxt = RedirectText(self.scrtxt)
        #sys.stdout = self.rdtxt
    def setStdout(self):
        sys.stdout = self.rdtxt
    
    def resetStdout(self):
        sys.stdout = sys.__stdout__


