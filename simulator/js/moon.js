polar2xy = (deg,r) => {
 const cx = 0;
 const cy = 0;
 const rad = deg * Math.PI / 180;
 return {
  x: cx + r * Math.sin(rad),
  y: cy - r * Math.cos(rad) }}

class Driver {
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
  this.name = name;
  this.radius = radius;
  this.angle = angle;
  this.rotation = 0;
  this.rot_goto = 0;
  this.intv_handler;
  this.rotating = false;
  var drv = window.document.createElementNS(svgns,'g');
  drv.id = name;
  if(name.includes('HRS')) {
   var peri = window.document.createElementNS(svgns,'circle');
   peri.setAttribute('class', 'driver_circle');
   peri.setAttribute('r', wheels['tri_driver_hrs']['driving_pin_orbit_cm'] + 3);
   drv.appendChild(peri);
   var axis = window.document.createElementNS(svgns,'circle');
   axis.setAttribute('class','driver_axis');
   axis.setAttribute('r', wheels['driver_axis_diameter_cm'] / 2);
   drv.appendChild(axis);
   var R = wheels['tri_driver_hrs']['driving_pin_orbit_cm'];
   var A = 30;
   for(var p=0;p<3;p++) {
    var pin_x = window.document.createElementNS(svgns,'circle');
    pin_x.setAttribute('class','driver_pin');
    var C = polar2xy(A,R);
    pin_x.setAttribute('r', wheels['tri_driver_hrs']['driving_pin_diameter_cm'] / 2);
    pin_x.setAttribute('cx',C.x);
    pin_x.setAttribute('cy',C.y);
    drv.appendChild(pin_x);
    A += 120; }
    drv.setAttribute('transform',`rotate(${angle}) translate(${radius})`);
   parent = $_('svg_48'); }
  else if(name.includes('MNS')) {
   var peri = window.document.createElementNS(svgns,'circle');
   peri.setAttribute('class', 'driver_circle');
   peri.setAttribute('r', wheels['tri_driver_mns']['driving_pin_orbit_cm'] + 3);
   drv.appendChild(peri);
   var axis = window.document.createElementNS(svgns,'circle');
   axis.setAttribute('class','driver_axis');
   axis.setAttribute('r', wheels['driver_axis_diameter_cm'] / 2);
   drv.appendChild(axis);
   var R = wheels['tri_driver_mns']['driving_pin_orbit_cm'];
   var A = 30;
   for(var p=0;p<3;p++) {
    var pin_x = window.document.createElementNS(svgns,'circle');
    pin_x.setAttribute('class','driver_pin');
    var C = polar2xy(A,R);
    pin_x.setAttribute('r', wheels['tri_driver_hrs']['driving_pin_diameter_cm'] / 2);
    pin_x.setAttribute('cx',C.x);
    pin_x.setAttribute('cy',C.y);
    drv.appendChild(pin_x);
    A += 120; }
   drv.setAttribute('transform',`rotate(${angle}) translate(${radius})`);
   parent = $_('svg_60'); }
  parent.appendChild(drv);
 return this; }}

make_drivers = () => {
 var r = wheels['tri_driver_hrs']['driver_axis_dist_cm'];
 D_HRS = new Driver('D_HRS',r,axis_deg['HRS'] - 90);
 var r = wheels['tri_driver_mns']['driver_axis_dist_cm'];
 D_MNS = new Driver('D_MNS',r,axis_deg['MNS'] - 90); }
