window.onload = () => {
 get_geometry();
 var xy;
 if(wWidth > wHeight) {
  xy = wHeight; }
 else {
  xy = wWidth; }
 ['mecanism_container','clockface_container','hrs_container','mns_container'].forEach(e => {
  $_(e).style.width = xy + 'px';
  $_(e).style.height = xy + 'px';
  $_(e).style.left = (wWidth - xy) / 2 + 'px;'
  $_(e).style.top = (wHeight - xy) / 2 + 'px;' });
 face_switch_arg = 1;
 face_switch();
 const dial = window.document.createElement('img');
 dial.id = 'clock_dial';
 dial.src = './svg/dial.svg';
 $_('clockface_container').appendChild(dial);
 dial.onload = () => {
  var rect = dial.getBoundingClientRect();
  var dial_xy = rect.width;
  // console.log(`dial_xy: ${dial_xy}`);
  var hmd = (dial_xy * 77 / 100) + 'px'
  dial.style.width = hmd;
  mk_clickable_quarters(dial_xy);
  mk_clickable_reset(dial_xy * 155 / 100);
  getTimeNow();
  place_clock_hands();
  setInterval(() => {
   getTimeNow();
   place_clock_hands(); },10000);
  make_drivers(); }
 $_('docbody').onclick = () => {
  face_switch(); } }

getTimeNow = () => {
 var now = new Date();
 HH = now.getHours() % 12;
 MM = now.getMinutes();
 SS = now.getSeconds(); }

place_clock_hands = () => {
 console.log(`${String(HH).padStart(2, '0')}:${String(MM).padStart(2, '0')}:${String(SS).padStart(2, '0')}`);
 const mns_angle = MM * 6;
 $_('geneva_60').setAttribute('transform', `rotate(${mns_angle})`);
 $_('MNS').setAttribute('transform', `scale(27) rotate(${mns_angle + 180})`);
 const hrs_angle = (HH * 30) + (Math.floor((MM * 60 + SS + 450) / 900) * 7.5);
 $_('geneva_48').setAttribute('transform', `rotate(${hrs_angle})`);
 $_('HRS').setAttribute('transform', `scale(27) rotate(${hrs_angle + 180})`); }

mk_clickable_reset = (xy) => {
 var cq_m = window.document.createElement('div');
 cq_m.id = 'CQM';
 cq_m.className = 'cq_elem';
 cq_m.title = 'RESET';
 cq_m.style.width = xy / 2 + 'px';
 cq_m.style.height = xy / 2 + 'px';
 cq_m.style.left = (wWidth - xy / 2) / 2 + 'px';
 cq_m.style.top = (wHeight - xy / 2) / 2 + 'px';
 window.document.body.appendChild(cq_m);
 cq_m.onclick = e => {
  $_('clockface_container').style.visibility = 'visible';
  $_('hrs_container').style.visibility = 'visible';
  $_('mns_container').style.visibility = 'visible';
  change_view('svg_48',views['global']);
  change_view('svg_60',views['global']); }}

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
   face_switch_arg = 0;
   face_switch(face_switch_arg);
   $_('clockface_container').style.visibility = 'hidden';
   $_('hrs_container').style.visibility = 'hidden';
   $_('mns_container').style.visibility = 'hidden';
   change_view('svg_48',views['hrs_driver_1']);
   change_view('svg_60',views['mins_driver_0']); }
 cq_1.onclick = () => {
   face_switch_arg = 0;
   face_switch(face_switch_arg);
   $_('clockface_container').style.visibility = 'hidden';
   $_('hrs_container').style.visibility = 'hidden';
   $_('mns_container').style.visibility = 'hidden';
   change_view('svg_48',views['hrs_driver_0']);
   change_view('svg_60',views['mins_driver_1']); }
 cq_2.onclick = () => {
   face_switch_arg = 1;
   face_switch(face_switch_arg);
   $_('clockface_container').style.visibility = 'hidden';
   $_('hrs_container').style.visibility = 'hidden';
   $_('mns_container').style.visibility = 'hidden';
   change_view('svg_48',views['hrs_driver_0']);
   change_view('svg_60',views['mins_driver_1']); }
 cq_3.onclick = () => {
   face_switch_arg = 1;
   face_switch(face_switch_arg);
   $_('clockface_container').style.visibility = 'hidden';
   $_('hrs_container').style.visibility = 'hidden';
   $_('mns_container').style.visibility = 'hidden';
   change_view('svg_48',views['hrs_driver_1']);
   change_view('svg_60',views['mins_driver_0']); }}

face_switch = () => {
 // if($_('clockface_container').style.visibility == 'hidden') return;
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
