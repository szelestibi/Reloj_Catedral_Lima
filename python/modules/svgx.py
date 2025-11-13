#!/usr/bin/python
# -*- coding: utf-8 -*-

from xml.dom import minidom
import inspect
from datetime import datetime
import cfgx
import grid
import piece
import style

def by_id(svgdoc, id_value):
 for el in svgdoc.getElementsByTagName('*'):
  if el.getAttribute('id') == id_value:
   return el
 return None

def get_svg_opening_tag(svgobject):
 svg = svgobject.documentElement
 opening = "<" + svg.tagName
 for name, value in svg.attributes.items():
  opening += f' {name}="{value}"'
 opening += ">"
 return opening

def float_shorten(f):
 ff = f'{f:.3f}'.rstrip('0').rstrip('.')
 if ff.startswith('0.'): ff = ff[1:]
 elif ff.startswith('-0.'): ff = '-' + ff[2:]
 return ff

def circle_path(cx, cy, r): # circle as two 180° arcs for compound path
 return (f"M {float_shorten(cx - r)} {float_shorten(cy)} a {float_shorten(r)} {float_shorten(r)} 0 1 0 {float_shorten(2*r)} 0 a {float_shorten(r)} {float_shorten(r)} 0 1 0 {float_shorten(-2*r)} 0 Z ")

def make(unit,filename):
 part = filename[5:]
 timestamp = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
 svg_txt = [f'<?xml version="1.0" encoding="utf-8" ?><!-- SZT {timestamp} -->']
 # opening_tag
 if cfgx.makedata['GRID'] == True:
  svg_txt.append(grid.grid['opening_tag'])
 else:
  svg_txt.append(piece.piecedata['opening_tag'])
 # style
 if cfgx.makedata['GRID'] == True:
  svg_txt.append(grid.grid['style'].toxml())
 svg_txt.append(style.piece_style.toxml())
 # grid
 if cfgx.makedata['GRID'] == True:
  svg_txt.append(grid.grid['grid'].toxml())
 # piece
 svg_txt.append(piece.piecedata['mainline'].toxml())
 for entry in piece.piecedata:
  if entry != 'opening_tag' and entry != 'mainline':
   try:
    svg_txt.append(piece.piecedata[entry].toxml())
   except AttributeError:
    print(f'INCLUDE ERROR: "{entry}" seems to be inexistent ...')
 # axis hole
 if 'axis_hole' in cfgx.makedata[unit][part]:
  r_add = 0
  if 'axis_hole_add' in cfgx.makedata[unit][part]:
   r_add = float(cfgx.makedata[unit][part]['axis_hole_add'])
  ax_ho = cfgx.makedata[unit][part]['axis_hole']
  if isinstance(ax_ho, str) and ' ' in ax_ho:
   idx, subidx = ax_ho.split(None,1)
   r = float(cfgx.dimensions[idx][subidx]) / 20 + r_add / 10
  else:
   r = float(cfgx.dimensions[ax_ho]) / 20 + r_add / 10
  axis_hole = f'<path id="axis" class="hole" d="{circle_path(0, 0, r).strip()}"/>'
  svg_txt.append(axis_hole)
 # other cuts
 if 'cuts_files' in cfgx.makedata[unit][part]:
  # print('CUTS FILES!')
  for hf in cfgx.makedata[unit][part]['cuts_files']:
   svgroot = minidom.parse('../../svg_master/' + hf + '.svg')
   elements = svgroot.getElementsByTagName('*')
   holes = [el for el in elements if el.getAttribute('class') == 'hole']
   if holes:
    svg_txt.append(holes[0].toxml())
 # end tag
 svg_txt.append('</svg>')
 filepath = '../../' + unit.lower() + '/' + filename + '.svg'
 print(f'WRITING {filepath}')
 with open(filepath, 'w', encoding='utf-8') as f:
  f.write('\n'.join(svg_txt))
