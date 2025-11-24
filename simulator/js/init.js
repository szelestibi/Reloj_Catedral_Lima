window.onload = () => {
 var ST = getParamVal('ST'); // start time on software clock
 var CT = getParamVal('CT'); // start time on clockwork
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
 ['mechanism_container','clockface_container','seconds_container','marker_container','autoset_container','index_container','hrs_container','mns_container'].forEach(e => {
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
  // $_('help_page').style.width = dial_xy + 'px';
  // $_('help_page').style.height = dial_xy + 'px';
  mk_clickable_quarters(dial_xy);
  mk_clickable_reset(dial_xy * 155 / 100);
  make_drivers();
  if((ST != '') && (Number.isNaN(ST-0) === false)) {
   CW.realtime = false;
   if(ST.length > 5) {
    var hh = ST.substring(0,2) - 0;
    var mm = ST.substring(2,4) - 0;
    var ss = ST.substring(4,6) - 0; }
   else if(ST.length > 3) {
    var hh = ST.substring(0,2) - 0;
    var mm = ST.substring(2,4) - 0;
    var ss = 0; }
   else if(ST.length > 1) {
    var hh = ST.substring(0,2) - 0;
    var mm = 0;
    var ss = 0; }
   CW.init(hh,mm,ss); }
  else {
   CW.init(); }
  CW.face_switch(1); // 0 = HRS | 1 = MNS
  if((CT != '') && (Number.isNaN(CT-0) === false)) {
   if(CT.length > 5) {
    var hh = CT.substring(0,2) - 0;
    var mm = CT.substring(2,4) - 0;
    var ss = CT.substring(4,6) - 0; }
   else if(CT.length > 3) {
    var hh = CT.substring(0,2) - 0;
    var mm = CT.substring(2,4) - 0;
    var ss = 0; }
   else if(CT.length > 1) {
    var hh = CT.substring(0,2) - 0;
    var mm = 0;
    var ss = 0; }}
  else {
   var hh = CW.time.getHours();
   var mm = CW.time.getMinutes();
   var ss = CW.time.getSeconds(); }
  W48.setTime(hh,mm,ss);
  W60.setTime(hh,mm,ss); W48.normalize();
  CW.start(); }
 $_('docbody').onclick = () => {
  CW.face_switch(); }

 window.document.onkeydown = function(k) {
  if(k.key == 'ArrowUp') {         // MEC: HRS+15MNS
   if((D_MNS.rotating == false) && (D_HRS.rotating == false)) {
    W48.inc_MM_15();
    display_clock(); }}
  else if(k.key == 'ArrowDown') {  // MEC: HRS-15MNS
   if((D_MNS.rotating == false) && (D_HRS.rotating == false)) {
    W48.dec_MM_15();
    display_clock(); }}
  else if(k.key == 'ArrowLeft') {  // MEC: MNS--
   if((D_MNS.rotating == false) && (D_HRS.rotating == false)) {
    W60.dec_MM();
    display_clock(); }}
  else if(k.key == 'ArrowRight') { // MEC: MNS++
   if((D_MNS.rotating == false) && (D_HRS.rotating == false)) {
    W60.inc_MM();
    display_clock(); }}
  else if(k.key == 'Enter') {
   W60.move();
   W48.move(); }
  else if(k.key == 'Escape') {
   if($_('help_page').style.visibility == 'visible') {
    $_('help_page').style.visibility = 'hidden'; }
   else {
    if(CW.running == false) {
     CW.realtime = false; $_('SECS').setAttribute('class','secs');
     CW.start(); }}}
  else if(k.key == ' ') {
   CW.face_switch(); }
  else if(k.key == 'Tab') {
   k.preventDefault();
   k.stopPropagation();
   CW.stop();
   if((CW.enter_mode += 1) == 3) { // 0 = time | 1 = MNS | 2 = HRS
    CW.enter_mode = 0; }
   if(CW.enter_mode == 0) {
    $_('hand_hrs').setAttribute('class','hand');
    $_('hand_mns').setAttribute('class','hand');
    $_('seconds_container').style.visibility = 'visible'; }
   else if(CW.enter_mode == 1) {
    $_('hand_hrs').setAttribute('class','hand');
    $_('hand_mns').setAttribute('class','hand_selected');
    $_('seconds_container').style.visibility = 'hidden'; }
   else if(CW.enter_mode == 2) {
    $_('hand_hrs').setAttribute('class','hand_selected');
    $_('hand_mns').setAttribute('class','hand');
    $_('seconds_container').style.visibility = 'hidden'; }
   display_clock(); }
  else if(k.key == 'Insert') {
   CW.stop();
   if(CW.enter_mode == 0) {       // time
    CW.set_HH(+1); }
   else if(CW.enter_mode == 1) {  // MNS
    W60.inc_HH(); }
   else if(CW.enter_mode == 2) {  // HRS
    W48.inc_HH(); }
   display_clock(); }
  else if(k.key == 'Delete') {
   CW.stop();
   if(CW.enter_mode == 0) {       // time
    CW.set_HH(-1); }
   else if(CW.enter_mode == 1) {  // MNS
    W60.dec_HH(); }
   else if(CW.enter_mode == 2) {  // HRS
    W48.dec_HH(); }
   display_clock(); }
  else if(k.key == 'Home') {
   CW.stop();
   if(CW.enter_mode == 0) {
    CW.set_MM(+1); }
   else if(CW.enter_mode == 1) {
    W60.inc_MM(); }
   else if(CW.enter_mode == 2) {
    W48.inc_MM(); }
   display_clock(); }
  else if(k.key == 'End') {
   CW.stop();
   if(CW.enter_mode == 0) {
    CW.set_MM(-1); }
   else if(CW.enter_mode == 1) {
    W60.dec_MM(); }
   else if(CW.enter_mode == 2) {
    W48.dec_MM(); }
   display_clock(); }
  else if(k.key == 'PageUp') {
   CW.stop();
   if(CW.enter_mode == 0) {
    CW.set_SS(+1); }
   else if(CW.enter_mode == 1) {
    W60.inc_SS(); }
   else if(CW.enter_mode == 2) {
    W48.inc_SS(); }
   display_clock(); }
  else if(k.key == 'PageDown') {
   CW.stop();
   if(CW.enter_mode == 0) {
    CW.set_SS(-1); }
   else if(CW.enter_mode == 1) {
    W60.dec_SS(); }
   else if(CW.enter_mode == 2) {
    W48.dec_SS(); }
   display_clock(); }
  else if(k.key == 's') {
   CW.stop();
   CW.time.setSeconds(0);
   display_clock(); }
  else if(k.key == 'S') {
   CW.stop();
   CW.time.setSeconds(0);
   display_clock(); }
  else if(k.key == 'r') {
   if(CW.realtime == true) {}
   else {
    if(CW.running) CW.stop;
    CW.realtime = true; $_('SECS').setAttribute('class','secs_rt');
    CW.start(); }}
  else if(k.key == 'R') {
   if(CW.realtime == true) {}
   else {
    if(CW.running) CW.stop;
    CW.realtime = true; $_('SECS').setAttribute('class','secs_rt');
    CW.start(); }}
  else if(k.key == '0') {
   if((D_MNS.rotating == false) && (D_HRS.rotating == false)) {
    W48.setTime(0,0,0);
    W60.setTime(0,0,0);
    display_clock(); }}
  else if(k.key == '1') {
   if((D_MNS.rotating == false) && (D_HRS.rotating == false)) {
    W48.setTime(1,0,0);
    W60.setTime(1,0,0);
    display_clock(); }}
  else if(k.key == '2') {
   if((D_MNS.rotating == false) && (D_HRS.rotating == false)) {
    W48.setTime(2,0,0);
    W60.setTime(2,0,0);
    display_clock(); }}
  else if(k.key == '3') {
   if((D_MNS.rotating == false) && (D_HRS.rotating == false)) {
    W48.setTime(3,0,0);
    W60.setTime(3,0,0);
    display_clock(); }}
  else if(k.key == '4') {
   if((D_MNS.rotating == false) && (D_HRS.rotating == false)) {
    W48.setTime(4,0,0);
    W60.setTime(4,0,0);
    display_clock(); }}
  else if(k.key == '5') {
   if((D_MNS.rotating == false) && (D_HRS.rotating == false)) {
    W48.setTime(5,0,0);
    W60.setTime(5,0,0);
    display_clock(); }}
  else if(k.key == '6') {
   if((D_MNS.rotating == false) && (D_HRS.rotating == false)) {
    W48.setTime(6,0,0);
    W60.setTime(6,0,0);
    display_clock(); }}
  else if(k.key == '7') {
   if((D_MNS.rotating == false) && (D_HRS.rotating == false)) {
    W48.setTime(7,0,0);
    W60.setTime(7,0,0);
    display_clock(); }}
  else if(k.key == '8') {
   if((D_MNS.rotating == false) && (D_HRS.rotating == false)) {
    W48.setTime(8,0,0);
    W60.setTime(8,0,0);
    display_clock(); }}
  else if(k.key == '9') {
   if((D_MNS.rotating == false) && (D_HRS.rotating == false)) {
    W48.setTime(9,0,0);
    W60.setTime(9,0,0);
    display_clock(); }}
  else if(k.key == 'A') {
   if((D_MNS.rotating == false) && (D_HRS.rotating == false)) {
    W48.setTime(10,0,0);
    W60.setTime(10,0,0);
    display_clock(); }}
  else if(k.key == 'B') {
   if((D_MNS.rotating == false) && (D_HRS.rotating == false)) {
    W48.setTime(11,0,0);
    W60.setTime(11,0,0);
    display_clock(); }}
  else if(k.key == 'a') {
   if((D_MNS.rotating == false) && (D_HRS.rotating == false)) {
    W48.setTime(10,0,0);
    W60.setTime(10,0,0);
    display_clock(); }}
  else if(k.key == 'b') {
   if((D_MNS.rotating == false) && (D_HRS.rotating == false)) {
    W48.setTime(11,0,0);
    W60.setTime(11,0,0);
    display_clock(); }}
  else if(k.key == 'F1') {
   k.preventDefault();
   k.stopPropagation();
   $_('help_page').style.visibility = 'visible'; }
  else {
   console.log(k.key); }}} // ONLOAD END

display_clock = () => {
 var show_aux = 1;
 var ss, mm, hh;
 if(CW.enter_mode == 0) {
  ss = CW.time.getSeconds();
  mm = CW.time.getMinutes();
  hh = CW.time.getHours();
  const secs_angle = ss * 6;
  $_('SECS').setAttribute('transform', `rotate(${secs_angle + 180})`); }
 else if(CW.enter_mode == 1) {
  ss = 'XX';
  mm = W60.MM;
  hh = 'XX'; }
 else if(CW.enter_mode == 2) {
  ss = W48.SS;
  mm = W48.MM;
  hh = W48.HH; }
 W60.place_svg_elems();
 W48.place_svg_elems();
 $_('TIME').innerHTML = `${String(hh).padStart(2,'0')}:${String(mm).padStart(2,'0')}:${String(ss).padStart(2,'0')}`;
 if(show_aux == 1) {
  ss_48 = W48.SS;
  mm_48 = W48.MM;
  hh_48 = W48.HH;
  ss_60 = 'XX';
  mm_60 = W60.MM;
  hh_60 = 'XX';
  /* debug(`${String(hh_48).padStart(2,'0')}:${String(mm_48).padStart(2,'0')}:${String(ss_48).padStart(2,'0')} • ${String(hh_60).padStart(2,'0')}:${String(mm_60).padStart(2,'0')}:${String(ss_60).padStart(2,'0')}`); */ }}

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
 cq_m.title = 'CENTER';
 cq_m.style.width = xy / 2 + 'px';
 cq_m.style.height = xy / 2 + 'px';
 cq_m.style.left = (wWidth - xy / 2) / 2 + 'px';
 cq_m.style.top = (wHeight - xy / 2) / 2 + 'px';
 window.document.body.appendChild(cq_m);
 cq_m.onclick = e => {
  $_('clockface_container').style.visibility = 'visible';
  $_('marker_container').style.visibility = 'visible';
  $_('index_container').style.visibility = 'visible';
  if(CW.running == true) {
   $_('autoset_container').style.visibility = 'visible'; }
  $_('seconds_container').style.visibility = 'visible';
  $_('hrs_container').style.visibility = 'visible';
  $_('mns_container').style.visibility = 'visible';
  change_view('svg_48',views['global']);
  change_view('svg_60',views['global']); }}

