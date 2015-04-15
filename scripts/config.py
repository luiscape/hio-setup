#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import json

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]

def LoadConfig(j = 'config.json'):
  '''Load configuration from config folder.'''
  try:
    j = os.path.join(dir, 'config', j)
    with open(j) as json_file:    
      return json.load(json_file)[0]

  except Exception as e:
    print "Could not load configuration."
    print e


def Main():
  LoadConfig()


if __name__ == '__main__':
  Main()