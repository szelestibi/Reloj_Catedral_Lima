#!/usr/bin/python
# -*- coding: utf-8 -*-

# patas de sostenimiento

from xml.dom import minidom
import math, os, sys, time, yaml
sys.path.insert(0, "/home/tiberio/Work/RCL/proyecto/python/modules/")
import cfgx
import style
import grid
import piece
import svgx

# --------- CONFIG BEGIN ------------------------------------
UNIT = 'MECANISMO'
SVGX = os.path.splitext(os.path.basename(__file__))[0]
PART = SVGX[5:]
# --------- CONFIG END --------------------------------------

cfgx.load()
style.load()
grid.load(cfgx.makedata[UNIT][PART]['grid'],cfgx.makedata['GRID'])
piece.load(cfgx.makedata[UNIT][PART])

# print('')
# print(style.piece_style)
# print(grid.grid)
# print(piece.piecedata)

svg_out = svgx.make(UNIT,SVGX) # svg to output

# time.sleep(1)
