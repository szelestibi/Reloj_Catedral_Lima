#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
import math
import os
import yaml

o = 74.5 # offset

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

def kreisspitz(cx, cy, r, b, o):
 P = Point(0,0)
 B = Point(0,b + o)
 Q = Point(0,0)
 angle_rad = math.asin(r/B.y)
 x = float(float_shorten(abs(r * math.cos(angle_rad))))
 y = float(float_shorten(abs(r * math.sin(angle_rad))))
 print(f'X: {x} Y: {y}')
 P.x = -x
 P.y = y + o
 Q.x = x
 Q.y = y + o
 return f'M {P.x} {P.y} A {r} {r} 0 1 1 {Q.x} {Q.y} L 0 {B.y} L {P.x} {P.y} Z '

def build_svg():
 d = kreisspitz(0,0,1.5,15.5,o)
 timestamp = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
 svg = f'''<?xml version="1.0" encoding="UTF-8" ?><!-- generated with ./{os.path.splitext(os.path.basename(__file__))[0]}.py --><!-- SZT {timestamp} -->
<svg xmlns="http://www.w3.org/2000/svg" width="5cm" height="20cm" viewBox="-2.5 {o-2} 5 20">
<defs><style>
 path {{ fill: rgba(30,60,90,.7); stroke: none; fill-rule:evenodd; }}
 #bgnd {{ fill: rgba(191,191,191,.5); stroke: none; }}
</style></defs>
<rect id="bgnd" width="5" height="20" x="-2.5" y="{o-2}" />
<circle cx="0" cy="0" r=".1" />
<path id="d_spitz" class="deco" d="{d.strip()}" />
</svg>'''
 return svg

print('')

svg = build_svg()
out = './kreisspitz.svg'
with open(out, 'w', encoding='utf-8') as f:
 f.write(svg)
print(out + ' WRITTEN')
