#!/usr/bin/perl

# shorten long floats [as 123.4567895154] up to three decimals

use constant EOL => "\n"; # END OF LINE

$infile = 's.svg';
$outfile = 't.svg';

open(MNS,'./'.$infile);
@mns = <MNS>; chomp(@mns);
close MNS;

$outstr = '';

foreach $line (@mns) {
 $line =~ s/([0-9]+)\.([0-9]+)/$1.'.'.substr($2,0,3)/ge;
 $outstr .= $line.EOL; }

open(MNO,'>./'.$outfile);
print MNO $outstr;
close MNO;

# sleep(3);

exit(0);
