#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
'''

    
class TokenAndValueError(ValueError):
  pass    
    
class TokenAndValue(object):
  '''
  TokenAndValue base class for Models
  '''
  
  TokenAndValueDict = {}
  TokenAndValueDict['Example Key'] = u'Example Value'

  def __init__(self, token):
    self.token      = None
    self.value_text = None
    self.set_dict_name()
    self.set_token_and_value(token)

  def set_dict_name(self):
    # self.dict_name = __class__.__name__ + 'Dict'
    self.dict_name = 'TokenAndValueDict'

  def set_token_and_value(self, token):
    o_dict = eval('self.%s' %self.dict_name)
    if token in o_dict.keys():
      self.token = token
      self.value_text = o_dict[self.token]
      return
    raise TokenAndValueError, 'Data Error: token %s is not registered in %s :: %s' %(token, str(self.__class__), str(o_dict))

  def __str__(self):
    outstr = '[%s] %s'  %(self.token, self.value_text)
    return outstr


class Location(TokenAndValue):

  LocationDict = {}

  LocationDict['SFXA'] = u'Ponto São Franciso Xavier'
  LocationDict['SPEN'] = u'Praça Saens Pena' 
  LocationDict['URUG'] = u'Esquina Rua Uruguai'
  LocationDict['CMSJ'] = u'Ponto do Colégio Marista São José'
  LocationDict['USIN'] = u'Largo da Usina'
  LocationDict['ALTO'] = u'Pracinha do Alto da Boa Vista'
  LocationDict['CARM'] = u'Esquina Rua Carmela Dutra'
  LocationDict['CLOV'] = u'Esquina Rua Clóvis Bevilacqua'
  LocationDict['PARE'] = u'Esquina Rua Pareto'
  LocationDict['SUJI'] = u'Minipraça apelidada Sujinho'
  
  def set_dict_name(self):
    self.dict_name = 'LocationDict'


class Parcours(TokenAndValue):
  '''
  Parcours Model
  '''

  ParcoursDict = {}
  
  ParcoursDict['USIN_CLOV'] = u'Da Usina à Esquina da Rua Clóvis Bevilacqua (~4km)'
  ParcoursDict['USIN_PARE'] = u'Da Usina à Esquina da Rua Pareto (~5km)'
  ParcoursDict['USIN_MARQ'] = u'Da Usina à Esquina da Rua Marquês de Valença (~6km)'
  ParcoursDict['ALTO_USIN'] = u'Da Pracinha do Alto à Usina (~5km)'

  def set_dict_name(self):
    self.dict_name = 'ParcoursDict'


class TransportVehicle(TokenAndValue):
  '''
  Transportation (buses, vans etc.) Constants
  '''
  
  TransportVehicleDict = {}
  
  TransportVehicleDict['B301'] = u'Ônibus 301' 
  TransportVehicleDict['B333'] = u'Ônibus 333'
  TransportVehicleDict['B415'] = u'Ônibus 415'
  TransportVehicleDict['B426'] = u'Ônibus 426'

  def set_dict_name(self):
    self.dict_name = 'TransportVehicleDict'


class RainType(TokenAndValue):
  '''
  Transportation (buses, vans etc.) Constants
  '''
  
  RainTypeDict = {}
  
  RainTypeDict['RAIN_NR']   = u'No Rain.' 
  RainTypeDict['RAIN_AWR']  = u'After Weak Rain. Wet floor.'
  RainTypeDict['RAIN_ANR']  = u'After Normal Rain. Wet floor.'
  RainTypeDict['RAIN_ANR']  = u'After Pouring Rain. Wet floor.'
  RainTypeDict['RAIN_WR']   = u'Weak Rain.'
  RainTypeDict['RAIN_WWR']  = u'Windy Weak Rain.'
  RainTypeDict['RAIN_NR']   = u'Normal Rain.'
  RainTypeDict['RAIN_WNR']  = u'Windy Normal Rain.'
  RainTypeDict['RAIN_PR']   = u'Pouring Rain.'
  RainTypeDict['RAIN_WIPR'] = u'Windy Pouring Rain.'
  RainTypeDict['RAIN_WAPR'] = u'Warm Pouring Rain.'
  RainTypeDict['RAIN_CPR']  = u'Cold Pouring Rain.'

  def set_dict_name(self):
    self.dict_name = 'RainTypeDict'


def process():
  pass
  
if __name__ == '__main__':
  process()
