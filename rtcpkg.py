#
#
from __future__ import print_function
import sys,os

def getTopDir():
    top = os.getenv('RTC_PKG_HOME')
    if not top: top=os.getenv('HOME')
    if not top: top=os.getenv('HOMEPATH')
    return top

def getFileList(pth):
    files = os.listdir(pth)
    return [f for f in files if os.path.isfile(os.path.join(pth, f))]

def getDirList(pth):
    files = os.listdir(pth)
    return [f for f in files if os.path.isdir(os.path.join(pth, f))]
