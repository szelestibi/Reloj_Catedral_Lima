var svgns = 'http://www.w3.org/2000/svg';

var wWidth, wHeight;

var realtime = true;    // true: real time, false: tim_HHMM
var tim_HHMM = '21:00'; // default time when realtime is false

var wheels = {
 'tri_driver_hrs' : {
  'wheel_angle_step' : 7.5,
  'driver_axis_dist_cm' : 59.337,
  'driving_pin_orbit_cm' : 4.327,
  'driver_axis_diameter_cm' : 2.00,
  'driving_pin_diameter_cm' : 2.00 },
 'tri_driver_mns' : {
  'wheel_angle_step' : 6,
  'driver_axis_dist_cm' : 58.949,
  'driving_pin_orbit_cm' : 3.463,
  'driver_axis_diameter_cm' : 2.00,
  'driving_pin_diameter_cm' : 2.00 }}

var axis_deg = {
 'MNS' : 23 * 6,
 'HRS' :  7 * 30 + 2 * 7.5 }

var views = { // svg  [cm]
 'global' : [130,130,-65,-65],
 'mins_driver_0' : [14,14,33,-50],
 'mins_driver_1' : [14,14,33,37],
 'hrs_driver_0' : [14,14,-48,34],
 'hrs_driver_1' : [14,14,-48,-48]}

var D_HRS = 0; // hours driver
var D_MNS = 0; // minutes driver

var CW;        // clockwork
