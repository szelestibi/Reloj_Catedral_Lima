#!perl

use constant EOL => "\n"; # END OF LINE
use constant PPI => 90;   # pixels per inch

$infile = @ARGV[0];                                     # print $infile."\n";

svm2svg($infile,0);

sleep(1); exit(0);

sub svm2svg {
 my $fname = shift();
 my $pmode = shift(); # process mode: 0 = as file, 1 = as inclusion
 my $filenm; my $outx; my @inf; my $fhin; my $fhout;
 if($fname !~ /.svm$/) {
  print('input file must be *.svm'.EOL);
  sleep(3);
  exit(0); }
 else {
  $filenm = (split('\.',(split('\x5C',$fname))[-1]))[0]; }
 if(!open($fhin,$fname)) {
  print($fname.': ERROR: '.($!).EOL);
  sleep(3);
  exit(0); }
 else {
  @inf = <$fhin>; chomp @inf;
  close $fhin; }
 foreach my $line (@inf) {
  if($line =~ /^#include\s(.+)/) { # include file
   $outx .= svm2svg($1,1); }
  elsif($line =~ /^##/) {}         # commented inclusion
  else {
   $line =~ s/(\-?[0-9\.]+)mm/mm2px($1)/ge;
   $line =~ s/(\-?[0-9\.]+)cm/cm2px($1)/ge;
   $outx .= $line.EOL; }}
 if($pmode == 1) {
  return($outx); }
 else {
  open($fhout,'>'.$filenm.'.svg');
  print $fhout $outx;
  close $fhout; }}

sub mm2px {
 my $mm = shift;
 return(sprintf('%.3f',($mm / 25.4 * PPI))); }

sub cm2px {
 my $mm = shift;
 return(sprintf('%.3f',($mm / 25.4 * PPI * 10))); }
