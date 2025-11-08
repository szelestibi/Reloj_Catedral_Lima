var wWidth, wHeight;
var geneva_angle_deg = 0; // geneva wheel rotation angle
var driver_angle_deg = 0; // driver wheel rotation angle

var face_switch_arg = 0;

var wheels = {
 'driver_axis_dist_cm' : '57.896',
 'geneva_48' : {
  'driving_pin_orbit_cm' : '3.816',
  'driving_pin_diameter_cm' : '1.25',
  'driving_pin_touch_angle_deg' : '10.92' },
 'geneva_60' : {
  'driving_pin_orbit_cm' : '3.074',
  'driving_pin_diameter_cm' : '1.00',
  'driving_pin_touch_angle_deg' : '12.75' }}

var axis_deg = {
 'MNS_0' :  7 * 6,
 'MNS_1' : 23 * 6,
 'HRS_0' :  7 * 30 + 2 * 7.5,
 'HRS_1' : 10 * 30 + 2 * 7.5 }

var views = { // svg  [cm]
 'global' : [-60,-60,120,120],
 'moon_driver_M' : [],
 'moon_driver_H' : [],
 'mins_driver_0' : [],
 'mins_driver_1' : [],
 'hrs_driver_0' : [],
 'hrs_driver_1' : []}
