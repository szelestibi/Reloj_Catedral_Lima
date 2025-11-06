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

def build_svg(id='disk'):
 d = ""
 # outer disc
 if id:
  d += circle_path(0, 0, R_DISK)
 timestamp = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
 svg = f'''<?xml version="1.0" encoding="UTF-8" ?><!-- generated with ../scripts/{os.path.splitext(os.path.basename(__file__))[0]}.py --><!-- SZT {timestamp} -->
<svg xmlns="http://www.w3.org/2000/svg" width="12cm" height="12cm" viewBox="-6 -6 12 12">
<defs><style>
 path {{ fill: rgba(30,60,90,.7); stroke: none; fill-rule:evenodd; }}
 #bgnd {{ fill: white; stroke: none; }}
</style></defs>
<rect id="bgnd" x="-6" y="-6" width="12" height="12" />
<path id="{id}" class="piece" d="{d.strip()}" />
</svg>'''
 return svg

print('')

R_DISK  = dimensions['mns_connect_wheel']['diameter'] / 20.0  # disk radius [cm]

svg = build_svg('disk')
out = '../../svg_master/MNS_disk.svg'
with open(out, 'w', encoding='utf-8') as f:
 f.write(svg)
print(out + ' WRITTEN')

R_DISK  = dimensions['hrs_connect_wheel']['diameter'] / 20.0  # disk radius [cm]

svg = build_svg('disk')
out = '../../svg_master/HRS_disk.svg'
with open(out, 'w', encoding='utf-8') as f:
 f.write(svg)
print(out + ' WRITTEN')
