#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
#
# SVG → DXF converter (units → millimeters)
# - Handles: <path>, <line>, <polyline>, <polygon>, <rect>, <circle>, <ellipse>
# - Flattens curves into polylines with configurable tolerance
#
# Usage:
#   python svg_to_dxf_mm.py input.svg output.dxf --tolerance 0.2 --layer Cuts
#
# Notes:
# - SVG user units are px at 96 dpi. We map 1 px = 25.4/96 mm.
# - If your SVG uses cm or mm, parsers normalize them; this script still scales to mm.

import argparse
import math
from typing import List, Tuple

import ezdxf
from svgelements import SVG, Path, Line, Polyline, Polygon, Rect, Circle, Ellipse

PX_TO_MM = 25.4 / 96.0  # Inkscape/SVG spec: 96 px = 1 inch

def linspace(a: float, b: float, n: int) -> List[float]:
  if n <= 1:
    return [a]
  step = (b - a) / (n - 1)
  return [a + i * step for i in range(n)]

def flatten_path(path: Path, tol: float) -> List[List[Tuple[float, float]]]:
  """
  Convert any Path to a list of polylines (each a list of (x,y) pairs),
  sampling each segment to approximate curves. tol ≈ max segment length in mm.
  """
  polylines: List[List[Tuple[float, float]]] = []
  current: List[Tuple[float, float]] = []

  # Heuristic: number of samples per segment based on length and tolerance
  for seg in path.segments():
    # segment length in px → mm for sampling decision
    try:
      seg_len_px = seg.length(error=1.0)  # svgelements provides length() for segments
    except Exception:
      # Fallback if not available
      seg_len_px = 10.0
    seg_len_mm = seg_len_px * PX_TO_MM
    samples = max(2, int(math.ceil(seg_len_mm / max(tol, 0.01))) + 1)

    pts: List[Tuple[float, float]] = []
    for t in linspace(0.0, 1.0, samples):
      p = seg.point(t)
      pts.append((p.x * PX_TO_MM, p.y * PX_TO_MM))

    if not current:
      current.extend(pts)
    else:
      # avoid duplicating the seam point
      current.extend(pts[1:])

    # If the segment ends a subpath, close the current polyline if needed
    if getattr(seg, "end", None) and getattr(seg, "start", None):
      # svgelements Path manages subpaths; we’ll break only at explicit MOVETO
      pass

  # Split into real subpaths (svgelements Path already keeps them; we rebuild)
  # Here we detect moveto indices to split polylines.
  # Simple approach: use path.as_subpaths()
  try:
    polylines = []
    for sp in path.as_subpaths():
      sub: List[Tuple[float, float]] = []
      for seg in sp.segments():
        try:
          seg_len_px = seg.length(error=1.0)
        except Exception:
          seg_len_px = 10.0
        seg_len_mm = seg_len_px * PX_TO_MM
        samples = max(2, int(math.ceil(seg_len_mm / max(tol, 0.01))) + 1)
        for t in linspace(0.0, 1.0, samples):
          p = seg.point(t)
          sub.append((p.x * PX_TO_MM, p.y * PX_TO_MM))
      # remove consecutive duplicates
      clean = [sub[0]] if sub else []
      for q in sub[1:]:
        if q != clean[-1]:
          clean.append(q)
      if clean:
        polylines.append(clean)
  except Exception:
    # fallback: single polyline
    if current:
      polylines = [current]

  return polylines

def rect_to_poly(r: Rect) -> List[Tuple[float, float]]:
  x0 = float(r.x) * PX_TO_MM
  y0 = float(r.y) * PX_TO_MM
  x1 = (float(r.x) + float(r.width)) * PX_TO_MM
  y1 = (float(r.y) + float(r.height)) * PX_TO_MM
  return [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]

