#!/usr/bin/python
# -*- coding: utf-8 -*-

from xml.dom import minidom
import inspect
import os
import sys

def join_paths(svg_file):
 print(f'this is join_paths({fi})')
 svgroot = minidom.parse(f'./{svg_file}.svg')
 paths = svgroot.getElementsByTagName('path')
 paths = [p for p in paths if p.hasAttribute('d')]
 if not paths:
  print('no <path> elements found')
  return
 if len(paths) == 1:
  with open(f'./{svg_file}_joined.svg', 'w', encoding='utf-8') as f:
   svgroot.writexml(f, encoding='utf-8')
  return
 first = paths[0]
 first_id = first.getAttribute('id') or 'combined_path'
 combined_d = ''
 for p in paths:
  d = p.getAttribute('d')
  if not d:
   continue
  if combined_d:
   combined_d += ' '
  combined_d += d
 first.setAttribute('id', first_id)
 first.setAttribute('d', combined_d)
 for p in paths[1:]:
  parent = p.parentNode
  parent.removeChild(p)
 with open(f'./{svg_file}_joined.svg', 'w', encoding='utf-8') as f:
  svgroot.writexml(f, encoding='utf-8')
 svgroot.unlink()

if __name__ == '__main__':
 svg_files = [f[:-4] for f in os.listdir('./') if f.endswith('.svg')]
 for fi in svg_files:
  join_paths(fi)
 pass
