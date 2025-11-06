#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
import math
import os
import yaml

with open('../yaml/dimensiones.yaml', 'r', encoding='utf-8') as f:
 dimensions = yaml.safe_load(f).get('dimensions', {})

r_metal = dimensions['panel_metal_rs']
r_bigxx = dimensions['panel_metal_rb']

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

def build_svg():
 P0 = calc_px_py(-50,-50,r_metal,135)
 P1 = calc_px_py(-50,-50,r_metal,315)
 P2 = calc_px_py( 50,-50,r_metal,225)
 P3 = calc_px_py( 50,-50,r_metal, 45)
 P4 = calc_px_py( 50, 50,r_metal,315)
 P5 = calc_px_py( 50, 50,r_metal,135)
 P6 = calc_px_py(-50, 50,r_metal, 45)
 P7 = calc_px_py(-50, 50,r_metal,225)
 P00 = float_shorten(P0[0])
 P01 = float_shorten(P0[1])
 P10 = float_shorten(P1[0])
 P11 = float_shorten(P1[1])
 P20 = float_shorten(P2[0])
 P21 = float_shorten(P2[1])
 P30 = float_shorten(P3[0])
 P31 = float_shorten(P3[1])
 P40 = float_shorten(P4[0])
 P41 = float_shorten(P4[1])
 P50 = float_shorten(P5[0])
 P51 = float_shorten(P5[1])
 P60 = float_shorten(P6[0])
 P61 = float_shorten(P6[1])
 P70 = float_shorten(P7[0])
 P71 = float_shorten(P7[1])
 d_metal = f'M {P00} {P01} A {r_metal} {r_metal} 0 0 1 {P10} {P11} A {r_bigxx} {r_bigxx} 0 0 0 {P20} {P21} ' \
                       + f'A {r_metal} {r_metal} 0 0 1 {P30} {P31} A {r_bigxx} {r_bigxx} 0 0 0 {P40} {P41} ' \
                       + f'A {r_metal} {r_metal} 0 0 1 {P50} {P51} A {r_bigxx} {r_bigxx} 0 0 0 {P60} {P61} ' \
                       + f'A {r_metal} {r_metal} 0 0 1 {P70} {P71} A {r_bigxx} {r_bigxx} 0 0 0 {P00} {P01} Z'
 timestamp = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
 svg = f'''<?xml version="1.0" encoding="UTF-8" ?><!-- generated with ../scripts/{os.path.splitext(os.path.basename(__file__))[0]}.py --><!-- SZT {timestamp} -->
<svg xmlns="http://www.w3.org/2000/svg" width="138cm" height="138cm" viewBox="-69 -69 138 138">
<defs><style type="text/css">
 #metal {{ fill:#204060; fill-opacity:.7; fill-rule:evenodd; stroke:none; }}
 #bgnd {{ fill:white; }}
</style></defs>
<rect id="bgnd" height="138" width="138" x="-69" y="-69" />
<path id="metal" d="{d_metal.strip()}" />
</svg>
'''
 return svg

svg = build_svg()
out = '../../svg_master/panel_metal.svg'
with open(out, 'w', encoding='utf-8') as f:
 f.write(svg)
print(out + ' WRITTEN')
