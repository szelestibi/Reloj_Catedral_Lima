var svgns = 'http://www.w3.org/2000/svg';

var wWidth, wHeight;
var SH, SM;               // SHOWN TIME  - SET @ STARTUP
var HH, MM, SS;           // ACTUAL TIME - ACTUALIZED EVERY SECOND
var TH, TM, TS;           // TARGET TIME - TO BE INDICATED

// --- ETC CMANUAL SETTINGS BEGIN ---
var mode = -1;            // -1 FORCE DECO CLOCK WITH JUMPING HANDS, 0 = NORMAL RUN, 1 = TEST [AUTOSWITCH 0/1, SET mode = 0]
var secx = 50;            // second when the movement to next minute begins in mode 0
// --- ETC MANUAL SETTINGS END -----

var modes = {
 '-1' : 'HOME CLOCK',
  '0' : 'NORMAL RUN' }

var DELTA_H = 0;
var DELTA_M = 0;

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

var loaded = 0;
