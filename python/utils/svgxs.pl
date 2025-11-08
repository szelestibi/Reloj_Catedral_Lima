#!perl

# translate and scale [XS]

use constant EOL => "\n";            # END OF LINE
use constant PPI => 90;              # pixels per inch

$dir = "./";
$myname = (split('\.',(split('\x5C',$0))[-1]))[0]; # print($myname.EOL); # this script's name without ending [windows]

$xsparams = '0,0,2,2';               # transform params: translate x,translate y,scale x,scale y [px|mm|cm,px|mm|cm,%,%] '0,0,1,1' = do nothing
$order = 'xs';                       # xs [translate-scale] or sx [scale-translate]

$filename = 'svgsz.svg';             # SVG file to process
$oouussttrr = '';

#$string = '<path style="stroke:#FF0000; stroke-width:4; fill:#7F7FFF;" transform="scale(.05) translate(2000 3000) rotate(180)" d="M 692 1247 H 516 V 0 H 201 V 1247 H 25 V 1434 H 692 V 1247 Z" /><!-- T -->';
#$oouussttrr .= lineprocess($string);

if(!open(SVG,'./'.$filename)) {
 print('ERROR: '.$filename.' '.$!.EOL);
 countdown(3);
 exit(0); }
else {
 print('processing '.$filename.EOL);
 @svg = <SVG>;
 chomp(@svg);
 close(SVG);
 $outstr = '';
 foreach my $line (@svg) {
 $outstr .= lineprocess($line); }
$oouussttrr .= $outstr; }

open(SVO,'>'.$myname.'.svg') or die($!);
print SVO ($oouussttrr.'<!-- SZT 06 2016 -->'.EOL);
close SVO;

sleep(1); exit(0);

opendir (DIR,"$dir");
@entries = readdir(DIR);
closedir DIR;

@svglist = @svg = ();                # GLOBALS

foreach $entry (@entries) {          # create SVG entries list of $dir
 if(($entry =~ /([0-9A-Za-z]+)\.(svg|SVG)$/) && ($entry !~ /^$myname\.svg/)) {
  push(@svglist,$1); }}

$oouussttrr = '';

foreach my $svgfile (@svglist) {
 if(!open(SVG,'./'.$svgfile.'.svg')) {
  print('ERROR: '.$svgfile.' '.$!.EOL);
  countdown(3);
  exit(0); }
 else {
  print('processing '.$svgfile.'.SVG'.EOL);
  @svg = <SVG>;
  chomp(@svg);
  close(SVG);
  $outstr = '';
  foreach my $line (@svg) {
  #print($line.EOL);
  $outstr .= lineprocess($line); }
 $oouussttrr .= $outstr; }}

open(SVO,'>'.(split('\.',(split('\x5C',$0))[-1]))[0].'.svg');
print SVO ('<?xml version="1.0" encoding="utf-8"?>'.EOL);
print SVO ('<svg version="1.2" class="svggear" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="3000px" height="3000px" viewBox="-1500 -1500 3000 3000" overflow="scroll" xml:space="preserve">'.EOL);
print SVO ('<!-- SZT 2016 -->'.EOL);
print SVO ($oouussttrr.EOL);
print SVO ('</svg>'.EOL);
close SVO;

if($info != 0) {
 close INF; }

sleep(3); exit(0);
#countdown(3); exit(0);

