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

def calc_px_py(r,a):
 ang = math.radians(a)
 px = r * math.cos(ang)
 py = r * math.sin(ang)
 return [px,py]

def build_command_axes():
 outtxt = ''
 ax_orbit_radius = dimensions['motor_axis']['orbit_radius'] / 10.0
 ax_radius = dimensions['motor_axis']['bearing_diameter'] / 20.0
 hrs_angle_1 = dimensions['motor_axis']['hrs_angle_1']
 x, y = calc_px_py(ax_orbit_radius,hrs_angle_1)
 outtxt = circle_path(x, y, ax_radius)
 hrs_angle_2 = dimensions['motor_axis']['hrs_angle_2']
 x, y = calc_px_py(ax_orbit_radius,hrs_angle_2)
 outtxt += circle_path(x, y, ax_radius)
 mns_angle_1 = dimensions['motor_axis']['mns_angle_1']
 x, y = calc_px_py(ax_orbit_radius,mns_angle_1)
 outtxt += circle_path(x, y, ax_radius)
 mns_angle_2 = dimensions['motor_axis']['mns_angle_2']
 x, y = calc_px_py(ax_orbit_radius,mns_angle_2)
 outtxt += circle_path(x, y, ax_radius)
 return outtxt

def build_command_trifixes():
 outtxt = ''

 def build_trifix(mx,my,mr,sr):
  txtout = ''
  for i in range(3):
   ang = math.radians(i * 120 + 30) # triangle sitting on base
   cx = mr * math.cos(ang) + mx
   cy = mr * math.sin(ang) + my
   txtout += circle_path(cx, cy, sr)
  return txtout
 radius_screw = dimensions['bearing_fixer_cmd']['screw_diameter'] / 20.0
 ax_orbit_radius = dimensions['motor_axis']['orbit_radius'] / 10.0
 ax_radius = dimensions['motor_axis']['bearing_diameter'] / 20.0 + 1 # one cm around of bearing
 hrs_angle_1 = dimensions['motor_axis']['hrs_angle_1']
 x, y = calc_px_py(ax_orbit_radius,hrs_angle_1)
 outtxt = build_trifix(x, y, ax_radius, radius_screw)
 hrs_angle_2 = dimensions['motor_axis']['hrs_angle_2']
 x, y = calc_px_py(ax_orbit_radius,hrs_angle_2)
 outtxt += build_trifix(x, y, ax_radius, radius_screw)
 mns_angle_1 = dimensions['motor_axis']['mns_angle_1']
 x, y = calc_px_py(ax_orbit_radius,mns_angle_1)
 outtxt += build_trifix(x, y, ax_radius, radius_screw)
 mns_angle_2 = dimensions['motor_axis']['mns_angle_2']
 x, y = calc_px_py(ax_orbit_radius,mns_angle_2)
 outtxt += build_trifix(x, y, ax_radius, radius_screw)
 return outtxt

def build_svg(wheel=False,hole=False,orbit=False,id="struts"):
 d = build_command_axes()
 d += build_command_trifixes()
 # four holes around at 90° steps
 if orbit:
  for i in range(4):
   ang = math.radians(i * 90.0 + 45)
   cx = R_ORBIT * math.cos(ang)
   cy = R_ORBIT * math.sin(ang)
   d += circle_path(cx, cy, R_SCREW)
 timestamp = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
 svg = f'''<?xml version="1.0" encoding="UTF-8" ?><!-- generated with ../scripts/{os.path.splitext(os.path.basename(__file__))[0]}.py --><!-- SZT {timestamp} -->
<svg xmlns="http://www.w3.org/2000/svg" width="138cm" height="138cm" viewBox="-69 -69 138 138">
<defs><style>
 path {{ fill: rgba(30,60,90,.7); stroke: none; fill-rule:evenodd; }}
 #bgnd {{ fill: #FFF; stroke: none; }}
</style></defs>
<rect id="bgnd" height="138" width="138" x="-69" y="-69" />
<path id="{id}" class="hole" d="{d.strip()}" />
</svg>'''
 return svg

R_SCREW = dimensions['panels']['strut_hole_diameter'] / 20.0 # fixing screw
R_ORBIT = dimensions['panels']['strut_orbit_radius']  / 10.0 # orbit radius

print('')

svg = build_svg(False,False,True)
out = '../../svg_master/panel_holes.svg'
with open(out, 'w', encoding='utf-8') as f:
 f.write(svg)
print(out + ' WRITTEN')
