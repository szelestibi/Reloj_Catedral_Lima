#!/usr/bin/python
# -*- coding: utf-8 -*-

from xml.dom import minidom
import inspect
import svgx

piece_style = {}

def load():
 # print(f'this is piece.load({p})')
 global piece_style
 svgroot = minidom.parse('../../svg_master/' + 'style_global' + '.svg')
 piece_style = svgx.by_id(svgroot, 'global_style')
 return piece_style
