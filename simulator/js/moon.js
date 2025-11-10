class Driver {
 constructor(name,radius,angle) {
  this.name = name;
  var drv = window.document.createElementNS(svgns,'g');
  drv.id = name;
  if(name.includes('D48')) {
   var peri = window.document.createElementNS(svgns,'circle');
   peri.setAttribute('class', 'driver_circle');
   peri.setAttribute('r', wheels['geneva_48']['driving_pin_orbit_cm'] + 1);
   drv.appendChild(peri);
   var axis = window.document.createElementNS(svgns,'circle');
   axis.setAttribute('class','driver_axis');
   axis.setAttribute('r', wheels['driver_axis_diameter_cm'] / 2);
   drv.appendChild(axis);
   var pin_1 = window.document.createElementNS(svgns,'circle');
   pin_1.setAttribute('class','driver_pin');
   pin_1.setAttribute('r', wheels['geneva_48']['driving_pin_diameter_cm'] / 2);
   pin_1.setAttribute('cy',wheels['geneva_48']['driving_pin_orbit_cm']);
   drv.appendChild(pin_1);
   var pin_2 = window.document.createElementNS(svgns,'circle');
   pin_2.setAttribute('class','driver_pin');
   pin_2.setAttribute('r', wheels['geneva_48']['driving_pin_diameter_cm'] / 2);
   pin_2.setAttribute('cy',-wheels['geneva_48']['driving_pin_orbit_cm']);
   drv.appendChild(pin_2);
   if(name.includes('_0')) {
    drv.setAttribute('transform',`rotate(${angle}) translate(${radius}) rotate(${-wheels['geneva_48']['driving_pin_touch_angle_deg']})`); }
   else if(name.includes('_1')) {
    drv.setAttribute('transform',`rotate(${angle}) translate(${radius}) rotate(${wheels['geneva_48']['driving_pin_touch_angle_deg']})`); }
   parent = $_('svg_48'); }
  else if(name.includes('D60')) {
   var peri = window.document.createElementNS(svgns,'circle');
   peri.setAttribute('class', 'driver_circle');
   peri.setAttribute('r', wheels['geneva_60']['driving_pin_orbit_cm'] + 1);
   drv.appendChild(peri);
   var axis = window.document.createElementNS(svgns,'circle');
   axis.setAttribute('class','driver_axis');
   axis.setAttribute('r', wheels['driver_axis_diameter_cm'] / 2);
   drv.appendChild(axis);
   var pin_1 = window.document.createElementNS(svgns,'circle');
   pin_1.setAttribute('class','driver_pin');
   pin_1.setAttribute('r', wheels['geneva_60']['driving_pin_diameter_cm'] / 2);
   pin_1.setAttribute('cy',wheels['geneva_60']['driving_pin_orbit_cm']);
   drv.appendChild(pin_1);
   var pin_2 = window.document.createElementNS(svgns,'circle');
   pin_2.setAttribute('class','driver_pin');
   pin_2.setAttribute('r', wheels['geneva_60']['driving_pin_diameter_cm'] / 2);
   pin_2.setAttribute('cy',-wheels['geneva_60']['driving_pin_orbit_cm']);
   drv.appendChild(pin_2);
   if(name.includes('_0')) {
    drv.setAttribute('transform',`rotate(${angle}) translate(${radius}) rotate(${-wheels['geneva_60']['driving_pin_touch_angle_deg']})`); }
   else if(name.includes('_1')) {
    drv.setAttribute('transform',`rotate(${angle}) translate(${radius}) rotate(${wheels['geneva_60']['driving_pin_touch_angle_deg']})`); }
   parent = $_('svg_60'); }
  parent.appendChild(drv);
 return drv; }}

make_drivers = () => {
 var r = wheels['driver_axis_dist_cm'];
 var D48_0 = new Driver('D48_0',r,axis_deg['HRS_0'] - 90);
 var D48_1 = new Driver('D48_1',r,axis_deg['HRS_1'] - 90);
 var D60_0 = new Driver('D60_0',r,axis_deg['MNS_0'] - 90);
 var D60_1 = new Driver('D60_1',r,axis_deg['MNS_1'] - 90); }
