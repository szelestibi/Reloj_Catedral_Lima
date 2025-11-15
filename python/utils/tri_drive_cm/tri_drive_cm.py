#!/usr/bin/python
# -*- coding: utf-8 -*-

from xml.dom import minidom
import math

# --- SETTINGS BEGIN ----------------------------------
gridfile = './grid_130x130.svg'
grid = True
#grid = False
slots = 60   # MNS
# slots = 48 # HRS
# given R, calculate C -------
# R_cm = 70                  # big wheel radius
# C_cm = math.pi * 2 * R_cm  # big wheel circumference
# given C, calculate R -------
C_cm = 360                   # big wheel circumference
R_cm = C_cm / (2 * math.pi)  # big wheel radius
# also needed in settings: ---
o_cm = 2                     # driving pin diameter
print(f'''
--- INPUT --------------------
slots:            {slots:5d}
wheel:
 radius:           {R_cm:8.3f} cm
 circumference:    {C_cm:8.3f} cm
pin diameter:      {o_cm:8.3f} cm''')
# --- SETTINGS END ------------------------------------

# --- DERIVATED VALUES CALC BEGIN ---------------------
P_cm = 2 * R_cm * math.sin(2 * math.pi / (slots * 2))
d_cm = P_cm / math.sqrt(3)
D_cm = d_cm / 2 + R_cm * math.cos(2 * math.pi / (slots * 2))
rounding_delta = o_cm / 10
A_deg = 360 / slots
print(f'''
--- CALCULATED DATA ----------
slots distance:
 angular:          {(A_deg):8.3f} °
 on circumference: {(C_cm / slots):8.3f} cm
 direct = linear:  {(P_cm):8.3f} cm
driver pin:
 axis distance:    {D_cm:8.3f} cm
 orbiting radius:  {d_cm:8.3f} cm
''')
# --- DERIVATED VALUES CALC END -----------------------

svgroot = {}
svgmain = None

import math

class Point:
 def __init__(self, x, y):
  self.x = x
  self.y = y
 def __repr__(self):
  return f'Point(x={self.x}, y={self.y})'
 def rotate(self, angle_deg):
  a = math.radians(angle_deg)
  x = self.x
  y = self.y
  self.x = x * math.cos(a) - y * math.sin(a)
  self.y = x * math.sin(a) + y * math.cos(a)
  return self
 def y_from_x(self, r):
  x = self.x
  self.y = math.sqrt(r*r - x*x)
  return self

def remove_grid():
 global svgroot
 for g in svgroot.getElementsByTagName('g'):
  if g.getAttribute('id') == 'grid':
   g.parentNode.removeChild(g)
   break

def remove_whitespace_nodes(node):
 remove = []
 for child in node.childNodes:
  if child.nodeType == child.TEXT_NODE and child.data.strip() == '':
   remove.append(child)
  elif child.hasChildNodes():
   remove_whitespace_nodes(child)
 for child in remove:
  node.removeChild(child)

def circle_path(C, r): # circle as two 180° arcs for compound path
 return f'M {float_shorten(C.x - r)} {float_shorten(C.y)} a {float_shorten(r)} {float_shorten(r)} 0 1 0 {float_shorten(2*r)} 0 a {float_shorten(r)} {float_shorten(r)} 0 1 0 {float_shorten(-2*r)} 0 Z '

def float_shorten(f):
 if f == 0:
  return '0'
 if isinstance(f, float):
  ff = f'{f:.3f}'.rstrip('0').rstrip('.')
  if ff.startswith('0.'): ff = ff[1:]
  if ff.startswith('-0.'): ff = '-' + ff[2:]
  return ff
 else:
  return str(f)

def add_marker(M):
 global svgroot, svgmain
 circle = svgroot.createElement('circle')
 circle.setAttribute('class','marker')
 circle.setAttribute('cx',float_shorten(M.x))
 circle.setAttribute('cy',float_shorten(M.y))
 circle.setAttribute('r','.1')
 svgmain = svgroot.getElementsByTagName('svg')[0]
 svgmain.appendChild(circle)

def add_circle(id,cl,C,r):
 global svgroot, svgmain
 circle = svgroot.createElement('circle')
 if id != '':
  circle.setAttribute('id',id)
 if cl != '':
  circle.setAttribute('class',cl)
 circle.setAttribute('cx',float_shorten(C.x))
 circle.setAttribute('cy',float_shorten(C.y))
 circle.setAttribute('r',float_shorten(r))
 svgmain.appendChild(circle)

def add_path(id,cl,d):
 global svgroot, svgmain
 path = svgroot.createElement('path')
 if id != '':
  path.setAttribute('id',id)
 if cl != '':
  path.setAttribute('class',cl)
 path.setAttribute('d',d)
 svgmain.appendChild(path)

