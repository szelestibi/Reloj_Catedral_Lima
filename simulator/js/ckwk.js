class Wheel {
 constructor(wheel) {
  this.name = wheel['name'];
  this.driven = wheel['svg'][0];
  this.hand = wheel['svg'][1];
  this.step = wheels[wheel['step']]['wheel_angle_step'];
  this.HH = wheel['HH'];
  this.MM = wheel['MM'];
  this.SS = wheel['SS'];
  this.angle = undefined;
  this.marker_angle = undefined;
  this.time_um = new Date();
  this.place_svg_elems(); }
 calc_angle = () => {
  if(this.name == 'W60') {
   this.angle = this.MM * this.step; }
  else if(this.name == 'W48') {
   this.angle = ((this.HH % 12) * 30) + (Math.floor((this.MM * 60 + this.SS + 450) / 900) * 7.5); }}
 calc_marker_angle = () => {
  this.time_um.setTime(CW.time.getTime() + 10000);
  if(this.name == 'W60') {
   this.marker_angle = (((((this.time_um.getMinutes() - this.MM) % 60) * 6) + 180) % 360 + 360) % 360 - 180; }
  else if(this.name == 'W48') {
   this.marker_angle = ((((((this.time_um.getHours() % 12) * 30) + (Math.floor((this.time_um.getMinutes() * 60 + this.time_um.getSeconds() + 450) / 900) * 7.5)) - this.angle) + 180) % 360 + 360) % 360 - 180; }}
 place_svg_elems = () => {
  this.calc_angle();
  this.calc_marker_angle();
  $_(this.driven).setAttribute('transform', `rotate(${this.angle})`);
  $_(this.hand).setAttribute('transform', `scale(27) rotate(${this.angle + 180})`);
  if((this.name == 'W60') && (CW.shown_face == 1)) {
   $_('marker').setAttribute('transform', `rotate(${-this.marker_angle})`); }
  else if((this.name == 'W48') && (CW.shown_face == 0)) {
   $_('marker').setAttribute('transform', `rotate(${-this.marker_angle})`); }}
 setTime = (hh,mm,ss) => {
  this.HH = hh;
  this.MM = mm;
  this.SS = ss;
  this.place_svg_elems(); }
 inc_HH = () => {
  if(++this.HH > 23) this.HH -= 24;
  this.place_svg_elems(); }
 dec_HH = () => {
  if(--this.HH < 0) this.HH += 24;
  this.place_svg_elems(); }
 inc_MM = () => {
  if(++this.MM > 59) {
   this.MM -= 60;
   if(++this.HH > 23) this.HH -= 24; }
  this.place_svg_elems(); }
 dec_MM = () => {
  if(--this.MM < 0) {
   this.MM += 60;
   if(--this.HH < 0) this.HH += 24; }
  this.place_svg_elems(); }
 inc_SS = () => {
  if(++this.SS > 59) {
   this.SS -= 60;
   if(++this.MM > 59) {
    this.MM -= 60;
    if(++this.HH > 23) this.HH -= 24; }}
  this.place_svg_elems(); }
 dec_SS = () => {
  if(--this.SS < 0) {
   this.SS += 60;
   if(--this.MM < 0) {
    this.MM += 60;
    if(--this.HH < 0) this.HH += 24; }}
  this.place_svg_elems(); }
 move = () => {
  console.log(`this is ${this.name}.move();`);
  var dir = Math.sign(this.marker_angle);
  console.log(`dir: ${dir}`);
  if(dir != 0) {
   if(this.name == 'W60') {
    D_MNS.autorotate(dir * CW.move_speed * -1); }
   else if(this.name == 'W48') {
    D_HRS.autorotate(dir * CW.move_speed * -1); }}}
 fix = (s) => {
  console.log(`${this.name} FIX: s = ${s}`);
  if(this.name == 'W60') {
   this.MM += s;
   if(this.MM > 59) {
    this.MM -= 60;
    if(++this.HH > 23) this.HH -= 24; }
   if(this.MM < 0) {
    this.MM += 60;
    if(--this.HH < 0) this.HH += 24; }
   this.place_svg_elems(); }
  else if(this.name == 'W60') { }} }

