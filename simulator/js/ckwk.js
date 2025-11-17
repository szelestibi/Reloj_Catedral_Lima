class clockwork {
 static CW = new clockwork();
 constructor(hh = 12, mm = 0) {
  this.HH = hh;
  this.MM = mm;
  this.HH_angle = 0;
  this.MM_angle = 0;
  this.MK_angle = 0; }
/* USAGE:
let cw = clockwork.CW;
cw.HH = 3;
cw.MM = 15;
console.log(cw); */ }

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
 tri_rotate = s => {
  console.log(s);
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
  console.log(`ROT: ${rot} Δ: ${wheel_delta.toFixed(3)}`);
  /* CW */ }
 autorotate_ = deg => {
  this.rotation += deg;
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
 rotate_by = deg => {
  this.rotation += deg;
  this.rotation %= 120 + 120;
  $_(this.name).setAttribute('transform',`rotate(${this.angle}) translate(${this.radius}) rotate(${this.rotation})`); }
 rotate_to = deg => {
  this.rotation = deg;
  this.rotation %= 120 + 120;
  $_(this.name).setAttribute('transform',`rotate(${this.angle}) translate(${this.radius}) rotate(${this.rotation})`); }
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
 var r = wheels['tri_driver_hrs']['driver_axis_dist_cm'];
 D_HRS = new Driver('D_HRS',r,axis_deg['HRS'] - 90);
 var r = wheels['tri_driver_mns']['driver_axis_dist_cm'];
 D_MNS = new Driver('D_MNS',r,axis_deg['MNS'] - 90); }
