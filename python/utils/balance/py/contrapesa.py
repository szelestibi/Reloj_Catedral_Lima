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
 'width_cm': 3,
 'length_cm' : 50,
 'r_axis_cm': 6,
 'r_weight_cm': 4 }

#ret = 1 # stumpf gerundet
#ret = 2 # stumpf gerundet mit achse
ret = 3 # mit achse und gegengewicht
#ret = 4 # mit gegengewicht

W = dimensiones['width_cm']
L = dimensiones['length_cm']
R = dimensiones['r_axis_cm']
S = dimensiones['r_weight_cm']

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

def build_counterweight(w,l,r,s):
 P0 = Point(-w/2,xy_polar_complement(w/2,r,2)) # achse oben links
 P1 = Point(w/2,xy_polar_complement(w/2,r,1))  # achse oben rechts
 P2 = Point(w/2,xy_polar_complement(w/2,r,4))  # achse unten rechts
 P3 = Point(-w/2,xy_polar_complement(w/2,r,3)) # achse unten links
 PA = Point(-w/2,-l+s+xy_polar_complement(w/2,s,3)) # gegengewicht unten links
 PB = Point(w/2,-l+s+xy_polar_complement(w/2,s,4)) # gegengewicht unten rechts
 print(P0) # anschluss traeger
 print(P1) # anschluss traeger
 print(P2) # anschluss uhrzeiger
 print(P3) # anschluss uhrzeiger
 print(PA) # anschluss gegengewicht
 print(PB) # anschluss gegengewicht
 if ret == 1:
  return f'M {float_shorten(P0.x)} {float_shorten(P0.y)} V {float_shorten(-l + w)} A {float_shorten(w/2)} {float_shorten(w/2)} 0 0 1 {float_shorten(P1.x)} {float_shorten(-l + w)} V {float_shorten(P1.y)} Z '
 elif ret == 2:
  return f'M {float_shorten(P0.x)} {float_shorten(P0.y)} V {float_shorten(-l + w)} A {float_shorten(w/2)} {float_shorten(w/2)} 0 0 1 {float_shorten(P1.x)} {float_shorten(-l + w)} V {float_shorten(P1.y)} A {float_shorten(r)} {float_shorten(r)} 0 1 1 {float_shorten(P0.x)} {float_shorten(P0.y)} Z '
 elif ret == 3:
  return f'M {float_shorten(P0.x)} {float_shorten(P0.y)} V {float_shorten(PA.y)} A {float_shorten(s)} {float_shorten(s)} 0 1 1 {float_shorten(PB.x)} {float_shorten(PB.y)} V {float_shorten(P1.y)} A {float_shorten(r)} {float_shorten(r)} 0 1 1 {float_shorten(P0.x)} {float_shorten(P0.y)} Z '
 elif ret == 4:
  return f'M {float_shorten(P0.x)} {float_shorten(P0.y)} V {float_shorten(PA.y)} A {float_shorten(s)} {float_shorten(s)} 0 1 1 {float_shorten(PB.x)} {float_shorten(PB.y)} V {float_shorten(P1.y)} Z '


 # return f'M {P0.x} {P0.y} V {-l + w} A {w/2} {w/2} 0 0 1 {P1.x} {-l + w} V {P1.y} Z '                               # stumpf gerundet
 # return f'M {P0.x} {P0.y} V {-l + w} A {w/2} {w/2} 0 0 1 {P1.x} {-l + w} V {P1.y} A {r} {r} 0 1 1 {P0.x} {P0.y} Z ' # stumpf gerundet mit achse
 # return f'M {P0.x} {P0.y} V {PA.y} A {s} {s} 0 1 1 {PB.x} {PB.y} V {P1.y} A {r} {r} 0 1 1 {P0.x} {P0.y} Z '         # mit achse und gegengewicht
 # return f'M {P0.x} {P0.y} V {PA.y} A {s} {s} 0 1 1 {PB.x} {PB.y} V {P1.y} Z '                                         # mit gegengewicht

def build_svg():
 d = build_counterweight(W,L,R,S)
 timestamp = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
 svg = f'''<?xml version="1.0" encoding="UTF-8" ?><!-- generated with ./{os.path.splitext(os.path.basename(__file__))[0]}.py --><!-- SZT {timestamp} -->
<svg xmlns="http://www.w3.org/2000/svg" width="13cm" height="57cm" viewBox="-6.5 -50.5 13 57">
<defs><style>
 path {{ fill: rgba(30,60,90,.7); stroke: none; fill-rule:evenodd; }}
 #bgnd {{ fill: white; stroke: none; }}
</style></defs>
{'<rect id="bgnd" width="13" height="57" x="-6.5" y="-50.5" />' if bgnd == True else ''}
<path id="cpx" d="{d.strip()}" />
</svg>'''
 return svg

print('')

svg = build_svg()
out = './contrapesa.svg'
with open(out, 'w', encoding='utf-8') as f:
 f.write(svg)
print(out + ' WRITTEN')
