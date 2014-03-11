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

from Constants import A, B, P, T
  
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
tripper.set_header(date=rundate, ground=True, comment='Carnival.|After a little rain.')

transport = Transport(transport_vehicle=B.B301)

pt1 = PointTime(pt=P.SFXA, t='1h26', temperature=25)
pt2 = PointTime(pt=P.SFXA, t='1h38', temperature=25)
point_range = PointRange(pt1, pt2, wait_time=True)
transport.add_point_time_or_range(point_range)

pt1 = PointTime(pt=P.SPEN, t='1h40', temperature=26)
pt2 = PointTime(pt=P.SPEN, t='1h46', temperature=26)
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

run = Run(parcours=T.USIN_CLOV, duration='19m45', nstops=0, weight=73, comment='Not bearing longer.')
tripper.set_run(run)

print tripper


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

newformat = '''
trip:20140228 gnd |Carnival.|After a little rain.

begin_transp
ve:B301

begin_wait_time
pt: SFXA 1h26 25
pt: SFXA 1h38 25
end_wait_time

pt: SPEN 1h40 26
pt: SPEN 1h46 26

pt: CMSJ 1h53
pt: USIN 1h55
end_transp

begin_exerc
pt: USIN 1h56
pt: USIN 2h41
end_exerc

run: USIN_CLOV 19m45 0 73 |Not bearing longer
'''



def process():
  pass
  
if __name__ == '__main__':
  process()
