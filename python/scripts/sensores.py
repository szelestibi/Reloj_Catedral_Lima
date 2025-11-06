#!/usr/bin/python
# -*- coding: utf-8 -*-

# liston con sensores magneticos 5 cm de ancho
# posiciones de los sensores magneticos [cm]:
# 36 --- 39.000 - 40.524 - 42.048 - 43.572 --- 46.5 --- 56.0
#         MAG3     MAG2     MAG1     MAG0        circuito

from datetime import datetime
import math
import os
import yaml

x_positions = []  # mm - posiciones de los imanes / sensores
y_pos_sensr = 0   # sensor position Y
y_pos_termx = 3   # terminal hole position Y
A3141_diamt = 5.2 # mm - mag sensor like A3141 or SS41
A3141_width = 4.2 # mm - mag sensor like A3141 or SS41
A3141_hight = 3.2 # mm - mag sensor like A3141 or SS41
termh_width = 3.0 # mm - terminal hole width
termh_hight = 1.0 # mm - terminal hole height

def rctang_path(cx, cy, w, h):
 return f'M {float_shorten(cx - w/2)} {float_shorten(cy - h/2)} H {float_shorten(cx + w/2)} V {float_shorten(cy + h/2)} H {float_shorten(cx - w/2)} Z '

def circle_path(cx, cy, r): # circle as two 180° arcs for compound path
 return f'M {float_shorten(cx - r)} {float_shorten(cy)} a {float_shorten(r)} {float_shorten(r)} 0 1 0 {float_shorten(2*r)} 0 a {float_shorten(r)} {float_shorten(r)} 0 1 0 {float_shorten(-2*r)} 0 Z '

def rounded_rectangle(c0,c1,c2,c3,r):
 return f'M {float_shorten(c0[0])} {float_shorten(c0[1]+r)} A {r} {r} 0 0 1 {float_shorten(c0[0]+r)} {float_shorten(c0[1])} H {float_shorten(c1[0]-r)} A {r} {r} 0 0 1 {float_shorten(c1[0])} {float_shorten(c1[1]+r)} V {float_shorten(c2[1]-r)} A {r} {r} 0 0 1 {float_shorten(c2[0]-r)} {float_shorten(c2[1])} H {float_shorten(c3[0]+r)} A {r} {r} 0 0 1 {float_shorten(c3[0])} {float_shorten(c3[1]-r)} Z '

def build_sensor_positions():
 outtxt = ''
 for pos in x_positions:
  # outtxt += circle_path(pos / 10, y_pos_sensr, A3141_diamt / 20)
  outtxt += rctang_path(pos / 10, y_pos_sensr / 10, A3141_width / 10, A3141_hight / 10)
  outtxt += rctang_path(pos / 10, y_pos_termx / 10, termh_width / 10, termh_hight / 10)
 return outtxt

def float_shorten(f):
 ff = f'{f:.3f}'.rstrip('0').rstrip('.')
 if ff.startswith('0.'): ff = ff[1:]
 if ff.startswith('-0.'): ff = '-' + ff[2:]
 return ff

def build_svg(id='mags'):
 d = rounded_rectangle([-56, -2.5],[-36, -2.5],[-36, 2.5],[-56, 2.5],.5)
 d += build_sensor_positions()
 timestamp = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
 svg = f'''<?xml version="1.0" encoding="UTF-8" ?><!-- generated with ../scripts/{os.path.splitext(os.path.basename(__file__))[0]}.py --><!-- SZT {timestamp} -->
<svg xmlns="http://www.w3.org/2000/svg" width="22cm" height="7cm" viewBox="-57 -3.5 22 7">
<defs><style>
 path {{ fill: rgba(30,60,90,.7); stroke: none; fill-rule:evenodd; }}
 #bgnd {{ fill: #FFF; stroke: none; }}
</style></defs>
<rect id="bgnd" height="7" width="22" x="-57" y="-3.5" />
<path id="{id}" class="piece" d="{d.strip()}" />
</svg>'''
 return svg

print('')

with open('../yaml/dimensiones.yaml', 'r', encoding='utf-8') as f:
 dimensions = yaml.safe_load(f).get('dimensions', {})

x_positions = dimensions['sensor_board']['mags_positions']

svg = build_svg('mags')
out = '../../svg_master/sensores.svg'
with open(out, 'w', encoding='utf-8') as f:
 f.write(svg)
print(out + ' WRITTEN')