def load_grid():
 global svgroot, svgmain
 svgroot = minidom.parse(gridfile)
 svgmain = svgroot.getElementsByTagName('svg')[0]

def make_wheel():
 global svgroot, svgmain, A_deg, D_cm, R_cm, d_cm, o_cm, rounding_delta
 act_ang = 0
 # rot_ang = 0
 # rot_ang = A_deg / 2
 #A = Point(o_cm/2 + rounding_delta,R_cm).y_from_x(R_cm).rotate(rot_ang)
 #B = Point(o_cm/2,R_cm).y_from_x(R_cm - rounding_delta).rotate(rot_ang)
 #M = Point(o_cm/2,R_cm).y_from_x(D_cm - d_cm).rotate(rot_ang)
 #N = Point(-o_cm/2,R_cm).y_from_x(D_cm - d_cm).rotate(rot_ang)
 #C = Point(-o_cm/2,R_cm).y_from_x(R_cm - rounding_delta).rotate(rot_ang)
 #D = Point(-o_cm/2 - rounding_delta,R_cm).y_from_x(R_cm).rotate(rot_ang)
 #E = Point(A.x,A.y).rotate(A_deg)
 #add_marker(A)
 #add_marker(B)
 #add_marker(M)
 #add_marker(N)
 #add_marker(C)
 #add_marker(D)
 #add_marker(E)
 A = Point(o_cm/2 + rounding_delta,R_cm).y_from_x(R_cm)
 d = f'M {float_shorten(A.x)} {float_shorten(A.y)} '
 while act_ang < 360:
  A = Point(o_cm/2 + rounding_delta,R_cm).y_from_x(R_cm).rotate(act_ang)
  B = Point(o_cm/2,R_cm).y_from_x(R_cm - rounding_delta).rotate(act_ang)
  M = Point(o_cm/2,R_cm).y_from_x(D_cm - d_cm).rotate(act_ang)
  N = Point(-o_cm/2,R_cm).y_from_x(D_cm - d_cm).rotate(act_ang)
  C = Point(-o_cm/2,R_cm).y_from_x(R_cm - rounding_delta).rotate(act_ang)
  D = Point(-o_cm/2 - rounding_delta,R_cm).y_from_x(R_cm).rotate(act_ang)
  E = Point(A.x,A.y).rotate(A_deg)
  path = svgroot.createElement('path')
  path.setAttribute('id', 'wheel')
  path.setAttribute('transform', f'rotate({A_deg / 2})')
  d += f'A {float_shorten(rounding_delta)} {float_shorten(rounding_delta)} 0 0 1 {float_shorten(B.x)} {float_shorten(B.y)} L {float_shorten(M.x)} {float_shorten(M.y)} ' + \
       f'A {float_shorten(o_cm/2)} {float_shorten(o_cm/2)} 0 0 0 {float_shorten(N.x)} {float_shorten(N.y)} L {float_shorten(C.x)} {float_shorten(C.y)} ' + \
       f'A {float_shorten(rounding_delta)} {float_shorten(rounding_delta)} 0 0 1 {float_shorten(D.x)} {float_shorten(D.y)} ' + \
       f'A {float_shorten(R_cm)} {float_shorten(R_cm)} 0 0 1 {float_shorten(E.x)} {float_shorten(E.y)} '
  act_ang += A_deg
 d += 'Z '
 path.setAttribute('d', d.strip())
 svgmain.appendChild(path)

def make_driver():
 global svgroot, svgmain, D_cm, R_cm, d_cm, o_cm
 add_marker(Point(0,D_cm))
 path = svgroot.createElement('path')
 path.setAttribute('id', 'driver')
 path.setAttribute('transform', f'translate(0 {float_shorten(D_cm)}) rotate(120)')
 # CC = circle_path(Point(0, 0), d_cm)
 d = circle_path(Point(0, d_cm).rotate(0), o_cm/2) + circle_path(Point(0, d_cm).rotate(120), o_cm/2) + circle_path(Point(0, d_cm).rotate(240), o_cm/2)
 # d += CC
 path.setAttribute('d', d)
 svgmain.appendChild(path)

if __name__ == '__main__':
 load_grid()
 make_driver()
 make_wheel()
 # add_circle('','',Point(0,0),D_cm - d_cm)
 # add_circle('','',Point(0,0),D_cm - d_cm - o_cm / 2)
 if grid == False:
  remove_grid()
 remove_whitespace_nodes(svgroot)
 with open(f'./tri_drive_cm.svg', 'w', encoding='utf-8') as f:
  svgroot.writexml(f, newl='\n', encoding='utf-8')
  # svgroot.writexml(f, indent='', addindent='', newl='\n', encoding='utf-8')
 svgroot.unlink()
