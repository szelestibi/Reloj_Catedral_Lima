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

def build_svg(id='OJOP'):
 d = ""
 # outer disc
 if id:
  d += circle_path(0, -R_ORBIT, R_SCREW)
 timestamp = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
 svg = f'''<?xml version="1.0" encoding="UTF-8" ?><!-- generated with ../scripts/{os.path.splitext(os.path.basename(__file__))[0]}.py --><!-- SZT {timestamp} -->
<svg xmlns="http://www.w3.org/2000/svg" width="2cm" height="2cm" viewBox="-1 -47.5 2 2">
<defs><style>
 path {{ fill: rgba(30,60,90,.7); stroke: none; fill-rule:evenodd; }}
 #bgnd {{ fill: white; stroke: none; }}
</style></defs>
<rect id="bgnd" x="-1" y="-47.5" width="2" height="2" />
<path id="{id}" class="hole" d="{d.strip()}" />
</svg>'''
 return svg

print('')

R_ORBIT  = dimensions['ojo_contrapeso']['orbit']    /  10.0 # centered orbit
R_SCREW  = dimensions['ojo_contrapeso']['diameter'] / 20.0  # screw hole radius [cm]

svg = build_svg('OJOP')
out = '../../svg_master/ojo_contrapeso.svg'
with open(out, 'w', encoding='utf-8') as f:
 f.write(svg)
print(out + ' WRITTEN')
