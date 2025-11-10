#!/usr/bin/env python3
# px_to_cm_numbers.py
# Rewrite numeric literals in an SVG from px to cm (1 px = 2.54/96 cm) WITHOUT applying transforms.
# Usage:
#   python px_to_cm_numbers.py in.svg out.svg [--dpi 96] [--no-stroke] [--no-size]
#
# Notes:
# - Edits numbers in-place in attributes (including <path d>), respecting SVG path syntax.
# - Arc commands (A/a): scales rx, ry, x, y; keeps rotation and flags unchanged.
# - Leaves any 'transform=' attributes exactly as they are.
# - By default, also converts width/height to 'cm' and viewBox numbers to cm.

import argparse, re, sys
import xml.etree.ElementTree as ET

# Robust float matcher per SVG grammar
NUM_RE = re.compile(r"""
    [+-]? (?: (?:\d+\.\d*) | (?:\.\d+) | (?:\d+) )
    (?: [eE] [+-]? \d+ )?
""", re.VERBOSE)

COMMANDS = set("MmZzLlHhVvCcSsQqTtAa")

def fnum(x: float) -> str:
    s = f"{x:.6f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s if s else "0"

def split_viewbox(vb: str):
    parts = re.split(r"[\s,]+", vb.strip())
    if len(parts) == 4:
        return [float(p) for p in parts]
    return None

def join_viewbox(nums):
    return " ".join(fnum(n) for n in nums)

def convert_viewbox(elem, k):
    vb = elem.get("viewBox")
    if not vb:
        return
    nums = split_viewbox(vb)
    if not nums:
        return
    elem.set("viewBox", join_viewbox([n * k for n in nums]))

def parse_len(s: str):
    if s is None:
        return None, None
    m = re.match(r"^\s*([+-]?(?:\d+(?:\.\d+)?|\.\d+))(?:\s*([a-z%]+))?\s*$", s)
    if not m:
        return None, None
    return float(m.group(1)), (m.group(2) or "")

def convert_size_attrs(elem, k, touch_size=True):
    if not touch_size:  # leave width/height unchanged
        return
    for attr in ("width", "height"):
        val, unit = parse_len(elem.get(attr))
        if val is not None:
            elem.set(attr, f"{fnum(val * k)}cm")

def scale_simple_attrs(el, attrs, k):
    for a in attrs:
        if a in el.attrib:
            try:
                el.set(a, fnum(float(el.get(a)) * k))
            except ValueError:
                pass

def scale_points(points: str, k: float) -> str:
    out = []
    i = 0
    while i < len(points):
        m = NUM_RE.match(points, i)
        if m:
            out.append(fnum(float(m.group()) * k))
            i = m.end()
            continue
        # copy separator char as-is
        out.append(points[i])
        i += 1
    return "".join(out)

def convert_path_d(d: str, k: float) -> str:
    """
    Rewrites numeric literals inside a path 'd' string by multiplying by k,
    with special handling for arc commands (A/a):
      per segment: rx, ry -> *k; rotation -> keep; flags (2) -> keep; x, y -> *k
    """
    out = []
    i = 0
    current_cmd = None
    # for commands with repeating parameter groups, track position in the current group's numbers
    group_pos = 0

    def reset_group():
        nonlocal group_pos
        group_pos = 0

    # group sizes and which indices to scale (per group) for each command
    GROUP_INFO = {
        'M': (2, [0,1]), 'm': (2, [0,1]),
        'L': (2, [0,1]), 'l': (2, [0,1]),
        'T': (2, [0,1]), 't': (2, [0,1]),
        'H': (1, [0]),   'h': (1, [0]),
        'V': (1, [0]),   'v': (1, [0]),
        'S': (4, [0,1,2,3]), 's': (4, [0,1,2,3]),
        'Q': (4, [0,1,2,3]), 'q': (4, [0,1,2,3]),
        'C': (6, [0,1,2,3,4,5]), 'c': (6, [0,1,2,3,4,5]),
        # For A/a: (rx, ry, rot, large, sweep, x, y) -> scale indices 0,1,5,6
        'A': (7, [0,1,5,6]), 'a': (7, [0,1,5,6]),
        'Z': (0, []), 'z': (0, []),
    }

    while i < len(d):
        ch = d[i]
        if ch in COMMANDS:
            current_cmd = ch
            out.append(ch)
            i += 1
            reset_group()
            continue
        m = NUM_RE.match(d, i)
        if m and current_cmd:
            num_txt = m.group()
            gi = GROUP_INFO[current_cmd]
            gsize, scale_indices = gi

            if gsize == 0:
                # Z/z has no numbers; should not come here, but copy as-is
                out.append(num_txt)
            else:
                # Determine index within the current group for this number
                idx_in_group = group_pos % gsize
                if current_cmd in ('A','a'):
                    # Arc: need to preserve rotation (index 2) and flags (3,4)
                    if idx_in_group in (0,1,5,6):
                        out.append(fnum(float(num_txt) * k))
                    else:
                        # rotation or flags -> keep
                        out.append(num_txt)
                else:
                    if idx_in_group in scale_indices:
                        out.append(fnum(float(num_txt) * k))
                    else:
                        out.append(num_txt)
                group_pos += 1
            i = m.end()
            continue
        # copy separators or unexpected chars verbatim
        out.append(ch)
        i += 1
    return "".join(out)