def ellipse_to_poly(e: Ellipse, tol: float) -> List[Tuple[float, float]]:
  # Sample ellipse perimeter with step ≈ tol
  rx_px = float(e.rx)
  ry_px = float(e.ry)
  cx_px = float(e.cx)
  cy_px = float(e.cy)
  # circumference approx (Ramanujan) in px
  a = rx_px
  b = ry_px
  h = ((a - b) ** 2) / ((a + b) ** 2) if (a + b) != 0 else 0
  circ_px = math.pi * (a + b) * (1 + (3*h) / (10 + math.sqrt(4 - 3*h)))
  circ_mm = circ_px * PX_TO_MM
  n = max(12, int(math.ceil(circ_mm / max(tol, 0.01))))
  pts = []
  for i in range(n + 1):
    t = 2 * math.pi * i / n
    x = cx_px + rx_px * math.cos(t)
    y = cy_px + ry_px * math.sin(t)
    pts.append((x * PX_TO_MM, y * PX_TO_MM))
  return pts

'''
def circle_to_poly(c: Circle, tol: float) -> List[Tuple[float, float]]:
  e = Ellipse(cx=c.cx, cy=c.cy, rx=c.r, ry=c.r)
  return ellipse_to_poly(e, tol)
'''

def circle_to_poly(c: Circle, tol: float) -> List[Tuple[float, float]]:
  # Circle in svgelements has rx = ry = radius
  e = Ellipse(cx=c.cx, cy=c.cy, rx=c.rx, ry=c.ry)
  return ellipse_to_poly(e, tol)


def write_polylines(msp, polylines: List[List[Tuple[float, float]]], layer: str):
  for pts in polylines:
    if len(pts) >= 2:
      msp.add_lwpolyline(pts, dxfattribs={"layer": layer})

def main():
  ap = argparse.ArgumentParser(description="Convert SVG to DXF (units → millimeters).")
  ap.add_argument("input_svg", help="Input SVG file")
  ap.add_argument("output_dxf", help="Output DXF file")
  ap.add_argument("--tolerance", type=float, default=0.25,
                  help="Max segment length for curve flattening in mm (default: 0.25)")
  ap.add_argument("--layer", type=str, default="CUTS",
                  help="DXF layer name (default: CUTS)")
  args = ap.parse_args()

  svg = SVG.parse(args.input_svg)

  doc = ezdxf.new(setup=True)
  # doc.units = ezdxf.units.MM  # mark as mm; many CADs honor this
  doc.header['$INSUNITS'] = 4  # 4 = millimeters
  if args.layer not in doc.layers:
    doc.layers.new(name=args.layer)
  msp = doc.modelspace()

  for el in svg.elements():
    if isinstance(el, Path):
      # Flatten any path to polylines
      pl = flatten_path(el, tol=args.tolerance)
      write_polylines(msp, pl, args.layer)

    elif isinstance(el, Line):
      x1 = float(el.x1) * PX_TO_MM
      y1 = float(el.y1) * PX_TO_MM
      x2 = float(el.x2) * PX_TO_MM
      y2 = float(el.y2) * PX_TO_MM
      msp.add_line((x1, y1), (x2, y2), dxfattribs={"layer": args.layer})

    elif isinstance(el, Polyline):
      pts = [(float(p[0]) * PX_TO_MM, float(p[1]) * PX_TO_MM) for p in el]
      write_polylines(msp, [pts], args.layer)

    elif isinstance(el, Polygon):
      pts = [(float(p[0]) * PX_TO_MM, float(p[1]) * PX_TO_MM) for p in el]
      if pts and pts[0] != pts[-1]:
        pts.append(pts[0])
      write_polylines(msp, [pts], args.layer)

    elif isinstance(el, Rect):
      pts = rect_to_poly(el)
      write_polylines(msp, [pts], args.layer)

    elif isinstance(el, Circle):
      pts = circle_to_poly(el, args.tolerance)
      write_polylines(msp, [pts], args.layer)

    elif isinstance(el, Ellipse):
      pts = ellipse_to_poly(el, args.tolerance)
      write_polylines(msp, [pts], args.layer)

    else:
      # Ignore text, images, etc. (can be added if needed)
      continue

  doc.saveas(args.output_dxf)
  print(f"Done. Wrote DXF in millimeters to: {args.output_dxf}")

if __name__ == "__main__":
  main()
