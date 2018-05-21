#
#
#
from __future__ import print_function
import sys
import os
import time
import subprocess
import re 

import rtcpkg as pkg
import rtc_handle as rh

__name_server__ = None
__system_editor__ = None

__rtc_home__ = os.getenv('RTC_PKG_HOME')

#
#
def rtse():
  global __system_editor__
  if __system_editor__ :
    if __system_editor__.poll():
      __system_editor__ = subprocess.Popen('RTSystemEditorRCP')
    else:
      print("RTSystemEditor is already running...")
  else:
    __system_editor__ = subprocess.Popen('RTSystemEditorRCP')


#
#
def eSEAT(fname=""):
  res = ""
  _eSEAT_path_ = pkg.findFiles(__rtc_home__, ['eSEAT.py', 'manifest.xml'])
  if _eSEAT_path_ :
    if fname : fname = findFile(fname)
    res = 'python '+ os.path.join(_eSEAT_path_ ,'eSEAT.py ') +fname
  else:
    print ('eSEAT not found.')
  return res

#
#
def findFile(fname, top=None):
  if top == None: top = __rtc_home__
  pth = pkg.findFile(top, fname)
  if pth :
    return os.path.join(pth, fname)
  else:
    return fname

def findFile2(pat, top=None):
  if top == None: top = __rtc_home__
  return pkg.findFile2(top, pat)

#
#
def terminateNameServer():
   global __name_server__
   if __name_server__:
     if __name_server__.poll() == 1:
       __name_server__ = None
     else:
       __name_server__.terminate()
       __name_server__ = None
#
#
def killNameServer():
  if __name_server__ :
    terminateNameServer()
  else:
    os.system("taskkill /F /IM omniNames.exe")
#
#
class RtcMgr(object):
  #
  #
  def __init__(self, argv=[]):
    self.rtm_env = None
    self.argv = argv
    self.object_list={}
    self.root={}
    self.initNS()
    self.name_space = self.rtm_env.name_space['localhost']
    self.update()

  #
  #   
  def initNS(self):
    global __name_server__
    try:
      self.rtm_env = rh.RtmEnv(self.argv)
    except:
      __name_server__ = subprocess.Popen('omniNames')
      self.rtm_env =  rh.RtmEnv(self.argv)
    return self.rtm_env
  #
  def update(self):
    try:
      self.name_space.list_obj()
    except:
      print ("Error in update object list")
  #
  def get_handle_names(self, pat=None):
    res = []
    self.update()
    for name in self.name_space.rtc_handles.keys():
      if pat is None or re.search(pat, name):
       res.append(name)
    return res

  def get_handle(self, pat=None):
    res = []
    self.update()
    for name in self.name_space.rtc_handles.keys():
      if pat is None or re.search(pat, name):
       res.append(self.name_space.rtc_handles[name])
    return res

  def get_port_info(self, name):
    hlist=self.get_handle(name)
    if len(hlist) == 1:
      h=hlist[0]
      res={}
      res['in'] =[]
      res['out']=[]
      res['service']=[]
      for x in h.inports:
        res['in'].append("%s:%s" % (x, h.inports[x].data_type))
        
      for x in h.outports:
        res['out'].append("%s:%s" % (x, h.outports[x].data_type))

      for x in h.services:
        res['service'].append("%s" % (x, ))
      return res

    else:
      print(self.get_handle_names(name))
    return None


#
#
class ProcessManager(object):
  #
  #
  def __init__(self, fname):
    self.popen = None
    self.env = None
    self.setFile( fname )
  #
  #
  def setFile(self, fname):
    self.exec_file_name = fname
    self.pid_file = os.path.basename(fname)+".pid"
  #
  #
  def run(self):
    if os.path.exists(self.pid_file):
      print("Process %s is already running..." % self.exec_file_name)
      return
    try:
      self.popen = subprocess.Popen(self.exec_file_name, env=self.env)
      if not self.popen.poll() :
        with open(self.pid_name, "w") as f:
          f.write(self.popen.pid)
          f.close()
    except:
      pass
  #
  #
  def remove_pid_file(self):
    try:
      os.remove(self.pid_file)
    except:
      pass
  #
  #
  def shutdown(self):
    if self.popen and (not self.popen.poll()) :
      self.popen.terminate()
      if self.popen.poll():
        self.remove_pid_file()


