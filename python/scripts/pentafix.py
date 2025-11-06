#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
import math
import os
import yaml

with open('../yaml/dimensiones.yaml', 'r', encoding='utf-8') as f:
 dimensions = yaml.safe_load(f).get('dimensions', {})

def float_shorten(f):
 ff = f'{f:.3f}'.rstrip('0').rstrip('.')
 if ff.startswith('0.'): ff = ff[1:]
 if ff.startswith('-0.'): ff = '-' + ff[2:]
 return ff

def circle_path(cx, cy, r): # circle as two 180° arcs for compound path
 return (f"M {float_shorten(cx - r)} {float_shorten(cy)} a {float_shorten(r)} {float_shorten(r)} 0 1 0 {float_shorten(2*r)} 0 a {float_shorten(r)} {float_shorten(r)} 0 1 0 {float_shorten(-2*r)} 0 Z ")

def build_svg():
 d = ""
 # five holes around at 72° steps
 for i in range(5):
  ang = math.radians(i * 72.0 - 18.0) # start at -18° to center top hole
  cx = R_ORBIT * math.cos(ang)
  cy = R_ORBIT * math.sin(ang)
  d += circle_path(cx, cy, R_SCREW)
 timestamp = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
 svg = f'''<?xml version="1.0" encoding="UTF-8" ?><!-- generated with ../scripts/{os.path.splitext(os.path.basename(__file__))[0]}.py --><!-- SZT {timestamp} -->
<svg xmlns="http://www.w3.org/2000/svg" width="36cm" height="36cm" viewBox="-18 -18 36 36">
<defs><style>
 path {{ fill: rgba(30,60,90,.7); stroke: none; fill-rule:evenodd; }}
 #bgnd {{ fill: white; stroke: none; }}
</style></defs>
<rect id="bgnd" height="36" width="36" x="-18" y="-18" />
<path id="PFIX" class="hole" d="{d.strip()}" />
</svg>'''
 return svg

R_SCREW = dimensions['pentafix']['screw_diameter'] / 20.0 # fixing screw
R_ORBIT = dimensions['pentafix']['orbit_radius']   / 10.0 # orbit radius

print('')

svg = build_svg()
out = '../../svg_master/pentafix.svg'
with open(out, 'w', encoding='utf-8') as f:
 f.write(svg)
print(out + ' WRITTEN')
