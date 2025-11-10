#!/usr/bin/python

# svg_px_2_cm.py input.svg output.svg

import sys
import re
import xml.etree.ElementTree as ET

PX_TO_CM = 0.02645833
SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"
NSMAP = {"svg": SVG_NS, "xlink": XLINK_NS}
for pfx, uri in NSMAP.items():
  ET.register_namespace(pfx if pfx != "svg" else "", uri)

def parse_len(val):
 # Return (number, unit) for a length string like '800px' or '800'
 if val is None:
  return None, None
 m = re.fullmatch(r"\s*([+-]?\d+(?:\.\d+)?)\s*([a-z%]*)\s*", val)
 if not m:
  return None, None
 num = float(m.group(1))
 unit = m.group(2)  # '' means unitless
 return num, unit

def fmt_cm(x):
 return f"{x:.6f}cm"

def convert_root_size(root):
 # width / height: treat unitless as px by convention
 for attr in ("width", "height"):
  v = root.get(attr)
  if not v:
   continue
  num, unit = parse_len(v)
  if num is None:
   continue
  if unit in ("", "px"):  # px or unitless ⇒ convert
   root.set(attr, fmt_cm(num * PX_TO_CM))
  elif unit in ("cm", "mm", "in", "pt", "pc"):  # leave other absolute units alone
   pass
  else:
   # if it is something odd (e.g., %), leave as-is
   pass

def convert_viewbox(root):
 vb = root.get("viewBox")
 if not vb:
  # Try to synthesize viewBox from width/height if both are numeric-or-px
  w, wu = parse_len(root.get("width"))
  h, hu = parse_len(root.get("height"))
  if w is not None and h is not None and (wu in ("", "px", "cm") and hu in ("", "px", "cm")):
    # If width/height were already converted to cm above, we need the px versions.
    # We can approximate by dividing back if unit is cm.
    if wu == "cm":
     w_px = w / PX_TO_CM
    else:
     w_px = w
    if hu == "cm":
     h_px = h / PX_TO_CM
    else:
     h_px = h
    vb = f"0 0 {w_px} {h_px}"
    root.set("viewBox", vb)
  else:
   return PX_TO_CM  # still return scale for wrapping
 # Scale the four viewBox numbers from px to cm
 parts = re.split(r"[\s,]+", vb.strip())
 if len(parts) != 4:
  return PX_TO_CM
 try:
  nums = [float(x) for x in parts]
 except ValueError:
  return PX_TO_CM
 nums_cm = [n * PX_TO_CM for n in nums]
 root.set("viewBox", " ".join(f"{n:.6f}" for n in nums_cm))
 return PX_TO_CM

def wrap_children_in_scale_group(root, scale):
 # Create <g transform="scale(scale)">
 g = ET.Element(f"{{{SVG_NS}}}g")
 g.set("transform", f"scale({scale:.8f})")
 # Move all existing children into g (preserve order)
 children = list(root)
 for ch in children:
  root.remove(ch)
  g.append(ch)
 root.append(g)

def main():
 if len(sys.argv) != 3:
  print(f'USAGE: /usr/bin/python3 {sys.argv[0]} input.svg output.svg')
  sys.exit(1)
 inp, outp = sys.argv[1], sys.argv[2]
 tree = ET.parse(inp)
 root = tree.getroot()
 # convert width/height
 convert_root_size(root)
 # convert viewBox values (numbers) from px→cm
 scale = convert_viewbox(root)
 # to preserve appearance, scale all original content by the same factor
 wrap_children_in_scale_group(root, scale)
 tree.write(outp, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
 main()
