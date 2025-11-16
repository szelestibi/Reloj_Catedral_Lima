class clockwork {
 static instance = new clockwork();
 constructor(hh = 12, mm = 0) {
  this.HH = hh;
  this.MM = mm; }
/* USAGE:
let cw = clockwork.instance;
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

class Driver {
 tri_rotate = () => {
  var rot = this.rotation;
  console.log(rot);
  const orbit_r = wheels[this.orbits[this.name]]['driving_pin_orbit_cm'] - 0;
  const axis_dx = wheels[this.orbits[this.name]]['driver_axis_dist_cm'] - 0;
  var wheel_delta = Math.atan((orbit_r * Math.sin(rot)) / (axis_dx - (orbit_r * Math.cos(rot))));
  return(`O: ${orbit_r} A: ${axis_dx} WD: ${wheel_delta}`); /**/ }
 autorot_ = d => {
  this.rotation += d;
  if((this.rotation % 120) == 0) {
   clearInterval(this.intv_handler);
   this.rotating = false; }
  $_(this.name).setAttribute('transform',`rotate(${this.angle}) translate(${this.radius}) rotate(${this.rotation})`); }
 autorotate = dir => {
  if(this.rotating) return;
  this.intv_handler = setInterval(() => {
   this.autorot_(dir); }, 100);
   this.rotating = true; }
 rotate_by = deg => {
  this.rotation += deg;
  $_(this.name).setAttribute('transform',`rotate(${this.angle}) translate(${this.radius}) rotate(${this.rotation})`); }
 rotate_to = deg => {
  this.rotation = deg;
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
  this.rotation = 0;
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
