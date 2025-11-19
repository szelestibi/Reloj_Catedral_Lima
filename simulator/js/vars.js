var svgns = 'http://www.w3.org/2000/svg';

var wWidth, wHeight;
var SH, SM;               // SHOWN TIME  - SET @ STARTUP
var HH, MM, SS;           // ACTUAL TIME - ACTUALIZED EVERY SECOND
var TH, TM, TS;           // TARGET TIME - TO BE INDICATED

// --- ETC CMANUAL SETTINGS BEGIN ---
var mode =  0;            // -1 FORCE DECO CLOCK WITH JUMPING HANDS, 0 = NORMAL RUN, 1 = TEST [AUTOSWITCH 0/1, SET mode = 0]
var secx = 50;            // second when the movement to next minute begins in mode 0
// --- ETC MANUAL SETTINGS END -----

var modes = {
 '-1' : 'HOME CLOCK',
  '0' : 'NORMAL RUN' }

var psec = -1;            // previous second value for time critical routines

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

var clockmove; // interval handler

var loaded = 0;

var D_HRS = 0;
var D_MNS = 0;

var CW;        // clockwork

// timer aux vars
var realtime =  true;
realtime = false;
var getTimeStarted = false;
var IH = 13;
var IM =  6;
var IS = 48;
var now_date = new Date();
if(realtime == false) {
 now_date.setHours(IH);
 now_date.setMinutes(IM);
 now_date.setSeconds(IS);
 now_date.setMilliseconds(0); }