class clockwork {
 static CW = new clockwork();
 constructor() {
  this.time = new Date();
  this.time.setHours(12);
  this.time.setMinutes(0);
  this.time.setSeconds(0);
  this.time.setMilliseconds(0);
  this.time_um = new Date(); // upcomming time for move
  this.HH = this.time.getHours();
  this.MM = this.time.getMinutes();
  this.PS = -1;              // previous second
  this.interval = 1000;      // interval for run
  this.IH = 0;               // interval handler
  this.running = false;
  this.HH_angle = 0;
  this.MM_angle = 0;
  this.marker_angle_HH = 0;
  this.marker_angle_MM = 0;
  this.marker_angle = 0;
  this.shown_face = 0;
  this.move_speed = 12;
  this.enter_mode = 0; }
 rotate = (A,n,t,s) => {
  // console.log(`${n}: ${A.toFixed(3)}° ROT: ${t} S:${s}`);
  // debug(`${n}: ${A.toFixed(3)}° ROT: ${t} S:${s} ${String(this.HH).padStart(2,'0')}:${String(this.MM).padStart(2,'0')} HH: ${this.HH_angle}° [Δ=${this.marker_angle_HH}°] MM: ${this.MM_angle}° [Δ=${this.marker_angle_MM}°] MK: ${this.marker_angle}°`);
  if(this.shown_face == 0) { // HRS
   if((n == 'D_MNS') && (t != 0)) {
    $_('MNS').setAttribute('transform', `scale(27) rotate(${this.MM_angle + 180 + A})`); }
   else if((n == 'D_HRS') && (t != 0)) {
    $_('geneva_48').setAttribute('transform', `rotate(${this.HH_angle + A})`);
    $_('marker').setAttribute('transform', `rotate(${-this.marker_angle + A})`);
    $_('HRS').setAttribute('transform', `scale(27) rotate(${this.HH_angle + 180 + A})`); }}
  else if(this.shown_face == 1) { // MNS
   if((n == 'D_MNS') && (t != 0)) {
    $_('geneva_60').setAttribute('transform', `rotate(${this.MM_angle + A})`);
    $_('marker').setAttribute('transform', `rotate(${-this.marker_angle + A})`);
    $_('MNS').setAttribute('transform', `scale(27) rotate(${this.MM_angle + 180 + A})`); }
   else if((n == 'D_HRS') && (t != 0)) {
    $_('HRS').setAttribute('transform', `scale(27) rotate(${this.HH_angle + 180 + A})`); }}
  if(t == 0) {
   // this.fix_(-s,n);
   if(n == 'D_MNS') W60.fix(-s);
   else if(n == 'D_HRS') W48.fix(-s); }}
 tick_ = () => {
  if(realtime) {
   var rt = new Date();
   this.time.setTime(rt.getTime()); }
  else {
   var hh = this.time.getHours();
   var mm = this.time.getMinutes();
   var ss = this.time.getSeconds();
   if(++ss == 60) {
    ss = 0;
    if(++mm == 60) {
     mm = 0;
     if(++hh == 24) {
      hh = 0; }}}
   this.time.setSeconds(ss);
   this.time.setMinutes(mm);
   this.time.setHours(hh); }
  if(this.time.getSeconds() != this.PS) {
   var ss = this.time.getSeconds();
   if(CW.enter_mode == 0) display_clock();
   W60.place_svg_elems();
   W48.place_svg_elems();
   if(ss == 20) {
    W48.move(); }
   if(ss == 50) {
    W60.move(); }
   this.PS = ss; }}
 start = () => {
  if(realtime) {
   this.IH = setInterval(this.tick_,250); }
  else {
   this.IH = setInterval(this.tick_,this.interval); }
  this.running = true; }
 stop = () => {
  if(this.running) {
   clearInterval(this.IH);
   this.running = false; }}
 set_HH = dh => {
  this.time.setHours(this.time.getHours() + dh); }
 set_MM = dm => {
  this.time.setMinutes(this.time.getMinutes() + dm); }
 set_SS = ds => {
  this.time.setSeconds(this.time.getSeconds() + ds); }
 fix_ = (d,n) => {
  // console.log(`fix_(${d},${n})`);
  if(n == 'D_MNS') {
   this.MM += d;
   if(this.MM > 59) {
    this.MM -= 60;
    if(++this.HH > 23) this.HH -= 24; }
   if(this.MM < 0) {
    this.MM += 60;
    if(--this.HH < 0) this.HH += 24; }
   this.show_face_();
   this.place_clockwork_('MM');
   this.move(); }
  else if(n == 'D_HRS') {
   this.show_face_();
   this.place_clockwork_('HH');
   this.move(); }}
 move = () => {
  var hh_dir = Math.sign(this.marker_angle_HH);
  var mm_dir = Math.sign(this.marker_angle_MM);
  if(hh_dir != 0) {
   D_HRS.autorotate(hh_dir * this.move_speed * -1); }
  if(mm_dir != 0) {
   D_MNS.autorotate(mm_dir * this.move_speed * -1); }}
 getRealTime_ = () => {
  var rt = new Date();
  this.HH = rt.getHours();
  this.MM = rt.getMinutes();
  this.time.setTime(rt.getTime()); }
 init = (hh='',mm='') => {
  if(realtime) {
   this.getRealTime_(); }
  else {
   this.HH = hh;
   this.MM = mm;
   this.time.setMilliseconds(0);
   this.time.setSeconds(0);
   this.time.setMinutes(mm);
   this.time.setHours(hh); }
  this.place_clockwork_(''); }
 cw_set = (hh,mm) => {
  $_('TC').innerHTML = `${String(hh).padStart(2,'0')}:${String(mm).padStart(2,'0')}`;
  console.log(`this is CW.set(${hh},${mm})`);
  this.MM = mm;
  this.HH = hh;
  this.show_face_();
  this.place_clockwork_(''); }
 cw_inc_hh = () => {
  if(++this.HH > 23) this.HH -= 24;
  this.show_face_();
  this.place_clockwork_(''); }
 cw_dec_hh = () => {
  if(--this.HH < 0) this.HH += 24;
  this.show_face_();
  this.place_clockwork_(''); }
 cw_inc_mm = () => {
  if(++this.MM > 59) {
   this.MM -= 60;
   if(++this.HH > 23) this.HH -= 24; }
  this.show_face_();
  this.place_clockwork_(''); }
 cw_dec_mm = () => {
  if(--this.MM < 0) {
   this.MM += 60;
   if(--this.HH < 0) this.HH += 24; }
  this.show_face_();
  this.place_clockwork_(''); }
 face_switch = (F=undefined) => {
  if(F == undefined) {}
  else {
   this.shown_face = F; }
  if(this.shown_face == 0) {
   $_('svg_48').style.display = 'none';
   $_('svg_60').style.display = 'block';
   this.shown_face = 1; }
  else {
   $_('svg_60').style.display = 'none';
   $_('svg_48').style.display = 'block';
   this.shown_face = 0; }
  this.show_face_(); }
 place_clockwork_ = (HM) => {
  if((HM == '') || (HM == 'MM')) {
   this.MM_angle = this.MM * 6;
   $_('geneva_60').setAttribute('transform', `rotate(${this.MM_angle})`);
   $_('MNS').setAttribute('transform', `scale(27) rotate(${this.MM_angle + 180})`); }
  if((HM == '') || (HM == 'HH')) {
   this.HH_angle = ((this.HH % 12) * 30) + (Math.floor((this.MM * 60 + 30 + 450) / 900) * 7.5);
   $_('geneva_48').setAttribute('transform', `rotate(${this.HH_angle})`);
   $_('HRS').setAttribute('transform', `scale(27) rotate(${this.HH_angle + 180})`); }
  $_('marker').setAttribute('transform', `rotate(${-this.marker_angle})`); }
 show_face_ = () => {
  this.mk_angle_();
  if(this.shown_face == 1) { // MNS
   this.marker_angle = this.marker_angle_MM;
   $_('marker').setAttribute('transform', `rotate(${-this.marker_angle})`); }
  else {                     // HRS
   this.marker_angle = this.marker_angle_HH;
   $_('marker').setAttribute('transform', `rotate(${-this.marker_angle})`); }}
 mk_angle_ = () => { // calculate marker angle for MM and HH
  this.time_um.setTime(this.time.getTime() + 10000);
  this.marker_angle_MM = (((((this.time_um.getMinutes() - this.MM) % 60) * 6) + 180) % 360 + 360) % 360 - 180;
  this.marker_angle_HH = ((((((this.time_um.getHours() % 12) * 30) + (Math.floor((this.time_um.getMinutes() * 60 + this.time_um.getSeconds() + 450) / 900) * 7.5)) - this.HH_angle) + 180) % 360 + 360) % 360 - 180; } }

