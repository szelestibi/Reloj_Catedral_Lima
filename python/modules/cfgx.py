#!/usr/bin/python
# -*- coding: utf-8 -*-

import yaml

dimensions = {}
makedata = {}

def load():
 global dimensions, makedata
 with open('../yaml/dimensiones.yaml', 'r', encoding='utf-8') as f:
  dimensions = yaml.safe_load(f).get('dimensions', {})
 with open('../yaml/make.yaml', 'r', encoding='utf-8') as f:
  makedata = yaml.safe_load(f)
 # print(dimensions)
 # print(makedata['MECANISMO'])
