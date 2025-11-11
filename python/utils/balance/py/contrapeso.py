#!/usr/bin/python
# -*- coding: utf-8 -*-

# contrapeso

from datetime import datetime
import math
import os
import yaml

bgnd = True
#bgnd = False

dimensiones = {
 'width_cm': 7,
 'length_cm' : 50,
 'r_axis_cm': 6 }

W = dimensiones['width_cm']
L = dimensiones['length_cm']
R = dimensiones['r_axis_cm']

class Point:
 def __init__(self, x, y):
  self.x = x
  self.y = y
 def __repr__(self):
  return f'Point(x={self.x}, y={self.y})'

def float_shorten(f):
 ff = f'{f:.3f}'.rstrip('0').rstrip('.')
 if ff.startswith('0.'): ff = ff[1:]
 if ff.startswith('-0.'): ff = '-' + ff[2:]
 return ff

def circle_path(cx, cy, r): # circle as two 180° arcs for compound path
 return f'M {float_shorten(cx - r)} {float_shorten(cy)} a {float_shorten(r)} {float_shorten(r)} 0 1 0 {float_shorten(2*r)} 0 a {float_shorten(r)} {float_shorten(r)} 0 1 0 {float_shorten(-2*r)} 0 Z '

def xy_polar_complement(xy,r,q,find='y'): # find = 'y' or 'x', quadrant = 1,2,3,4
 delta = math.sqrt(r*r - xy*xy)
 q = 5 - q                                # SVG coordinates
 if find == 'y':
  if q in (1, 2):
   return delta
  else:
   return -delta
 elif find == 'x':
  if q in (1, 4):
   return delta
  else:
   return -delta

def build_counterweight(w,l,r):
 P0 = Point(-w/2,xy_polar_complement(w/2,r,2)) # oben links
 P1 = Point(w/2,xy_polar_complement(w/2,r,1))  # oben rechts
 P2 = Point(w/2,xy_polar_complement(w/2,r,4))  # unten rechts
 P3 = Point(-w/2,xy_polar_complement(w/2,r,3)) # unten links
 print(P0) # anschluss gegengewicht
 print(P1) # anschluss gegengewicht
 print(P2) # anschluss uhrzeiger
 print(P3) # anschluss uhrzeiger
 return f'M {P0.x} {P0.y} V {-l + w} A {w/2} {w/2} 0 0 1 {P1.x} {-l + w} V {P1.y} A {r} {r} 0 1 1 {P0.x} {P0.y} Z '

def build_svg():
 d = build_counterweight(W,L,R)
 timestamp = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
 svg = f'''<?xml version="1.0" encoding="UTF-8" ?><!-- generated with ./{os.path.splitext(os.path.basename(__file__))[0]}.py --><!-- SZT {timestamp} -->
<svg xmlns="http://www.w3.org/2000/svg" width="13cm" height="60cm" viewBox="-6.5 -50 13 60">
<defs><style>
 path {{ fill: rgba(30,60,90,.7); stroke: none; fill-rule:evenodd; }}
 #bgnd {{ fill: white; stroke: none; }}
</style></defs>
{'<rect id="bgnd" width="13" height="60" x="-6.5" y="-50" />' if bgnd == True else ''}
<path id="cpx" d="{d.strip()}" />
</svg>'''
 return svg

print('')

svg = build_svg()
out = './contrapeso.svg'
with open(out, 'w', encoding='utf-8') as f:
 f.write(svg)
print(out + ' WRITTEN')
