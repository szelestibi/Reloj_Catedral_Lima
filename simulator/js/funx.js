$_ = id => { return window.document.getElementById(id); }

cookieVal = cookieName => {
 thisCookie = document.cookie.split("; ");
 for(i=0;i<thisCookie.length;i++) {
  if(cookieName==thisCookie[i].split("=")[0]) {
   return thisCookie[i].split("=")[1]; }}
 return ''; }

getParamVal = getParamName => {
 thisParam = window.location.search.substring(1).split("&");
 for(i=0;i<thisParam.length;i++) {
  if(getParamName==thisParam[i].split("=")[0]) {
   return thisParam[i].split("=")[1]; }}
 return ''; }

normform = strnr => {
 if((strnr-0) < 10) {
  return('0' + '' + strnr); }
 else { return('' + strnr); }}

setCookie = (name,value,days=1) => {
 if(days) {
  var date = new Date();
   date.setTime(date.getTime() + (days*24*60*60*1000));
   var expires = '; expires=' + date.toGMTString(); }
  else {
   var expires = ""; }
  document.cookie = name + "=" + value + expires + "; path=/; SameSite=Lax"; }
