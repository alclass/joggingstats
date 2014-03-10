#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
XmlSha1HexFileMod.py
This module contains the XmlSha1HexFile class
'''

import os, sys
import __init__


class PointTime(object):
  
  def __init__(self, pt, t=None, temperature=None, comment=None):
    self.pt = pt
    self.t  = t
    self.temperature = temperature
    self.comment     = comment

class PointRange(object):

  def __init__(self,  pt1, pt2, wait_time=False):
    self.pt1 = pt1
    self.pt2 = pt2
    self.wait_time = wait_time

class Transport(object):

  def __init__(self, transport_vehicle=None):
    self.transport_vehicle = transport_vehicle
    self.point_times = []
    
  def add_point_time_or_range(self, point_time_or_range):
    self.point_times.append(point_time_or_range)

class Exercise(PointRange):

  def __init__(self, pt1, pt2, comment=None): # duration is calculated
    super(Exercise, self).__init__(pt1, pt2)
    self.comment = comment

class Run(object):
  
  def __init__(self, parcours=None, duration=None, nstops=0, weight=None, raintype=0, comment=None):
    self.parcours = parcours
    self.duration = duration
    self.nstops   = nstops
    self.weight   = weight
    self.raintype = raintype
    self.comment  = comment

  
class RunTripper(object):
  
  def __init__(self):
    self.date        = None
    self.ground      = None
    self.comment     = None
    self.transports  = []
    self.exercises   = []
    self.run         = None

  def set_header(self, date=None, ground=1, comment=None):
    self.date    = date
    self.ground  = ground
    self.comment = comment
        
  def add_transport(self, transport):
    self.transports.append(transport)

  def add_exercise(self, exercise):
    self.exercises.append(exercise)

  def set_run(self, run):
    self.run = run


class P:
  SFXA = 1
  SPEN = 2
  CMSJ = 3
  USIN = 4
  ALTO = 5
  CARM = 6
  CLOV = 7
  PARE = 8
  SUJI = 9    

class A:
  RUN = 1
  EXE =2
  
class T:
  USIN_CLOV = 1
  USIN_PARE = 2
  USIN_MARQ = 3
  ALTO_USIN = 4
   
class B:
  B301 = 1
  B333 = 2
  B415 = 3
  B426 = 4

  
runregs=[]
runreg = '''
date:'2014-2-28', ground:1, co:'Carnival.|After a little rain.'
pt:P.SFXA, t:'1h26', t2:'1h38', te:25, transp:B.B301
pt:P.SPEN, t1:'1h40', t2:'1h46', te:26
pt:P.CMSJ, t:'1h53'
pt:P.USIN, t:'1h55'
ativ:A.EXE, t1:'1h56', t2:'2h41'
ativ:A.RUN, parcours:T.USIN_CLOV, rt:'19m45', nstops:0, wei:73, co:'Not bearing longer.'
'''

#runregs.append(runreg)
runreg = '''
'date':'2014-3-2', 'ground':1, 'co':'Carnival' 
'pt':P.SFXA, 't1':'1h50', 't2':'2h4', 'te':25, 'transp':B.B415
'pt':P.SPEN, 't1':'2h5', 't2':'2h8', 'te':25
'pt':P.CMSJ, 't':'2h19'
'pt':P.USIN, 't':'2h23'
'ativ':A.EXE, 't1':'2h24', 't2':'3h9'
'ativ':A.RUN, 'parcours':T.USIN_MARQ, 'rt':'29m44', 'nstops':0, 'wei':73, 'co':'Not too hot.'
'pt':P.SUJI, 't':'3h38'
'ativ':A.EXE, 't1':'3h43', 't2':'3h57'
'''
runregs.append(runreg)


#date=1;ground=1;co=1;pt=1;t=1;t1=1;t2=1;te=1;transp=1;ativ=1;rt=1;wei=1;nstops=1;parcours=1

def process_line(line):
  pp = line.split(',')
  for i, p in enumerate(pp):
    key_colon_value = p.split(':')
    key = "eval('%s')" %key_colon_value[0]
    key_colon_value[0] = key
    pp[i] = ':'.join(key_colon_value)
  newline = ','.join(pp)  
  newline = '{%s}' %newline
  print newline
  return newline

def process():
  for runreg in runregs:
    lines=runreg.split('\n')
    for line in lines:
      if line=='':
        continue
      if line.find(':') < 0:
        continue
      newline = 'd = {%s}' %line
      # newline = process_line(line)
      exec(newline)
      print d
  
if __name__ == '__main__':
  process()
