window.onload = () => {
 get_geometry();
 var xy;
 if(wWidth > wHeight) {
  xy = wHeight; }
 else {
  xy = wWidth; }
 var digital_clock = window.document.createElement('div');
 digital_clock.id = 'TIME';
 window.document.body.appendChild(digital_clock);
 var debug = window.document.createElement('div');
 debug.id = 'DBG';
 window.document.body.appendChild(debug);
 $_('DBG').style.visibility = 'hidden';
 ['mechanism_container','clockface_container','seconds_container','marker_container','hrs_container','mns_container'].forEach(e => {
  $_(e).style.width = xy + 'px';
  $_(e).style.height = xy + 'px';
  $_(e).style.left = (wWidth - xy) / 2 + 'px;'
  $_(e).style.top = (wHeight - xy) / 2 + 'px;' });
 const dial = window.document.createElement('img');
 dial.id = 'clock_dial';
 dial.src = './svg/dial.svg';
 $_('clockface_container').appendChild(dial);
 dial.onload = () => {
  CW = clockwork.CW;
  var rect = dial.getBoundingClientRect();
  var dial_xy = rect.width;
  var hmd = (dial_xy * 77 / 100) + 'px'
  dial.style.width = hmd;
  dial.style.height = hmd;
  mk_clickable_quarters(dial_xy);
  mk_clickable_reset(dial_xy * 155 / 100);
  make_drivers();
  CW.init();
  CW.face_switch(0); // 0 = MNS | 1 = HRS
  CW.start(); }
 $_('docbody').onclick = () => {
  CW.face_switch(); }

 window.document.onkeydown = function(k) {
  if(k.key == 'ArrowUp') {         // HRS/10MNS++
   if(CW.shown_face == 0) {
    CW.stop();
    CW.set_HH(+1); }
   else if(CW.shown_face == 1) {
    CW.stop();
    CW.set_MM(+10); }}
  else if(k.key == 'ArrowDown') {  // HRS/10MNS--
   if(CW.shown_face == 0) {
    CW.stop();
    CW.set_HH(-1); }
   else if(CW.shown_face == 1) {
    CW.stop();
    CW.set_MM(-10); }}
  else if(k.key == 'ArrowLeft') {  // ¼HRS/MNS--
   if(CW.shown_face == 0) {
    CW.stop();
    CW.set_MM(-15); }
   else if(CW.shown_face == 1) {
    CW.stop();
    CW.set_MM(-1); }}
  else if(k.key == 'ArrowRight') { // ¼HRS/MNS++
   if(CW.shown_face == 0) {
    CW.stop();
    CW.set_MM(+15); }
   else if(CW.shown_face == 1) {
    CW.stop();
    CW.set_MM(+1); }}
  else if(k.key == 'Enter') {
   CW.stop();
   realtime = true;
   CW.init();
   CW.show_face_();
   CW.showTime_();
   CW.start(); }
  else if(k.key == 'Escape') {
   if(CW.running == false) {
    realtime = false;
    CW.start(); }}
  else if(k.key == ' ') {
   CW.face_switch(); }
  else if(k.key == 'Tab') {
   k.preventDefault();
   k.stopPropagation();
   CW.face_switch(); }
  else if(k.key == 'Insert') {
   CW.stop();
   CW.set_HH(+1); }
  else if(k.key == 'Delete') {
   CW.stop();
   CW.set_HH(-1); }
  else if(k.key == 'Home') {
   CW.stop();
   CW.set_MM(+1); }
  else if(k.key == 'End') {
   CW.stop();
   CW.set_MM(-1); }
  else if(k.key == 'PageUp') {
   CW.stop();
   CW.set_SS(+1); }
  else if(k.key == 'PageDown') {
   CW.stop();
   CW.set_SS(-1); }
  else if(k.key == 'm') {
   CW.move(); }
  else if(k.key == 'M') {
   CW.move(); }
  else {
   console.log(k.key); }}}

show_ttime = () => {
 $_('TC').innerHTML = `${String(HH).padStart(2,'0')}:${String(MM).padStart(2,'0')}:${String(SS).padStart(2,'0')}`; }

change_view = (s,[w,h,x,y]) => {
 if(typeof(s) == 'string') {
  s = $_(s); }
 s.viewBox.baseVal.x = x;
 s.viewBox.baseVal.y = y;
 s.viewBox.baseVal.width = w;
 s.viewBox.baseVal.height = h; }

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
  $_('marker_container').style.visibility = 'visible';
  $_('seconds_container').style.visibility = 'visible';
  $_('hrs_container').style.visibility = 'visible';
  $_('mns_container').style.visibility = 'visible';
  change_view('svg_48',views['global']);
  change_view('svg_60',views['global']); }}

mk_clickable_quarters = (xy) => {
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
 cq_1.onclick = () => {
   CW.face_switch(0);
   $_('clockface_container').style.visibility = 'hidden';
   $_('marker_container').style.visibility = 'hidden';
   $_('seconds_container').style.visibility = 'hidden';
   $_('hrs_container').style.visibility = 'hidden';
   $_('mns_container').style.visibility = 'hidden';
   change_view('svg_48',views['hrs_driver_0']);
   change_view('svg_60',views['mins_driver_1']); }
 cq_2.onclick = () => {
   CW.face_switch(1);
   $_('clockface_container').style.visibility = 'hidden';
   $_('marker_container').style.visibility = 'hidden';
   $_('seconds_container').style.visibility = 'hidden';
   $_('hrs_container').style.visibility = 'hidden';
   $_('mns_container').style.visibility = 'hidden';
   change_view('svg_48',views['hrs_driver_0']);
   change_view('svg_60',views['mins_driver_1']); }}

debug = s => {
 $_('DBG').style.visibility = 'visible';
 $_('DBG').innerHTML = s; }