mk_clickable_quarters = (xy) => {
 var cq_1 = window.document.createElement('div');
 cq_1.id = 'CQ1';
 cq_1.className = 'cq_elem';
 cq_1.title = 'ZOOM';
 cq_1.style.width = xy / 2 + 'px';
 cq_1.style.height = xy / 2 + 'px';
 cq_1.style.left = (wWidth / 2) + 'px';
 cq_1.style.top = (wHeight / 2) + 'px';
 window.document.body.appendChild(cq_1);
 var cq_2 = window.document.createElement('div');
 cq_2.id = 'CQ2';
 cq_2.className = 'cq_elem';
 cq_2.title = 'ZOOM';
 cq_2.style.width = xy / 2 + 'px';
 cq_2.style.height = xy / 2 + 'px';
 cq_2.style.left = (wWidth - xy) / 2 + 'px';
 cq_2.style.top = (wHeight / 2) + 'px';
 window.document.body.appendChild(cq_2);
 cq_1.onclick = () => {
   CW.face_switch(1);
   $_('clockface_container').style.visibility = 'hidden';
   $_('marker_container').style.visibility = 'hidden';
   $_('index_container').style.visibility = 'hidden';
   $_('autoset_container').style.visibility = 'hidden';
   $_('seconds_container').style.visibility = 'hidden';
   $_('hrs_container').style.visibility = 'hidden';
   $_('mns_container').style.visibility = 'hidden';
   change_view('svg_48',views['hrs_driver_0']);
   change_view('svg_60',views['mins_driver_1']); }
 cq_2.onclick = () => {
   CW.face_switch(0);
   $_('clockface_container').style.visibility = 'hidden';
   $_('marker_container').style.visibility = 'hidden';
   $_('index_container').style.visibility = 'hidden';
   $_('autoset_container').style.visibility = 'hidden';
   $_('seconds_container').style.visibility = 'hidden';
   $_('hrs_container').style.visibility = 'hidden';
   $_('mns_container').style.visibility = 'hidden';
   change_view('svg_48',views['hrs_driver_0']);
   change_view('svg_60',views['mins_driver_1']); }}

debug = s => {
 $_('DBG').style.visibility = 'visible';
 $_('DBG').innerHTML = s; }
