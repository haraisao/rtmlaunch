#
#
#
from __future__ import print_function
import sys
import os
import time
import subprocess
import re 
import traceback

import shlex

import rtcpkg as pkg
import rtc_handle as rh

__name_server__ = None
__system_editor__ = None

__rtc_home__ = os.getenv('RTC_PKG_HOME')

if __rtc_home__ is None:
  __rtc_home__ = os.getenv('HOME')

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
def eSEAT_cmd(fname=""):
  res = ""
  _eSEAT_path_ = pkg.findFiles(__rtc_home__, ['eSEAT.py', 'manifest.xml'])
  if _eSEAT_path_ :
    if fname : fname = findFile(fname)
    res = 'python '+ os.path.join(_eSEAT_path_ ,'eSEAT.py -v ') +fname
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
    return None

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
      import traceback
      traceback.print_exc()
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
  def __init__(self, fname, stderr=None, stdout=None, stdin=None):
    self.popen = None
    self.env = None
    self.f_out = stdout
    self.f_err = stderr
    self.f_in = stdin
    if fname:
      self.setFile( fname )
  #
  #
  def setFile(self, fname):
    self.exec_file_name = shlex.split(fname)
    self.pid_file = os.path.basename(fname)+".pid"
  #
  #
  def run(self):
    if os.path.exists(self.pid_file):
      print("Process %s is already running..." % self.exec_file_name)
      return
    try:
      self.popen = subprocess.Popen(self.exec_file_name, env=self.env,
         stdout=self.f_out, stdin=self.f_in, stderr=self.f_err)
      #if not self.popen.poll() :
      #  with open(self.pid_name, "w") as f:
      #    f.write(self.popen.pid)
      #    f.close()
    except:
      import traceback
      traceback.print_exc()
      print("Error in run()")
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

class eSEAT(ProcessManager):
  def __init__(self, fname):
    ProcessManager.__init__(self, "")
    self.eSEAT_path = "" 
    self.seatml = fname
    self.find_eSEAT()
    if self.eSEAT_path:
      self.seatml = self.find_seatml(fname)

  def find_eSEAT(self):
    global __rtc_home__
    self.eSEAT_path = pkg.findFiles(__rtc_home__, ['eSEAT.py', 'manifest.xml'])
    if self.eSEAT_path :
      self.eSEAT_path = os.path.join(self.eSEAT_path ,'eSEAT.py')
      print("eSEAT_path = " + self.eSEAT_path)

  def find_seatml(self, fname):
    res = findFile(fname)
    if res:
      print ("Seatml File = "+ res)
      return res
    else:
      print ("Seatml not found: "+fname)
      return fname

  def run(self, opt = ""):
    self.setFile( "python "+self.eSEAT_path + " "+opt+" "+  self.seatml)
    ProcessManager.run(self)


