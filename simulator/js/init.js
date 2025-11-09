window.onload = () => {
 get_geometry();
 face_switch_arg = 1;
 face_switch();
 dial = window.document.createElement('img');
 dial.id = 'clock_dial';
 dial.src = './svg/dial.svg';
 $_('clockface_container').appendChild(dial);
 dial.onload = () => {
  var rect = dial.getBoundingClientRect();
  var dial_xy = rect.width;
  // console.log(`dial_xy: ${dial_xy}`);
  dial.style.width = (dial_xy * 77 / 100) + 'px';
  mk_clickable_quarters(dial_xy);
  mk_clickable_menu(dial_xy);
  var now = new Date();
  HH = now.getHours() % 12;
  MM = now.getMinutes();
  SS = now.getSeconds();
  place_clock_hands(); }
 $_('clockface_container').onclick = () => {
  face_switch(); }
 /* */ }

place_clock_hands = () => {
 $_('geneva_60').setAttribute('transform', `rotate(${MM * 6})`);
 // MM = 7; SS = 30;
 var angle = Math.floor((MM * 60 + SS + 450) / 900) * 7.5;
 console.log(angle);
 $_('geneva_48').setAttribute('transform', `rotate(${(HH * 30) + (Math.floor((MM * 60 + SS + 450) / 900) * 7.5) })`); }

mk_clickable_menu = (xy) => {
 var cq_m = window.document.createElement('div');
 cq_m.id = 'CQM';
 cq_m.className = 'cq_elem';
 cq_m.title = 'MENU';
 cq_m.style.width = xy / 3 + 'px';
 cq_m.style.height = xy / 3 + 'px';
 cq_m.style.left = (wWidth - xy / 3) / 2 + 'px';
 cq_m.style.top = (wHeight - xy / 3) / 2 + 'px';
 window.document.body.appendChild(cq_m);
 cq_m.onclick = e => {}}

mk_clickable_quarters = (xy) => {
 var cq_0 = window.document.createElement('div');
 cq_0.id = 'CQ0';
 cq_0.className = 'cq_elem';
 cq_0.title = 'MNS_0';
 cq_0.style.width = xy / 2 + 'px';
 cq_0.style.height = xy / 2 + 'px';
 cq_0.style.left = (wWidth / 2) + 'px';
 cq_0.style.top = (wHeight - xy) / 2 + 'px';
 window.document.body.appendChild(cq_0);
 var cq_1 = window.document.createElement('div');
 cq_1.id = 'CQ1';
 cq_1.className = 'cq_elem';
 cq_1.title = 'MNS_1';
 cq_1.style.width = xy / 2 + 'px';
 cq_1.style.height = xy / 2 + 'px';
 cq_1.style.left = (wWidth / 2) + 'px';
 cq_1.style.top = (wHeight / 2) + 'px';
 window.document.body.appendChild(cq_1);
 var cq_2 = window.document.createElement('div');
 cq_2.id = 'CQ2';
 cq_2.className = 'cq_elem';
 cq_2.title = 'HRS_0';
 cq_2.style.width = xy / 2 + 'px';
 cq_2.style.height = xy / 2 + 'px';
 cq_2.style.left = (wWidth - xy) / 2 + 'px';
 cq_2.style.top = (wHeight / 2) + 'px';
 window.document.body.appendChild(cq_2);
 var cq_3 = window.document.createElement('div');
 cq_3.id = 'CQ3';
 cq_3.className = 'cq_elem';
 cq_3.title = 'HRS_1';
 cq_3.style.width = xy / 2 + 'px';
 cq_3.style.height = xy / 2 + 'px';
 cq_3.style.left = (wWidth - xy) / 2 + 'px';
 cq_3.style.top = (wHeight - xy) / 2 + 'px';
 window.document.body.appendChild(cq_3);
 cq_0.onclick = () => {
  if(zoomed == 0) {
   face_switch_arg = 0;
   face_switch(face_switch_arg);
   zoomed = 1;
   $_('clock_dial').style.visibility = 'hidden';
   change_view('svg_60',views['mins_driver_0']); }
  else {
   zoomed = 0;
   $_('clock_dial').style.visibility = 'visible';
   change_view('svg_48',views['global']);
   change_view('svg_60',views['global']); } }
 cq_1.onclick = () => {
  if(zoomed == 0) {
   face_switch_arg = 0;
   face_switch(face_switch_arg);
   zoomed = 1;
   $_('clock_dial').style.visibility = 'hidden';
   change_view('svg_60',views['mins_driver_1']); }
  else {
   zoomed = 0;
   $_('clock_dial').style.visibility = 'visible';
   change_view('svg_48',views['global']);
   change_view('svg_60',views['global']); } }
 cq_2.onclick = () => {
  if(zoomed == 0) {
   face_switch_arg = 1;
   face_switch(face_switch_arg);
   zoomed = 1;
   $_('clock_dial').style.visibility = 'hidden';
   change_view('svg_48',views['hrs_driver_0']); }
  else {
   zoomed = 0;
   $_('clock_dial').style.visibility = 'visible';
   change_view('svg_48',views['global']);
   change_view('svg_60',views['global']); } }
 cq_3.onclick = () => {
  if(zoomed == 0) {
   face_switch_arg = 1;
   face_switch(face_switch_arg);
   zoomed = 1;
   $_('clock_dial').style.visibility = 'hidden';
   change_view('svg_48',views['hrs_driver_1']); }
  else {
   zoomed = 0;
   $_('clock_dial').style.visibility = 'visible';
   change_view('svg_48',views['global']);
   change_view('svg_60',views['global']); }}}

face_switch = () => {
 if(zoomed == 1) {
  $_('clock_dial').style.visibility = 'visible';
  change_view('svg_48',views['global']);
  change_view('svg_60',views['global']);
  zoomed = 0;
  return; }
 if(face_switch_arg == 0) {
  $_('svg_48').style.display = 'none';
  $_('svg_60').style.display = 'block';
  face_switch_arg = 1; }
 else {
  $_('svg_60').style.display = 'none';
  $_('svg_48').style.display = 'block';
  face_switch_arg = 0; }}

change_view = (s,[w,h,x,y]) => {
 if(typeof(s) == 'string') {
  s = $_(s); }
 s.viewBox.baseVal.x = x;
 s.viewBox.baseVal.y = y;
 s.viewBox.baseVal.width = w;
 s.viewBox.baseVal.height = h; }
