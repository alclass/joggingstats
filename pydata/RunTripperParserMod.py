#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
XmlSha1HexFileMod.py
This module contains the XmlSha1HexFile class
'''

import datetime, os, sys
import __init__
import local_settings as ls
from RunTripperMod import Exercise
from RunTripperMod import PointRange
from RunTripperMod import PointTime
from RunTripperMod import WaitTime
from RunTripperMod import Run
from RunTripperMod import RunTripper
from RunTripperMod import Transport

from Movements import Location, Parcours, TransportVehicle, RainType, TokenAndValueError
  
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
#clean_empty_lambda = lambda e : e if e != ''
#clean_empty_map = filtermap(clean_empty_lambda, l)  


def clean_empty_strs(pp):
  newpp = []
  for e in pp:
    if len(e) > 0:
      newpp.append(e)
  return newpp 

def clean_str_and_split_by_blanks(s):
  s = s.lstrip(' \t').rstrip(' \t\r\n')
  pp = s.split(' ')
  pp = clean_empty_strs(pp)
  return pp

def pydate_from_8str(date8str):
  pydate = None
  try:
    year  = int(date8str[:4])
    month = int(date8str[4:6])
    day   = int(date8str[6:8])
    pydate = datetime.date(year, month, day)
  except ValueError:
    pass
  except IndexError:
    pass
  return pydate 

class DataFlowError(ValueError):
  pass

def get_comments_by_vertical_bars_if_any(rem_line):
  pos_vertical_bar = rem_line.find('|')
  if pos_vertical_bar > -1:
    comment = rem_line[ pos_vertical_bar + 1 : ]
    return comment
  return None


def scrape_point_time(line):
  if not line.startswith('pt:'):
    return None
  s = line[ len('pt:') : ]
  pp = clean_str_and_split_by_blanks(s)
  location_token = None
  hstr_time = None
  temperature = None
  try:
    location_token = pp[0]
    hstr_time      = pp[1]
    temperature    = int(pp[2])
  except ValueError:
    pass
  except IndexError:
    pass
  if location_token == None or hstr_time == None:
    return None
  location = Location(location_token)
  point_time = PointTime(location=location, t=hstr_time, temperature=temperature)
  return point_time 

def look_ahead_section_and_return_wait_time(lines):
  point_times = []
  for line in lines:
    if line.startswith('e_wait'):
      if len(point_times) != 2:
        raise DataFlowError, 'len(point_times)=%d != 2' %len(point_times)
      pt1 = point_times[0]
      pt2 = point_times[1]
      wait_time = WaitTime(pt1, pt2)
      return wait_time 
    elif line.startswith('pt:'):
      pt = scrape_point_time(line)
      if pt != None:
        point_times.append(pt)
  raise DataFlowError, '[e_transp] marker did not finished a transport section in data file.'
    
def look_ahead_section_and_return_transport_obj(lines):
  transport = None
  for i, line in enumerate(lines):
    if line.startswith('ve:'):
      rem_line = line[ len('ve:') : ]
      transport_token = rem_line.lstrip(' \t').rstrip(' \t\r\n')
      transport_vehicle = TransportVehicle(transport_token)
      transport = Transport(transport_vehicle)
    elif line.startswith('b_wait'):
      wait_time = look_ahead_section_and_return_wait_time(lines[i+1:])
      transport.add_point_time_or_range(wait_time)
    elif line.startswith('pt:'):
      pt = scrape_point_time(line)
      if pt != None:
        transport.add_point_time_or_range(pt)
    elif line.startswith('co:'):
      comment = line[ len('co:') : ]
      comment = comment.lstrip(' \t').rstrip(' \t\r\n')
      transport.set_comment(comment)
    elif line.startswith('e_transp'):
      return transport
  raise DataFlowError, '[e_transp] marker did not finished a transport section in data file.'

      
def look_ahead_section_and_return_exercise_obj(lines):
  point_times = []; comment = None
  for line in lines: # xrange(i+1, len(lines)+1):
    #line = lines[j]
    if line.startswith('e_exerc'):
      if len(point_times) != 2:
        raise DataFlowError, '[e_exerc] marker did not get 2 point times as expected.'
      pt1 = point_times[0]
      pt2 = point_times[1]
      exercise = Exercise(pt1, pt2, comment)
      return exercise
    elif line.startswith('pt:'):
      pt = scrape_point_time(line)
      if pt != None:
        point_times.append(pt)
    elif line.startswith('co:'):
      comment = line[ len('co:') : ]
  raise DataFlowError, '[e_exerc] marker did not finished an exercise section in data file.'

trips = []
def process_datafile_abspath(datafile_abspath):
  lines = open(datafile_abspath).readlines()
  for i, line in enumerate(lines):
    line = line.lstrip(' \t').rstrip(' \t\r\n')
    if line == '':
      continue
    if line.startswith('trip:'):
      tripper = RunTripper()
      pos_trip = len('trip:')
      rem_line = line[ pos_trip : ]
      rem_line = rem_line.lstrip(' \t').rstrip(' \t\r\n')
      date8str = rem_line[ : 8 ]
      pydate = pydate_from_8str(date8str)
      if pydate == None:
        raise DataFlowError, 'pydate == None after tripper() instantiation'
      ground = False
      if rem_line.find(' gnd ') > -1:
        ground = True
      comment  = get_comments_by_vertical_bars_if_any(rem_line)
      tripper.set_header(pydate, ground, comment)
    elif line.startswith('b_transp'):
      transport = look_ahead_section_and_return_transport_obj(lines[i+1:])
      tripper.add_transport(transport)
    elif line.startswith('b_exerc'):
      exercise = look_ahead_section_and_return_exercise_obj(lines[i+1:])
      tripper.add_exercise(exercise)
    elif line.startswith('run:'):
      rem_line = line [ len('run:') : ]
      rem_line = rem_line.lstrip(' \t').rstrip(' \t\r\n')
      comment = get_comments_by_vertical_bars_if_any(rem_line)

      parcours_token = None
      mstr_duration  = None
      nstops         = None
      raintype       = None

      try:
        pp = rem_line.split(' ')
        parcours_token   = pp[0]
        parcours = Parcours(parcours_token)
        mstr_duration = pp[1]
        nstops    = int(pp[2])
        weight    = int(pp[3])
        raintype_token  = pp[4]
        raintype = RainType(raintype_token) # may raise TokenAndValueError, in which case it just "pass(es)"
      except ValueError:
        pass
      except IndexError:
        pass
      except TokenAndValueError: # may be raised by RainType(token)
        pass
      run = Run(parcours=parcours, duration=mstr_duration, nstops=nstops, weight=weight, raintype=raintype, comment=comment)
      tripper.set_run(run)
    elif line.startswith('e_trip'):
      trips.append(tripper)

def read_rundata_txtfiles():
  datafile_abspaths = ls.get_all_rundatafiles_abspaths()
  for datafile_abspath in datafile_abspaths:
    # print 'datafile_abspath', datafile_abspath
    process_datafile_abspath(datafile_abspath)
  for tripper in trips:
    print 'Tripper'
    print '='*50
    print tripper

def process():
  read_rundata_txtfiles()

if __name__ == '__main__':
  process()