polar2xy = (deg,r) => {
 const cx = 0;
 const cy = 0;
 const rad = deg * Math.PI / 180;
 return {
  x: cx + r * Math.sin(rad),
  y: cy - r * Math.cos(rad) }}

degToRad = deg => {
 return deg * Math.PI / 180; }

radToDeg = rad => {
 return rad * 180 / Math.PI; }

class Driver {
 tri_rotate = s => { // s: +1=BACK | -1=FORW
  // console.log(s);
  var rot = this.rotation % 120;
  var rad = degToRad(rot);
  var wheel_delta = 0;
  const a_stepx = wheels[this.orbits[this.name]]['wheel_angle_step'] - 0;
  const orbit_r = wheels[this.orbits[this.name]]['driving_pin_orbit_cm'] - 0;
  const axis_dx = wheels[this.orbits[this.name]]['driver_axis_dist_cm'] - 0;
  if(s > 0) {
   if(rot <= 60) {
    wheel_delta = radToDeg(Math.atan((orbit_r * Math.sin(rad)) / (axis_dx - (orbit_r * Math.cos(rad))))); }
   else {
    wheel_delta = a_stepx - radToDeg(Math.atan((orbit_r * Math.sin(2 * Math.PI / 3 - rad)) / (axis_dx - (orbit_r * Math.cos(2 * Math.PI / 3 - rad))))); }}
  else {
   if(rot > 60) {
    wheel_delta = -(radToDeg(Math.atan((orbit_r * Math.sin(2 * Math.PI / 3 - rad)) / (axis_dx - (orbit_r * Math.cos(2 * Math.PI / 3 - rad)))))); }
   else {
    wheel_delta = -(a_stepx - radToDeg(Math.atan((orbit_r * Math.sin(rad)) / (axis_dx - (orbit_r * Math.cos(rad)))))); }}
  // console.log(`ROT: ${rot} Δ: ${wheel_delta.toFixed(3)}`);
  CW.rotate(-wheel_delta,this.name,rot,s); }
 autorotate_ = deg => {
  this.rotation += deg;
  // console.log(this.rotation);
  if((this.rotation % 120) == 0) {
   this.rotation = 120;
   clearInterval(this.intv_handler);
   this.rotating = false; }
  this.tri_rotate(Math.sign(deg));
  $_(this.name).setAttribute('transform',`rotate(${this.angle}) translate(${this.radius}) rotate(${this.rotation})`); }
 autorotate = deg => {
  if(this.rotating) return;
  this.intv_handler = setInterval(() => {
   this.autorotate_(deg); }, 100);
   this.rotating = true; }
 constructor(name,radius,angle) {
  this.disks = {
   'D_HRS' : 'svg_48',
   'D_MNS' : 'svg_60' }
  this.orbits = {
   'D_HRS' : 'tri_driver_hrs',
   'D_MNS' : 'tri_driver_mns' }
  this.name = name;
  this.radius = radius;
  this.angle = angle;
  this.rotation = 120;
  this.rot_goto = 0;
  this.intv_handler;
  this.rotating = false;
  var drv = window.document.createElementNS(svgns,'g');
  drv.id = name;
  var peri = window.document.createElementNS(svgns,'circle');
  peri.setAttribute('class', 'driver_circle');
  peri.setAttribute('r', wheels[this.orbits[this.name]]['driving_pin_orbit_cm'] + 3);
  drv.appendChild(peri);
  var axis = window.document.createElementNS(svgns,'circle');
  axis.setAttribute('class','driver_axis');
  axis.setAttribute('r', wheels[this.orbits[this.name]]['driver_axis_diameter_cm'] / 2);
  drv.appendChild(axis);
  var R = wheels[this.orbits[this.name]]['driving_pin_orbit_cm'];
  var A = 30;
  for(var p=0;p<3;p++) {
   var pin_x = window.document.createElementNS(svgns,'circle');
   pin_x.setAttribute('class','driver_pin');
   var C = polar2xy(A,R);
   pin_x.setAttribute('r', wheels[this.orbits[this.name]]['driving_pin_diameter_cm'] / 2);
   pin_x.setAttribute('cx',C.x);
   pin_x.setAttribute('cy',C.y);
   drv.appendChild(pin_x);
   A += 120; }
  drv.setAttribute('transform',`rotate(${this.angle}) translate(${radius})`);
  parent = $_(this.disks[this.name]);
  parent.appendChild(drv);
  return this; }}

make_drivers = () => {
 W48 = new Wheel(wheels['W48']);
 W60 = new Wheel(wheels['W60']);
 var r = wheels['tri_driver_hrs']['driver_axis_dist_cm'];
 D_HRS = new Driver('D_HRS',r,axis_deg['HRS'] - 90);
 var r = wheels['tri_driver_mns']['driver_axis_dist_cm'];
 D_MNS = new Driver('D_MNS',r,axis_deg['MNS'] - 90); }
