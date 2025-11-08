#!/usr/bin/python

# 130 x 130 cm SVG grid centered at [0,0]
# - grid every 1 cm
# - axes (0,0) thick red
# - every 10 cm thin red
# - all other lines blue
# - labels every 10 cm

import svgwrite

def make_grid_svg(filename='./grid.svg'):
 size_cm = 130
 margin_cm = 3
 half = size_cm // 2
 outer_half = half + margin_cm  # includes margin

 # stroke widths (in cm)
 w_blue = .0026      # regular grid
 w_red_thin = .0026  # every 10 cm
 w_red_thick = .0052 # main axes

 # labels
 text_color = 'rgb(255,0,0)'

 # drawing with viewBox centered at 0,0
 dwg = svgwrite.Drawing(
  filename,
  size=(f"{size_cm + margin_cm * 2}cm", f"{size_cm + margin_cm * 2}cm"),
  viewBox=f"{-outer_half} {-outer_half} {size_cm + margin_cm * 2} {size_cm + margin_cm * 2}" )

 # background
 dwg.add(dwg.rect(
  insert=(-(half + margin_cm), -(half + margin_cm)),
  size=(size_cm + margin_cm * 2, size_cm + margin_cm * 2),
  fill="white" ))

 # flip Y so +Y points up for geometry
 scene = dwg.g(id='scene', transform='scale(1,-1)')
 dwg.add(scene)

 # grid lines (skip axes, draw them later)
 for i in range(-half, half + 1):
  if i == 0:
   continue
  color = 'rgb(255,0,0)' if (i % 10 == 0) else 'rgb(0,0,255)'
  width = w_red_thin if (i % 10 == 0) else w_blue
  # vertical x = i
  scene.add(dwg.line(
   start=(i, -half), end=(i, half),
   stroke=color, stroke_opacity=.5, stroke_width=f'{width}cm' ))
  # horizontal y = i
  scene.add(dwg.line(
   start=(-half, i), end=(half, i),
   stroke=color, stroke_opacity=.5, stroke_width=f'{width}cm' ))

 # main axes (thick red)
 scene.add(dwg.line(
  start=(0, -half), end=(0, half),
  stroke='red', stroke_opacity=.5, stroke_width=f'{w_red_thick}cm' ))
 scene.add(dwg.line(
  start=(-half, 0), end=(half, 0),
  stroke='red', stroke_opacity=.5, stroke_width=f'{w_red_thick}cm' ))

 # labels: add in a sub-group that cancels the flip so text is upright
 labels = dwg.g(id='labels', transform='scale(1,-1)')
 scene.add(labels)
 font_size = '.05cm'

 # Helper: place symmetric signed labels every 10 cm FROM AXES
 # X labels go on top & bottom margins at x = ±(10, 20, ..., 60)
 # Y labels go on left & right margins at y = ±(10, 20, ..., 60)
 step = 10
 max_step = half // step  # 6

 # X-axis distances
 for k in range(1, max_step + 1):
  pos = k * step
  s_pos = f"{pos:+d}"   # +10, +20, ...
  s_neg = f"{-pos:+d}"  # -10, -20, ...

  # bottom margin (y = -half - 0.5) and top margin (y = +half + 0.5)
  y_bottom = -(half + 1)
  y_top = (half + 2)

  # at +pos
  labels.add(dwg.text(
   s_pos, insert=(pos, y_bottom), font_size=font_size, fill=text_color, text_anchor="middle" ))
  labels.add(dwg.text(
   s_pos, insert=(pos, y_top), font_size=font_size, fill=text_color, text_anchor="middle" ))

  # at -pos
  labels.add(dwg.text(
   s_neg, insert=(-pos, y_bottom), font_size=font_size, fill=text_color, text_anchor="middle" ))
  labels.add(dwg.text(
   s_neg, insert=(-pos, y_top), font_size=font_size, fill=text_color, text_anchor="middle" ))

 # Y-axis distances
 for k in range(1, max_step + 1):
  pos = k * step
  s_pos = f"{pos:+d}"
  s_neg = f"{-pos:+d}"

  # left & right margins (x = ±(half + 0.5))
  x_left = -(half + 1.5)
  x_right = (half + 1.5)

  # at +pos
  labels.add(dwg.text(
   s_pos, insert=(x_left, pos), font_size=font_size, fill=text_color, text_anchor="middle", dominant_baseline="central" ))
  labels.add(dwg.text(
   s_pos, insert=(x_right, pos), font_size=font_size, fill=text_color, text_anchor="middle", dominant_baseline="central" ))

  # at -pos
  labels.add(dwg.text(
   s_neg, insert=(x_left, -pos), font_size=font_size, fill=text_color, text_anchor="middle", dominant_baseline="central" ))
  labels.add(dwg.text(
   s_neg, insert=(x_right, -pos), font_size=font_size, fill=text_color, text_anchor="middle", dominant_baseline="central" ))

 # origin label at a tiny offset inside the grid (optional)
 # labels.add(dwg.text(
 #  "0", insert=(1, 1), font_size=font_size, fill=text_color, text_anchor="start" ))

 dwg.save()
 print(f'Saved: {filename}')

if __name__ == '__main__':
 make_grid_svg()
