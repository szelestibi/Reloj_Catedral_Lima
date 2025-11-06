#!/usr/bin/python
# -*- coding: utf-8 -*-

# disco minutero con imanes

from xml.dom import minidom
import math, os, sys, time, yaml
sys.path.insert(0, "/home/tiberio/Work/RCL/proyecto/python/modules/")
import cfgx
import style
import grid
import piece
import svgx

# --------- CONFIG BEGIN ------------------------------------
UNIT = 'MECANISMO'
SVGX = os.path.splitext(os.path.basename(__file__))[0]
PART = SVGX[5:]
# --------- CONFIG END --------------------------------------

def float_shorten(f):
 ff = f'{f:.3f}'.rstrip('0').rstrip('.')
 if ff.startswith('0.'): ff = ff[1:]
 if ff.startswith('-0.'): ff = '-' + ff[2:]
 return ff

def circle_path(cx, cy, r): # circle as two 180° arcs for compound path
 return (f"M {float_shorten(cx - r)} {float_shorten(cy)} a {float_shorten(r)} {float_shorten(r)} 0 1 0 {float_shorten(2*r)} 0 a {float_shorten(r)} {float_shorten(r)} 0 1 0 {float_shorten(-2*r)} 0 Z ")

cfgx.load()
style.load()
grid.load(cfgx.makedata[UNIT][PART]['grid'],cfgx.makedata['GRID'])
piece.load(cfgx.makedata[UNIT][PART])

# print('')
# print(style.piece_style)
# print(grid.grid)
# print(piece.piecedata['svgroot'])
# print(cfgx.makedata[UNIT][PART])

holes_list = {}

if 'cuts_files' in cfgx.makedata[UNIT][PART]:
 # print('CUTS FILES!')
 for hf in cfgx.makedata[UNIT][PART]['cuts_files']:
  svgx = minidom.parse('../../svg_master/' + hf + '.svg')
  elems = svgx.getElementsByTagName('*')
  holes = [el for el in elems if el.getAttribute('class') == 'hole']
  if holes:
   holes_list[hf] = holes[0]

# print(holes_list)

axis_hole_svg_txt = ''

if 'axis_hole' in cfgx.makedata[UNIT][PART]:
 # print('AXIS HOLE!')
 ax_ho = cfgx.makedata[UNIT][PART]['axis_hole']
 if isinstance(ax_ho, str) and ' ' in ax_ho:
  idx, subidx = ax_ho.split(None,1)
  r = float(cfgx.dimensions[idx][subidx]) / 20
 else:
  r = float(cfgx.dimensions[ax_ho]) / 20
 axis_hole_svg_txt = f'<path id="axis" class="hole" d="{circle_path(0, 0, r).strip()}"/>'
 # print(axis_hole_svg_txt)

# ********************************************************

if cfgx.makedata['GRID'] == True:
 bgnd_elems = [e for e in piece.piecedata['svgroot'].getElementsByTagName('*') if e.getAttribute('id') == 'bgnd']
 # print(bgnd_elems[0].toxml())
 parent = bgnd_elems[0].parentNode
 next_sibling = bgnd_elems[0].nextSibling
 if next_sibling is not None:
  parent.insertBefore(grid.grid['style'], next_sibling)
 else:
  parent.appendChild(grid.grid['style'])
 parent.insertBefore(grid.grid['grid'], next_sibling)
 #parent.removeChild(bgnd_elems[0])
 parent.replaceChild(style.piece_style, bgnd_elems[0])
else:
 bgnd_elems = [e for e in piece.piecedata['svgroot'].getElementsByTagName('*') if e.getAttribute('id') == 'bgnd']
 # print(bgnd_elems[0].toxml())
 parent = bgnd_elems[0].parentNode
 next_sibling = bgnd_elems[0].nextSibling
 if next_sibling is not None:
  parent.insertBefore(style.piece_style, next_sibling)
 else:
  parent.appendChild(style.piece_style)
 
# ********************************************************

# holes_list
# print(holes_list)
for hole in holes_list:
 # print(holes_list[hole].toxml())
 parent.appendChild(holes_list[hole])

# axis_hole_svg_txt
# print(axis_hole_svg_txt)
#parent.appendChild(axis_hole_svg_txt)
if axis_hole_svg_txt:
 axis_hole_node = minidom.parseString(axis_hole_svg_txt).documentElement
 parent.appendChild(axis_hole_node)

# ********************************************************

filepath = '../../' + UNIT.lower() + '/' + SVGX + '.svg'
print(f'WRITING {filepath}')
with open(filepath, 'w', encoding='utf-8') as f:
 piece.piecedata['svgroot'].writexml(f)

# time.sleep(1)
