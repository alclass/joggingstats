#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
XmlSha1HexFileMod.py
This module contains the XmlSha1HexFile class
'''

import datetime, os, sys
import __init__

from Constants import A, B, P, T
 
class PointTime(object):
  
  def __init__(self, pt, t=None, temperature=None, comment=None):
    self.pt = None
    self.t  = None
    self.set_pt(pt)
    self.set_t(t)
    self.temperature = temperature
    self.comment     = comment

  def set_pt(self, pt):
    if pt == None:
      raise ValueError, 'pt (point location) cannot be None.'
    if not P.is_attr_valid(pt):
      raise ValueError, 'pt (point location) with id %d is not valid.'
    self.pt = pt

  def get_pt_txt(self):
    return P.get_const_txt(self.pt)

  def set_t(self, t):
    '''
    t (time) as None is allowed. However, once it's not None,
      it should either be a str (or unicode) or datetime.time, 
      otherwise TypeError will be raised.
    '''
    if t == None:
      self.t = None
      return
    if type(t) in [str, unicode]:
      if t.find('h') > -1:
        pp = t.split('h')
        try:
          minute = int(pp[0])
          second = int(pp[1])
          t = datetime.time(minute=minute, second=second)
          self.t = t
          return
        except ValueError: # ie, int(...) is raising it
          pass
        except IndexError: # ie, pp[1] is raising it
          pass
    else:
      if type(t) == datetime.time:
        self.t = t
        return
    raise TypeError, 't (=%s) should either be a string in the form <min>h<sec> or it should have a datetime.time type,'

  def __str__(self):
    return 'PointTime'

class PointRangeTypeError(TypeError):
  pt_error_msg = 'Error: pt (=%s) given to PointRange is not of type PointTime'

class PointRange(object):

  def __init__(self,  pt1, pt2, wait_time=False):

    if type(pt1) != PointTime:
      error_msg = PointRangeTypeError.pt_error_msg %str(pt1)
      raise PointRangeTypeError, error_msg 
    if type(pt2) != PointTime:
      error_msg = PointRangeTypeError.pt_error_msg %str(pt2)
      raise PointRangeTypeError, error_msg 
       
    self.pt1 = pt1
    self.pt2 = pt2

    if type(wait_time) != bool:
      error_msg = 'wait_time given to PointRange should be a boolean (ie, either True or False)'
      raise PointRangeTypeError, error_msg
    self.wait_time = wait_time

  def __str__(self):
    return 'PointRange'

class Transport(object):

  def __init__(self, transport_vehicle=None):
    self.transport_vehicle = None
    self.set_transport_vehicle(transport_vehicle)
    self.point_times = []
    
  def set_transport_vehicle(self, transport_vehicle):
    if transport_vehicle == None:
      self.transport_vehicle = None
      return
    if not B.is_attr_valid(transport_vehicle):
      raise TypeError, 'transport_vehicle (=%s) is not valid.'
    self.transport_vehicle = transport_vehicle 
  
  def add_point_time_or_range(self, point_time_or_range):
    self.point_times.append(point_time_or_range)

class Exercise(PointRange):

  def __init__(self, pt1, pt2, comment=None): # duration is calculated
    super(Exercise, self).__init__(pt1, pt2)
    self.comment = comment

  def __str__(self):
    return 'Exerc'


class Run(object):
  
  def __init__(self, parcours=None, duration=None, nstops=0, weight=None, raintype=0, comment=None):
    self.parcours = None
    self.set_parcours(parcours)
    self.duration = None
    self.set_duration(duration)
    self.nstops   = nstops
    self.weight   = weight
    self.raintype = raintype
    self.comment  = comment

  def set_parcours(self, parcours):
    if parcours == None:
      return
    if not T.is_attr_valid(parcours):
      raise TypeError, 'parcours id %s is not valid.' %str(parcours)
    self.parcours = parcours

  def get_parcours_txt(self):
    return T.get_const_txt(self.parcours)    

  def set_duration(self, duration):
    if duration == None:
      self.duration = None
      return
    if type(duration) in [str, unicode]:
      if duration.find('m') > -1:
        pp = duration.split('m')
        try:
          minute = int(pp[0])
          second = int(pp[1])
          self.duration = datetime.time(minute=minute, second=second)
          return
        except ValueError: # ie, int(...) is raising it
          pass
        except IndexError: # ie, pp[1] is raising it
          pass
    else:
      if type(duration) == datetime.time:
        self.self.duration = duration
        return
    raise TypeError, 'self.duration (=%s) should either be a string in the form <min>m<sec> or it should have a datetime.time type,'
    


  def __str__(self):
    outstr  = 'Parcours: %s\n'  %self.get_parcours_txt()
    outstr += '\tDuration: %s\n' %str(self.duration)
    outstr += '\tN. Stops: %d\n' %self.nstops
    outstr += '\tWeight:   %d\n' %self.weight
    return outstr

  
class RunTripper(object):
  
  def __init__(self):
    self.date        = None
    self.ground      = None
    self.comment     = None
    self.transports  = []
    self.exercises   = []
    self.run         = None

  def set_header(self, date=None, ground=True, comment=None):
    if type(date) != datetime.date:
      raise TypeError, 'date should be of datetime.date type'
    self.date    = date
    self.ground  = ground
    self.comment = comment
        
  def add_transport(self, transport):
    if type(transport) != Transport:
      raise TypeError, 'transport is not of Transport type'
    self.transports.append(transport)

  def add_exercise(self, exercise):
    if type(exercise) != Exercise:
      raise TypeError, 'exercise is not of Exercise type'
    self.exercises.append(exercise)

  def set_run(self, run):
    if type(run) != Run:
      raise TypeError, 'run is not of Run type'
    self.run = run

  def __str__(self):
    outstr  = 'Runtrip:\n'
    outstr += '\tDate: %s\n' %self.date 
    outstr += '\tComment: %s\n' %self.comment
    for transport in self.transports:
      outstr += '\tTransp.:%s\n' %str(transport)
    for exercise in self.exercises:
      outstr += '\tExercise:%s\n' %str(exercise)
    outstr += '\tRun:%s\n' %str(self.run)
    return outstr


def process():
  pass
  
if __name__ == '__main__':
  process()