sub lineprocess {
 my $svgline = shift();
 my $outstr = '';
 if($svgline =~ /(\s*?)(<path.*?)\sd="(.+?)"(.*)/) {             # path d="..." ---------------------------------------------
  my $spacepart = $1;
  my $pathpart1 = $2;
  my $pathdata = $3;
  my $pathpart3 = $4;
  my @pathdata = ();
  my $collect = '';
  while(length($pathdata) > 0) {
   if(substr($pathdata,0,1) =~ /([A-DF-Za-df-z])/) {       # exclude E,e
    $letter = $1;
    if($collect ne '') {
     push(@pathdata,$collect);
     $collect = ''; }
    $collect = $letter;
	$pathdata = substr($pathdata,1); }
   else {
    $collect .= substr($pathdata,0,1);
    $pathdata = substr($pathdata,1); }}
  push(@pathdata,$collect);
  if($info =~ /1/) {
   print INF ('   PATH: '.join('+',@pathdata).EOL); }
  foreach my $entry (@pathdata) {
   $entry =~ s/^\s+|\s+$//g;  # trim first and last space[s]
   $entry =~ s/\s{2,}|\,/ /g; # change one/more spaces and/or comma with one space
   my @entry = split(' ',$entry);
   if($info =~ /2/) { print INF (join(' + ',@entry).EOL); }
   if(@entry[0] =~ /M|m/) {      # moveto [2 params] --------------------------------------------------------
    $outstr .= 'M'.' '.xform($entry[1],'TSX').' '.xform($entry[2],'TSY').' '; }
   elsif(@entry[0] =~ /L|l/) { # lineto [2 params or multiple of] -------------------------------------------
    $outstr .= shift(@entry); # L or l
    while($#entry > -1) { 
     my $xd = shift(@entry);
     my $yd = shift(@entry);
     $outstr .= ' '.xform($xd,'TSX').' '.xform($yd,'TSY').' '; }}
   elsif(@entry[0] =~ /H|h/) { # lineto H [1 param or multiple of] ------------------------------------------
    $outstr .= shift(@entry); # H or h
    while($#entry > -1) { 
     my $xd = shift(@entry);
     $outstr .= ' '.xform($xd,'TSX').' '; }}
   elsif(@entry[0] =~ /V|v/) { # lineto V [1 param or multiple of] ------------------------------------------
    $outstr .= shift(@entry); # V or v
    while($#entry > -1) { 
     my $yd = shift(@entry);
     $outstr .= ' '.xform($yd,'TSY').' '; }}
   elsif(@entry[0] =~ /A|a/) { # elliptic arc [7 params or multiple of] -------------------------------------
    $outstr .= shift(@entry); # A
    while($#entry > -1) { 
     my $rx = shift(@entry);
     my $ry = shift(@entry);
     my $rt = shift(@entry);
     my $fl = shift(@entry);
     my $ar = shift(@entry);
     my $dx = shift(@entry);
     my $dy = shift(@entry);
     $outstr .= ' '.xform($rx,'SX').' '.xform($ry,'SY').' '.xform($rt,'').' '.xform($fl,'').' '.xform($ar,'').' '.xform($dx,'TSX').' '.xform($dy,'TSY').' '; }}
   elsif(@entry[0] =~ /Q|q/) { # quadratic bezier [4 params or multiple of] ---------------------------------
    $outstr .= shift(@entry); # Q
    while($#entry > -1) { 
     my $xd = shift(@entry);
     my $yd = shift(@entry);
     my $dx = shift(@entry);
     my $dy = shift(@entry);
     $outstr .= ' '.xform($xd,'TSX').' '.xform($yd,'TSY').' '.xform($dx,'TSX').' '.xform($dy,'TSY').' '; }}
   elsif(@entry[0] =~ /T|t/) { # quadratic bezier with reflexion or current point as ref [2 params or multiple of]
    $outstr .= shift(@entry); # T
    while($#entry > -1) { 
     my $xd = shift(@entry);
     my $yd = shift(@entry);
     $outstr .= ' '.xform($xd,'TSX').' '.xform($yd,'TSY').' '; }}
   elsif(@entry[0] =~ /C|c/) { # cubic bezier [6 params or multiple of] -------------------------------------
    $outstr .= shift(@entry); # C
    while($#entry > -1) { 
     my $xd = shift(@entry);
     my $yd = shift(@entry);
     my $xx = shift(@entry);
     my $yy = shift(@entry);
     my $dx = shift(@entry);
     my $dy = shift(@entry);
     $outstr .= ' '.xform($xd,'TSX').' '.xform($yd,'TSY').' '.xform($xx,'TSX').' '.xform($yy,'TSY').' '.xform($dx,'TSX').' '.xform($dy,'TSY').' '; }}
   elsif(@entry[0] =~ /S|s/) { # cubic bezier [4 params or multiple of]
    $outstr .= shift(@entry); # C
    while($#entry > -1) { 
     my $xd = shift(@entry);
     my $yd = shift(@entry);
     my $dx = shift(@entry);
     my $dy = shift(@entry);
     $outstr .= ' '.xform($xd,'TSX').' '.xform($yd,'TSY').' '.xform($dx,'TSX').' '.xform($dy,'TSY').' '; }}
   elsif(@entry[0] =~ /Z|z/) { # close path [no params]
    $outstr .= shift(@entry); }
   else {}}
  $outstr =~ s/^\s+|\s+$//g;  # trim first and last space[s]
  $outstr =~ s/\s{2,}/ /g;
  $outstr = $spacepart.$pathpart1.' d="'.$outstr.'"'.$pathpart3.EOL;  }
 elsif($svgline =~ /(<polygon.+?)\spoints="(.+?)"(.*)/) {  # polygon points="..." -------------------------------------
  my $polypart1 = $1;
  my $polydata = $2;
  my $polypart3 = $3;
  $polydata =~ s/^\s+|\s+$//g;  # trim first and last space[s]
  $polydata =~ s/\s{2,}|\,/ /g; # change one/more spaces and/or comma with one space
  my @polydata = split('\s+',$polydata);
  if($info =~ /1/) { print INF ('POLYGON: '.join(' ',@polydata).EOL); }
  my $outstr = '';
  while($#polydata > -1) {
   my $xd = shift(@polydata);
   my $yd = shift(@polydata);
   $outstr .= xform($xd,'TSX').' '.xform($yd,'TSY').' '; }
  $outstr =~ s/^\s+|\s+$//g;  # trim first and last space[s]
  $outstr =~ s/\s{2,}/ /g; }
 elsif($svgline =~ /(<polyline.+?)\spoints="(.+?)"(.*)/) { # polyline points="..." ------------------------------------
  my $polypart1 = $1;
  my $polydata = $2;
  my $polypart3 = $3;
  $polydata =~ s/^\s+|\s+$//g;  # trim first and last space[s]
  $polydata =~ s/\s{2,}|\,/ /g; # change one/more spaces and/or comma with one space
  my @polydata = split('\s+',$polydata);
  if($info =~ /1/) { print INF ('POLYLINE: '.join(' ',@polydata).EOL); }
  my $outstr = '';
  while($#polydata > -1) {
   my $xd = shift(@polydata);
   my $yd = shift(@polydata);
   $outstr .= xform($xd,'TSX').' '.xform($yd,'TSY').' '; }
  $outstr =~ s/^\s+|\s+$//g;  # trim first and last space[s]
  $outstr =~ s/\s{2,}/ /g; }
 elsif($svgline =~ /(\s*?)(<circle.*?)\scx="(.+?)"\scy="(.+?)"\sr="(.+?)"(.*)/) { # <circle cx="0" cy="0" r="177.165" />
  my $spacepart = $1;
  my $circlepart1 = $2;
  my $cx = $3;
  my $cy = $4;
  my $rr = $5;
  my $circlepart5 = $6;
  $outstr = $circlepart1.' cx="'.xform($cx,'TSX').'" cy="'.xform($cy,'TSY').'" r="'.xform($rr,'S').'" '.$circlepart5;
  $outstr =~ s/^\s+|\s+$//g;  # trim first and last space[s]
  $outstr =~ s/\s{2,}/ /g;
  $outstr = $spacepart.$outstr.EOL; }
 else { # nothing matched: leave line
  if($svgline =~ /<\/svg>/) {
   $outstr = $svgline; }
  else {
   $outstr = $svgline.EOL; }}
 return($outstr); }

