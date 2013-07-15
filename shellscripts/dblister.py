#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
Created on 27/06/2013

@author: friend
'''
# import os, sys, time

htmlfile = 'analyticalchem-001-lecture-index.html'  
re_text_to_find = 'lecture_id=(\d+)'
import re
re_compiled_text_to_find = re.compile(re_text_to_find) 

def process():
  text = open(htmlfile).read()
  re_find_obj = re_compiled_text_to_find.finditer(text)
  unique_ids = {}
  #for i, each in enumerate(re_find_obj):
  for each in re_find_obj:
    video_n_id = each.group(1)
    if unique_ids.has_key(video_n_id):
      continue
    unique_ids[video_n_id]=1
  video_n_ids = map(int, unique_ids.keys())
  video_n_ids.sort()
  #for i, video_n_id in enumerate(video_n_ids):
  for video_n_id in video_n_ids:
    print video_n_id,',',
  
if __name__ == '__main__':
  process()  

