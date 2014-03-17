#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
'''

class ConstantsBase:

  @classmethod
  def is_attr_valid(cls, p_attrib):
    for attr in dir(cls):
      if attr.startswith('_'):
        continue
      if attr == p_attrib:
        return True
    return False

  @classmethod
  def is_const_in_cc_class(cls, p_const):
    for attr in dir(cls):
      if attr.startswith('_'):
        continue
      class_dot_attrib = 'cls.%s' %attr
      n = eval(class_dot_attrib)
      if n == p_const:
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
    
  @classmethod
  def get_const_id_by_token(cls, token):
    class_dot_attr = 'cls.%s' %token
    try:
      n = eval(class_dot_attr)
      return n
    except AttributeError:
      pass
    return None # 'No description for location'

def process():
  pass
  
if __name__ == '__main__':
  process()
