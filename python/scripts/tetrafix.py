#!/usr/bin/python

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

def build_svg(tfid = 'TFXX'):
 d = ""
 # four holes around at 90° step
 for i in range(4):
  ang = math.radians(i * 90.0 - 45.0) # sitting square disposition
  cx = R_ORBIT * math.cos(ang)
  cy = R_ORBIT * math.sin(ang)
  d += circle_path(cx, cy, R_SCREW)
 svg = f'''<?xml version="1.0" encoding="UTF-8" ?><!-- generated with ../scripts/{os.path.splitext(os.path.basename(__file__))[0]}.py --><!-- SZT {datetime.now().strftime('%Y.%m.%d %H:%M:%S')} -->
<svg xmlns="http://www.w3.org/2000/svg" width="20cm" height="20cm" viewBox="-10 -10 20 20">
<defs><style>
 path {{ fill: rgba(30,60,90,.7); stroke: none; fill-rule:evenodd; }}
 #bgnd {{ fill: white; stroke: none; }}
</style></defs>
<rect id="bgnd" height="20" width="20" x="-10" y="-10" />
<path id="{tfid}" class="hole" d="{d.strip()}" />
</svg>'''
 return svg

print('')

R_SCREW = dimensions['tetrafix_48']['screw_diameter'] / 20.0 # fixing screw
R_ORBIT = dimensions['tetrafix_48']['orbit_radius']   / 10.0 # orbit radius

svg = build_svg('TF48')
out = '../../svg_master/tetrafix_48.svg'
with open(out, 'w', encoding='utf-8') as f:
 f.write(svg)
print(out + ' WRITTEN')

R_SCREW = dimensions['tetrafix_60']['screw_diameter'] / 20.0 # fixing screw
R_ORBIT = dimensions['tetrafix_60']['orbit_radius']   / 10.0 # orbit radius

svg = build_svg('TF60')
out = '../../svg_master/tetrafix_60.svg'
with open(out, 'w', encoding='utf-8') as f:
 f.write(svg)
print(out + ' WRITTEN')
