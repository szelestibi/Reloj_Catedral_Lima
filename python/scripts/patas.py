#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
import math
import os
import yaml

class Point:
 def __init__(self, x, y):
  self.x = x
  self.y = y
 def __repr__(self):
  return f'Point(x={self.x}, y={self.y})'

with open('../yaml/dimensiones.yaml', 'r', encoding='utf-8') as f:
 dimensions = yaml.safe_load(f).get('dimensions', {})

show_panel = True # show panel ... para tener una idea ...

r_metal = dimensions['panel_metal_rs']
r_bigxx = dimensions['foot_stand_rb']
r_small = dimensions['foot_stand_rx']
a_optim = dimensions['foot_stand_ax']

struct_holes_orbit = dimensions['panels']['strut_orbit_radius'] / 10.0
struct_holes_radius = dimensions['panels']['strut_hole_diameter'] / 20.0

outstand = dimensions['foot_outstand']
backlevel = 1 # feet backlevel

def calc_px_py(x,y,r,a):
 ang = math.radians(a)
 px = r * math.cos(ang) + x
 py = r * math.sin(ang) + y
 return [px,py]

def float_shorten(f):
 ff = f'{f:.3f}'.rstrip('0').rstrip('.')
 if ff.startswith('0.'): ff = ff[1:]
 if ff.startswith('-0.'): ff = '-' + ff[2:]
 return ff

def circle_path(cx, cy, r): # circle as two 180° arcs for compound path
 return f'M {float_shorten(cx - r)} {float_shorten(cy)} a {float_shorten(r)} {float_shorten(r)} 0 1 0 {float_shorten(2*r)} 0 a {float_shorten(r)} {float_shorten(r)} 0 1 0 {float_shorten(-2*r)} 0 Z '

def add_struct_holes():
 outtxt = ''
 an = math.radians(45)
 px = struct_holes_orbit * math.cos(an)
 py = struct_holes_orbit * math.sin(an)
 outtxt += circle_path(px, py, struct_holes_radius)
 an = math.radians(135)
 px = struct_holes_orbit * math.cos(an)
 py = struct_holes_orbit * math.sin(an)
 outtxt += circle_path(px, py, struct_holes_radius)
 return outtxt

def build_svg():
 P0 = calc_px_py(-50, 50,r_metal,180)
 P1 = calc_px_py(-50, 50,r_metal,360 - a_optim)
 P2 = calc_px_py( 50, 50,r_metal,180 + a_optim)
 P3 = calc_px_py( 50, 50,r_metal,  0)

 P00 = float_shorten(P0[0])
 P01 = float_shorten(P0[1])
 P10 = float_shorten(P1[0])
 P11 = float_shorten(P1[1])
 P20 = float_shorten(P2[0])
 P21 = float_shorten(P2[1])
 P30 = float_shorten(P3[0])
 P31 = float_shorten(P3[1])

 p4 = calc_px_py( 59, 59,r_small,  0)
 p5 = calc_px_py( 59, 59,r_small, 90)
 p6 = calc_px_py(-59, 59,r_small, 90)
 p7 = calc_px_py(-59, 59,r_small,180)

 p40 = float_shorten(p4[0])
 p41 = float_shorten(60 - r_small + outstand)
 p50 = float_shorten(P3[0] - r_small)
 p51 = float_shorten(60 + outstand)
 p60 = float_shorten(P0[0] + r_small)
 p61 = float_shorten(p6[1])
 p70 = float_shorten(P0[0])
 p71 = float_shorten(60 - r_small + outstand)

 A = Point(0,0)
 B = Point(0,0)
 C = Point(0,0)
 D = Point(0,0)
 E = Point(0,0)
 F = Point(0,0)

 pata = f'M {P00} {P01} A {r_metal} {r_metal} 0 0 1 {P10} {P11} A {r_bigxx} {r_bigxx} 0 0 0 {P20} {P21} ' \
                       + f'A {r_metal} {r_metal} 0 0 1 {P30} {P31} V {p41} A {r_small} {r_small} 0 0 1 {p50} {p51} ' \
                       + f'{''} H {p60} ' \
                       + f'A {r_small} {r_small} 0 0 1 {p70} {p71} Z'
 pata += add_struct_holes()
 timestamp = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
 svg = f'''<?xml version="1.0" encoding="UTF-8" ?><!-- generated with ../scripts/{os.path.splitext(os.path.basename(__file__))[0]}.py --><!-- SZT {timestamp} -->
<svg xmlns="http://www.w3.org/2000/svg" width="138cm" height="138cm" viewBox="-69 -69 138 138">
<defs><style type="text/css">
 #pata {{ fill:#204060; fill-opacity:.7; fill-rule:evenodd; stroke:none; }}
 #bgnd {{ fill:white; }}
</style></defs>
<rect id="bgnd" height="138" width="138" x="-69" y="-69" />
{'<path id="panel" style="fill:rgba(30,60,90,.2); fill-rule:evenodd; stroke:none;" d="M -57 -60 H 57 A 3 3 0 0 1 60 -57 V 57 A 3 3 0 0 1 57 60 H 50.5 A .5 .5 0 0 0 49.5 60 H .5 A .5 .5 0 0 0 -.5 60 H -57 A 3 3 0 0 1 -60 57 V -57 A 3 3 0 0 1 -57 -60 Z M -55.657 -44.343 A 8 8 0 0 1 -44.343 -55.657 A 58 58 0 0 0 44.343 -55.657 A 8 8 0 0 1 55.657 -44.343 A 58 58 0 0 0 55.657 44.343 A 8 8 0 0 1 44.343 55.657 A 58 58 0 0 0 -44.343 55.657 A 8 8 0 0 1 -55.657 44.343 A 58 58 0 0 0 -55.657 -44.343 Z " />' if (show_panel == True) else ''}
<path id="pata" d="{pata.strip()}" />
</svg>
'''
 return svg

svg = build_svg()
out = '../../svg_master/patas.svg'
with open(out, 'w', encoding='utf-8') as f:
 f.write(svg)
print(out + ' WRITTEN')
