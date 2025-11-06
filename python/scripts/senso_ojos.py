#!/usr/bin/python
# -*- coding: utf-8 -*-

# ojos para fijar el listón de sensores

from datetime import datetime
import os
import yaml

def build_ojos():
 ojos = [[-55.5, -2], [-36.5, -2], [-55.5, 2], [-36.5, 2]]
 diam_ojo = dimensions['sensor_board']['screw_diameter'] / 20
 outtxt = ''
 for ojo in ojos:
  outtxt += circle_path(ojo[0], ojo[1], diam_ojo)
 return outtxt

def float_shorten(f):
 ff = f'{f:.3f}'.rstrip('0').rstrip('.')
 if ff.startswith('0.'): ff = ff[1:]
 if ff.startswith('-0.'): ff = '-' + ff[2:]
 return ff

def circle_path(cx, cy, r): # circle as two 180° arcs for compound path
 return (f"M {float_shorten(cx - r)} {float_shorten(cy)} a {float_shorten(r)} {float_shorten(r)} 0 1 0 {float_shorten(2*r)} 0 a {float_shorten(r)} {float_shorten(r)} 0 1 0 {float_shorten(-2*r)} 0 Z ")

def rounded_rectangle(c0,c1,c2,c3,r):
 return f'M {float_shorten(c0[0])} {float_shorten(c0[1]+r)} A {r} {r} 0 0 1 {float_shorten(c0[0]+r)} {float_shorten(c0[1])} H {float_shorten(c1[0]-r)} A {r} {r} 0 0 1 {float_shorten(c1[0])} {float_shorten(c1[1]+r)} V {float_shorten(c2[1]-r)} A {r} {r} 0 0 1 {float_shorten(c2[0]-r)} {float_shorten(c2[1])} H {float_shorten(c3[0]+r)} A {r} {r} 0 0 1 {float_shorten(c3[0])} {float_shorten(c3[1]-r)} Z '

def build_svg(id='ojos'):
 d= ''
 # d += rounded_rectangle([-56, -2.5],[-36, -2.5],[-36, 2.5],[-56, 2.5],.5)
 d += build_ojos()
 timestamp = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
 svg = f'''<?xml version="1.0" encoding="UTF-8" ?><!-- generated with ../scripts/{os.path.splitext(os.path.basename(__file__))[0]}.py --><!-- SZT {timestamp} -->
<svg xmlns="http://www.w3.org/2000/svg" width="22cm" height="7cm" viewBox="-57 -3.5 22 7">
<defs><style>
 path {{ fill: rgba(30,60,90,.7); stroke: none; fill-rule:evenodd; }}
 #bgnd {{ fill: #FFF; stroke: none; }}
</style></defs>
<rect id="bgnd" height="7" width="22" x="-57" y="-3.5" />
<path id="{id}" class="hole" d="{d.strip()}" />
</svg>'''
 return svg

with open('../yaml/dimensiones.yaml', 'r', encoding='utf-8') as f:
 dimensions = yaml.safe_load(f).get('dimensions', {})

print('')

svg = build_svg('ojos')
out = '../../svg_master/senso_ojos.svg'
with open(out, 'w', encoding='utf-8') as f:
 f.write(svg)
print(out + ' WRITTEN')
