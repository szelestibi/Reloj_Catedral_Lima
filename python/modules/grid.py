#!/usr/bin/python
# -*- coding: utf-8 -*-

from xml.dom import minidom
import inspect
import svgx

grid = {}

def load(g,d):
 if d == False:
  return {}
 global grid
 # print(f'this is grid.load_grid({g})')
 grid_files = { '10x10': '010x010', '24x150': '024x150', '30x30': '030x030', '130x130': '130x130' }
 try:
  filename = '../grids/grid_' + grid_files[g] + '.svg'
 except KeyError:
  info = inspect.getframeinfo(inspect.currentframe())
  print(f'KEY ERROR: {g} in {info.filename} {info.function} {info.lineno} ')
  return None
 svgroot = minidom.parse(filename)
 grid['opening_tag'] = svgx.get_svg_opening_tag(svgroot)
 grid['style'] = svgx.by_id(svgroot, 'grid_style')
 grid['grid'] = svgx.by_id(svgroot, 'grid')
 return grid
