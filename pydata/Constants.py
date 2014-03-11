#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
'''

class ConstantsBase:

  @classmethod
  def is_attr_valid(cls, pt):
    for attr in dir(cls):
      if attr.startswith('_'):
        continue
      class_dot_attr = 'cls.%s' %attr
      n = eval(class_dot_attr)
      if n == pt:
        return True
    return False

  @classmethod 
  def get_const_txt(cls, pt):
    for attr in dir(cls):
      if attr.startswith('_'):
        continue
      class_dot_attr = 'cls.%s' %attr
      n = eval(class_dot_attr)
      if n == pt:
        txt_attrib = 'cls.%s_TXT' %attr
        return eval(txt_attrib)
    return None # 'No description for location'

  @classmethod
  def list_const_txts(cls):
    outstr = ''
    n_attrs = 0
    for attr in dir(cls):
      if attr.startswith('_'):
        continue
      n_attrs += 1
    for i in xrange(1, n_attrs + 1):
      const_txt = cls.get_const_txt(i)
      if const_txt == None:
        continue
      outstr += '%s\n' %const_txt
    return outstr
    

class P(ConstantsBase):
  '''
  Point (Locations) Constants
  '''
  SFXA = 1; SFXA_TXT = u'Ponto São Franciso Xavier'
  SPEN = 2; SPEN_TXT = u'Praça Saens Pena' 
  CMSJ = 3; CMSJ_TXT = u'Ponto do Colégio Marista São José'
  USIN = 4; USIN_TXT = u'Largo da Usina'
  ALTO = 5; ALTO_TXT = u'Pracinha do Alto da Boa Vista'
  CARM = 6; CARM_TXT = u'Esquina Rua Carmela Dutra'
  CLOV = 7; CLOV_TXT = u'Esquina Rua Clóvis Bevilacqua'
  PARE = 8; PARE_TXT = u'Esquina Rua Pareto'
  SUJI = 9; SUJI_TXT = u'Minipraça apelidada Sujinho'
  

class A(ConstantsBase):
  '''
  Activity (Run or Exercise) Constants
  '''
  RUN = 1
  EXE =2
  
class T(ConstantsBase):
  '''
  Point-to-Point (trajectory) Constants
  '''
  
  USIN_CLOV = 1; USIN_CLOV_TXT = u'Da Usina à Esquina da Rua Clóvis Bevilacqua (~4km)'
  USIN_PARE = 2; USIN_PARE_TXT = u'Da Usina à Esquina da Rua Pareto (~5km)'
  USIN_MARQ = 3; USIN_MARQ_TXT = u'Da Usina à Esquina da Rua Marquês de Valença (~6km)'
  ALTO_USIN = 4; ALTO_USIN_TXT = u'Da Pracinha do Alto à Usina (~5km)'
   
class B(ConstantsBase):
  '''
  Transportation (buses, vans etc.) Constants
  '''
  B301 = 1
  B333 = 2
  B415 = 3
  B426 = 4


def test_txt():
  print '***begins'
  print T.list_const_txts()
  print P.list_const_txts()
  print '***ends'


def process():
  test_txt()
  
if __name__ == '__main__':
  process()
