window.onload = () => {
 get_geometry();
 face_switch_arg = 1;
 face_switch(face_switch_arg);
 dial = window.document.createElement('img');
 dial.id = 'clock_dial';
 dial.src = './svg/dial.svg';
 $_('clockface_container').appendChild(dial);
 dial.onload = () => {
  var rect = dial.getBoundingClientRect();
  var dial_xy = rect.width;
  console.log(`dial_xy: ${dial_xy}`);
  dial.style.width = (dial_xy * 77 / 100) + 'px'; }
 $_('clockface_container').onclick = () => {
  if(face_switch_arg == 0) face_switch_arg = 1;
  else face_switch_arg = 0;
  face_switch(face_switch_arg); }
}

face_switch = s => {
 if(s == 0) {
  $_('svg_48').style.display = 'none';
  $_('svg_60').style.display = 'block'; }
 else {
  $_('svg_60').style.display = 'none';
  $_('svg_48').style.display = 'block'; }}
