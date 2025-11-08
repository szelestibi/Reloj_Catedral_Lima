#!perl

# pixels to milimeters in selected lines

use constant EOL => "\n"; # END OF LINE
use constant PPI => 90;   # pixels per inch

$infile = 'dial.svp';
$outfile = 'dial.svm';
@lines = (1816,1819); # lines to convert pixels to mm | count from 1 = compatibility with text editors numbering

if(!open(INF,$infile)) {
 print($infile.': '.$!.EOL);
 sleep(3);
 exit(0); }
else {
 @inf = <INF>; chomp(@inf);
 close(INF); }

$linenr = 1;
$outx = '';
foreach $line (@inf) {
 if(rownr($linenr++)) {
  $outx .= '<!-- px to mm -->'.pixtomim($line).EOL; }
 else {
  $outx .= $line.EOL; }}

open(OUF,'>./'.$outfile);
print OUF $outx;
close(OUF);

sleep(1); exit(0);

sub rownr {
 my $ln = shift();
 foreach $li (@lines) {
  if($li == $ln) {
   return 1; }}
 return 0; }

sub pixtomim {
 my $line = shift();
 $line =~ s/^\s+|\s+$//g;  # trim first and last space[s]
 $line =~ s/\s{2,}/ /g;    # two spaces -> one space
 $line =~ s/(\-?[0-9\.]{2,})/px2mm($1).'mm'/ge;
 return($line); }

sub mm2px {
 my $mm = shift;
 return(sprintf('%.3f',($mm / 25.4 * PPI))); }

sub px2mm {
 my $px = shift;
 my $mm = sprintf('%.3f',($px * 25.4 / PPI));
 while((substr($mm,-1,1) eq '0') && (length($mm) > 1) && ($mm =~ /\./)) { $mm = substr($mm,0,-1); }
 if(substr($mm,-1,1) eq '.') { $mm = substr($mm,0,-1); }
 return($mm); }
