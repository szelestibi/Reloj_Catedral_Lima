var svgns = 'http://www.w3.org/2000/svg';

var wWidth, wHeight;
var SH, SM;               // START HOUR, START MINUTE
var HH, MM, SS;           // time indicated by clock
var TH, TM, TS;           // target time = to be indicated
var geneva_angle_deg = 0; // geneva wheel rotation angle
var driver_angle_deg = 0; // driver wheel rotation angle

// --- MANUAL SETTINGS BEGIN ---
var mode =  0;            // -1 DECO CLOCK, 0 = normal run [TIME to TH+TM], 1+ = test [set TH+TM manually]
var secx = 50;            // second when the movement to next minute begins
// --- MANUAL SETTINGS END -----

var modes = {
 '-1' : 'HOME CLOCK',
  '0' : 'NORMAL RUN' }

var psec = -1;            // previous second value for time critical routines

var face_switch_arg = 0;

var zoomed = 0;

var wheels = {
 'driver_axis_dist_cm' : 57.896,
 'driver_axis_diameter_cm' : 1.00,
 'geneva_48' : {
  'driving_pin_orbit_cm' : 3.816,
  'driving_pin_diameter_cm' : 1.25,
  'driving_pin_touch_angle_deg' : 10.92 },
 'geneva_60' : {
  'driving_pin_orbit_cm' : 3.074,
  'driving_pin_diameter_cm' : 1.00,
  'driving_pin_touch_angle_deg' : 12.75 }}

var axis_deg = {
 'MNS_0' :  7 * 6,
 'MNS_1' : 23 * 6,
 'HRS_0' :  7 * 30 + 2 * 7.5,
 'HRS_1' : 10 * 30 + 2 * 7.5 }

var views = { // svg  [cm]
 'global' : [130,130,-65,-65],
 'mins_driver_0' : [14,14,33,-50],
 'mins_driver_1' : [14,14,33,37],
 'hrs_driver_0' : [14,14,-48,34],
 'hrs_driver_1' : [14,14,-48,-48]}

var drivers = {}

var clockmove; // interval handler
