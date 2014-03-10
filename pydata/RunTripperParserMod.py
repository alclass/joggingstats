#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
XmlSha1HexFileMod.py
This module contains the XmlSha1HexFile class
'''

import datetime, os, sys
import __init__
from RunTripperMod import Exercise
from RunTripperMod import PointRange
from RunTripperMod import PointTime
from RunTripperMod import Run
from RunTripperMod import RunTripper
from RunTripperMod import Transport

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

tripper = RunTripper()
rundate = datetime.date(year=2014, month=2, day=28)
tripper.set_header(date=rundate, ground=1, co='Carnival.|After a little rain.')

transport = Transport(transport_vehicle=B.B301)

pt1 = PointTime(pt=P.SFXA, t='1h26', te=25)
pt2 = PointTime(pt=P.SFXA, t='1h38', te=25)
point_range = PointRange(pt1, pt2, wait_time=True)
transport.add_point_time_or_range(point_range)

pt1 = PointTime(pt=P.SPEN, t='1h40', te=26)
pt2 = PointTime(pt=P.SPEN, t='1h46', te=26)
point_range = PointRange(pt1, pt2)
transport.add_point_time_or_range(point_range)

point_time = PointTime(pt=P.CMSJ, t='1h53')
transport.add_point_time_or_range(point_time)

point_time = PointTime(pt=P.USIN, t='1h55')
transport.add_point_time_or_range(point_time)

pt1 = PointTime(pt=P.USIN, t='1h56')
pt2 = PointTime(pt=P.USIN, t='2h41')
exercise = Exercise(pt1, pt2)
tripper.add_exercise(exercise)

run = Run(parcours=T.USIN_CLOV, duration='19m45', nstops=0, weight=73, co='Not bearing longer.')
tripper.set_run(run)

print tripper



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
