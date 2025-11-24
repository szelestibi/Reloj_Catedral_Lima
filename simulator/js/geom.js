get_geometry = () => {
 wWidth = window.innerWidth;
 wHeight = window.innerHeight; }

check_geom = () => {
 if(wWidth < wHeight) return 1; // portrait = V
 else return 0; }    // square or landscape = H

setdivpos = (ptr,xxx,yyy,www=0,hhh=0) => {
 if(typeof(ptr) == 'string') {
  ptr = $_(ptr); }
 ptr.style.position = 'absolute';
 ptr.style.left = xxx + 'px';
 ptr.style.top = yyy + 'px';
 if(www != 0) {
  ptr.style.width = www + 'px'; }
 if(hhh != 0) {
  ptr.style.height = hhh + 'px'; }}

setdivdim = (divPtr,xx,yy) => {
 if(typeof(divPtr) == 'string') {
  divPtr = $_(divPtr); }
 divPtr.style.position = 'absolute';
 divPtr.style.width = xx + 'px';
 divPtr.style.height = yy + 'px'; }