# <circle class="hole" cx="354.330" cy="252.517" r="70.866" />

sub countdown {
 use IO::Handle;
 STDOUT -> autoflush(1);
 my $cdval = shift();
 for(my $cnt=$cdval;$cnt>0;$cnt--) {
  print('WAIT '.$cnt.' s ...'."\r");
  sleep(1); }
 print '                    '.EOL; }

sub xform {                                                # TRANSFORM
 my $number = shift();
 my $mode = shift();
 my @xsparams = split(',',$xsparams);
 my $tx = @xsparams[0]; # translate x
 my $ty = @xsparams[1]; # translate y
 if($tx =~ /.+?mm$/) { $tx = mm2px(substr($tx,0,-2)); }
 elsif($tx =~ /.+?cm$/) { $tx = cm2px(substr($tx,0,-2)); }
 if($ty =~ /.+?mm$/) { $ty = mm2px(substr($ty,0,-2)); }
 elsif($ty =~ /.+?cm$/) { $ty = cm2px(substr($ty,0,-2)); }
 if($ty =~ /.+?px$/) { $ty = substr($ty,0,-2); }
 elsif($ty =~ /.+?px$/) { $ty = substr($ty,0,-2); }
 my $sx = @xsparams[2]; # scale x
 my $sy = @xsparams[3]; # scale y
 if($info =~ /6/) { print INF ('NR: '.$number.' XPARAMS: '.$xparams.' '.join('+',@xparams).' X: '.$sx.' MODE: '.$mode.EOL); }
 my $outx = '';
 if($order eq 'xs') { # order: xs
  if($mode =~ /T/) {     # translate
   if($mode =~ /X/) {    # X
    $number = $number + $tx;
    $outx = $number; }
   elsif($mode =~ /Y/) { # Y
    $number = $number + $ty;
    $outx = $number; }
   else {}}
  if($mode =~ /S/) {     # scale
   if($mode =~ /X/) {    # X
    $number = $number * $sx;
    $outx = $number; }
   elsif($mode =~ /Y/) { # Y
    $number = $number * $sy;
    $outx = $number; }
   else {
    $number = $number * ($sx + $sy) / 2;
    $outx = $number; }}}
 else {
  if($mode =~ /S/) {     # scale
   if($mode =~ /X/) {    # X
    $number = $number * $sx;
    $outx = $number; }
   elsif($mode =~ /Y/) { # Y
    $number = $number * $sy;
    $outx = $number; }
   else { # order: not xs, supposed sx
    $number = $number * ($sx + $sy) / 2;
    $outx = $number; }}
  if($mode =~ /T/) {     # translate
   if($mode =~ /X/) {    # X
    $number = $number + $tx;
    $outx = $number; }
   elsif($mode =~ /Y/) { # Y
    $number = $number + $ty;
    $outx = $number; }
   else {}}}
 if($mode eq '') {
  $outx = $number; }
 if(($outx == 0) || ($outx == 1)) { $toout = $outx; }
 else { $toout = sprintf('%.3f',$outx); }
 while((substr($toout,-1,1) eq '0') && (length($toout) > 1)) { $toout = substr($toout,0,-1); }
 if(substr($toout,-1,1) eq '.') { $toout = substr($toout,0,-1); }
 return($toout); }

sub mm2px {
 my $mm = shift;
 return(sprintf('%.3f',($mm / 25.4 * PPI))); }

sub cm2px {
 my $mm = shift;
 return(sprintf('%.3f',($mm / 25.4 * PPI * 10))); }
