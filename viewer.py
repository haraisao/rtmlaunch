#!/usr/bin/env python

# Built-in modules
import sys
import logging
import Tkinter
import threading

import ScrolledText


class RedirectText(object):
    def __init__(self, text_ctrl):
        self.output = text_ctrl

    def write(self, string):
        """"""
        self.output.insert(Tkinter.END, string)
 

class MyViewer(object):

    def __init__(self):
        self.root = Tkinter.Tk()
        self.frame = Tkinter.Frame(self.root)
        self.frame.pack()
  
        self.scrtxt = ScrolledText.ScrolledText(self.frame)
        self.scrtxt.configure(font='TkFixedFont')
        self.scrtxt.pack()


        self.rdtxt = RedirectText(self.scrtxt)
        #sys.stdout = self.rdtxt

