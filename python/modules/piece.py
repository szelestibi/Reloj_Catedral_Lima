#!/usr/bin/python
# -*- coding: utf-8 -*-

from xml.dom import minidom
import inspect
import svgx

piecedata = {}

def load(p):
 # print(f'this is piece.load({p})')
 global piecedata
 svgroot = minidom.parse('../../svg_master/' + p['piece'] + '.svg')
 if p['mainline'] != None:
  piecedata['opening_tag'] = svgx.get_svg_opening_tag(svgroot)
  piecedata['mainline'] = svgx.by_id(svgroot, p['mainline'])
  if 'include' in p and p['include'] != None:
   for incl in p['include']:
    piecedata[incl] = svgx.by_id(svgroot, incl)
 else: piecedata['svgroot'] = svgroot
