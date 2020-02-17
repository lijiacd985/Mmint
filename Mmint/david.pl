#!/usr/bin/perl
use strict;
use warnings;
require "./headerGeneral.pm";

getDavid($ARGV[0], $ARGV[0]. ".xls");
sub getDavid ##($in, $out)
{
    my ($in, $out) = @_;
    my @genes = ();
    open(IN, $in) or die;
    while(<IN>){
        chomp;
        my @f= split("\t",$_);
        push(@genes, $f[0]) ;
    }
    close(IN);
    
    #writeStringToFile(join("\n", @genes), "$in.lst");
    
    require "./david.pm";
    davidChartReport( join(",", @genes), "OFFICIAL_GENE_SYMBOL", "make_up", 0, $out);

}