def process(svg_in, svg_out, dpi=96.0, scale_stroke=True, touch_size=True):
    k = 2.54 / float(dpi)  # px -> cm

    ET.register_namespace("", "http://www.w3.org/2000/svg")  # preserve default ns if present
    tree = ET.parse(svg_in)
    root = tree.getroot()

    # Update viewBox and width/height
    convert_viewbox(root, k)
    convert_size_attrs(root, k, touch_size=touch_size)

    for el in root.iter():
        tag = el.tag.split('}',1)[-1]  # localname

        if tag == 'path' and 'd' in el.attrib:
            el.set('d', convert_path_d(el.get('d'), k))
            if scale_stroke and 'stroke-width' in el.attrib:
                try:
                    el.set('stroke-width', fnum(float(el.get('stroke-width')) * k))
                except ValueError:
                    pass

        elif tag == 'circle':
            scale_simple_attrs(el, ['cx','cy','r'], k)
            if scale_stroke and 'stroke-width' in el.attrib:
                scale_simple_attrs(el, ['stroke-width'], k)

        elif tag == 'ellipse':
            scale_simple_attrs(el, ['cx','cy','rx','ry'], k)
            if scale_stroke and 'stroke-width' in el.attrib:
                scale_simple_attrs(el, ['stroke-width'], k)

        elif tag == 'rect':
            scale_simple_attrs(el, ['x','y','width','height','rx','ry'], k)
            if scale_stroke and 'stroke-width' in el.attrib:
                scale_simple_attrs(el, ['stroke-width'], k)

        elif tag == 'line':
            scale_simple_attrs(el, ['x1','y1','x2','y2'], k)
            if scale_stroke and 'stroke-width' in el.attrib:
                scale_simple_attrs(el, ['stroke-width'], k)

        elif tag in ('polyline','polygon') and 'points' in el.attrib:
            el.set('points', scale_points(el.get('points'), k))
            if scale_stroke and 'stroke-width' in el.attrib:
                scale_simple_attrs(el, ['stroke-width'], k)

        elif tag in ('text',):
            # Optional: shift-like attrs if present (rare)
            scale_simple_attrs(el, ['x','y','dx','dy'], k)

        # DO NOT touch 'transform' attributes by design.

    tree.write(svg_out, encoding='utf-8', xml_declaration=True)

def main():
    ap = argparse.ArgumentParser(description="Rewrite SVG numbers from px to cm (no transforms).")
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--dpi", type=float, default=96.0, help="CSS px DPI (default: 96)")
    ap.add_argument("--no-stroke", action="store_true", help="do NOT convert stroke-width values")
    ap.add_argument("--no-size", action="store_true", help="do NOT convert width/height to cm")
    args = ap.parse_args()
    process(args.input, args.output, dpi=args.dpi, scale_stroke=(not args.no_stroke), touch_size=(not args.no_size))

if __name__ == "__main__":
    main()
