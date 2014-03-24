#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
XmlSha1HexFileMod.py
This module contains the XmlSha1HexFile class
'''

import datetime, os, sys
import __init__

from Movements import Location, Parcours, TransportVehicle, RainType
 
class PointTime(object):
  
  def __init__(self, location, t=None, temperature=None, comment=None):
    self.location = None
    self.t  = None
    self.set_location(location)
    self.set_t(t)
    self.temperature = temperature
    self.comment     = comment

  def set_location(self, location):
    if location == None:
      raise ValueError, 'location for PointTime cannot be None.'
    if type(location) != Location:
      raise ValueError, 'Given location (=%s) for PointTime is not valid.' %str(location) 
    self.location = location

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
          hour = int(pp[0])
          minute = int(pp[1])
          t = datetime.time(hour=hour, minute=minute)
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
    raise TypeError, 't (=%s) should either be a string in the form <min>h<sec> or it should have a datetime.time type,' %str(t)

  def __str__(self):
    try:
      location = str(self.location)
    except UnicodeEncodeError:
      location = 'UnicodeEncodeError'
    outstr = u'%s' %location 
    outstr += u' às %s' %(str(self.t))
    if self.temperature != None:
      outstr += ' : Temper %dC' %(self.temperature)
    return outstr

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

  def get_duration(self):
    '''
    delta_t = self.pt2.t - self.pt1.t
    return delta_t
    ''' 
    return '<duration>'

  def __str__(self):
    try:
      pt1_str = str(self.pt1)
      pt2_str = str(self.pt2)
    except UnicodeEncodeError:
      pt1_str = pt2_str = 'UnicodeEncodeError'
    outstr = u'%s até %s (duration:%s)' %(pt1_str, pt2_str, str(self.get_duration()))
    return outstr

class WaitTime(PointRange):
  
  def __init__(self, pt1, pt2): # duration is calculated
    super(WaitTime, self).__init__(pt1, pt2)

  def __str__(self):
    super_outstr = super(WaitTime, self).__str__()
    outstr = u'WaitTime %s' %super_outstr
    return outstr


class Transport(object):

  def __init__(self, transport_vehicle=None):
    self.transport_vehicle = None
    self.comment = None
    self.set_transport_vehicle(transport_vehicle)
    self.point_times = [] # each list element may be either of type PointTime, or type PointRange, or type WaitTime 
    
  def set_transport_vehicle(self, transport_vehicle):
    if transport_vehicle == None:
      raise ValueError, 'transport_vehicle for Transport cannot be None.'
    if type(transport_vehicle) != TransportVehicle:
      raise ValueError, 'Given transport_vehicle (=%s) for Transport is not valid.' %str(transport_vehicle) 
    self.transport_vehicle = transport_vehicle 
  
  def add_point_time_or_range(self, point_time_or_range):
    if type(point_time_or_range) not in [PointTime, PointRange, WaitTime]:
      raise TypeError, 'type(point_time_or_range)=%s not in [PointTime, PointRange, WaitTime]' %type(point_time_or_range)
    self.point_times.append(point_time_or_range)

  def set_comment(self, comment):
    self.comment = comment

  def __str__(self):
    try:
      vehicle = u'' + str(self.transport_vehicle)
    except UnicodeEncodeError:
      vehicle = 'UnicodeEncodeError'
    outstr = u'Vehicle: %s' %vehicle
    if self.comment != None:
      try:
        outstr += u'(Comment: %s)\n' %self.comment
      except UnicodeDecodeError:
        outstr += u'(Comment: %s)\n' %'UnicodeDecodeError' 
    else:
      outstr += u'\n'
    for i, point_time in enumerate(self.point_times):
      seq = i + 1
      try:
        pt_str = str(point_time)
      except UnicodeEncodeError:
        pt_str = 'UnicodeEncodeError' 
      outstr += u'\t%d %s\n' %(seq, pt_str)
    return outstr

class Exercise(PointRange):

  def __init__(self, pt1, pt2, comment=None): # duration is calculated
    super(Exercise, self).__init__(pt1, pt2)
    self.comment = comment

  def __str__(self):
    outstr  = u'Exercise:\n'
    outstr += super(Exercise, self).__str__()
    return outstr

class Run(object):
  
  def __init__(self, parcours, duration, nstops=0, weight=None, raintype=0, comment=None):
    self.parcours = None
    self.set_parcours(parcours)
    self.duration = None
    self.set_duration(duration)
    self.nstops   = 0
    self.set_nstops(nstops)
    self.weight   = weight
    self.raintype = None
    if type(raintype) == RainType:
      self.raintype = raintype
    self.comment  = comment

  def set_parcours(self, parcours):
    if parcours == None:
      raise ValueError, 'Parcours cannot be None for Run.'
    if type(parcours) != Parcours:
      raise ValueError, 'Given parcours (=%s) for Parcours is not valid.' %str(parcours) 
    self.parcours = parcours 

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

  def set_nstops(self, nstops):
    self.nstops = 0
    if nstops == None:
      return
    try:
      int(nstops)
      self.nstops = nstops
      return
    except ValueError:
      return

  def __str__(self):
    try:
      parcours_str = str(self.parcours)
    except UnicodeEncodeError:
      parcours_str = 'UnicodeEncodeError' 
    outstr  = u'Parcours: %s\n' %parcours_str
    outstr += u'\tDuration: %s\n' %str(self.duration)
    outstr += u'\tN. Stops: %d\n' %self.nstops
    if self.weight != None:
      outstr += u'\tWeight:   %d\n' %self.weight
    if self.raintype:
      outstr += u'\tRain:   %s\n' %str(self.raintype)
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
    outstr  = u'Runtrip:\n'
    outstr += u'\tDate: %s\n' %self.date 
    try:
      outstr += u'\tComments: %s\n' %self.comment
    except UnicodeDecodeError:
      outstr += u'\tComments: %s\n' %'UnicodeDecodeError' 
    for transport in self.transports:
      try:
        transport_str = str(transport)
      except UnicodeEncodeError:
        transport_str = 'UnicodeEncodeError' 
      outstr += u'\t%s\n' %transport_str
    for exercise in self.exercises:
      try:
        exerc_str = str(exercise)
      except UnicodeEncodeError:
        exerc_str = 'UnicodeEncodeError' 
      outstr += u'\t%s\n' %exerc_str
    outstr += u'\nRun:\n\t%s\n' %str(self.run)
    return outstr


def process():
  pass
  
if __name__ == '__main__':
  process()
