#!/usr/bin/perl
use strict;
use warnings;

use Getopt::Long;

my %opts;
GetOptions(\%opts,"t:s","r:s","o:s","s:i");
my $ver = "1.0";
my $usage=<<"USAGE";
        Program : $0
        Version : $ver
        Contact : deqiangs\@bcm.edu
        Usage : $0 [options]
                -t 	<str>	type 'peaks.bed', 'origin.bw', 'diff.bw', 'bw', 'bam','bb'
		-r 	<str>	mm9 or hg18
		-s 	<int>	scale eg.250
                -o	<str>	output file name. default: ucsc.type.txt
USAGE

die $usage unless ($opts{"t"} and $opts{"r"});
$opts{"s"}=250 unless defined($opts{"s"});
print STDERR "Executing your command: $0 ",  join(' ', @ARGV), "\n";

my $type = $opts{"t"};
if( $type ne 'peaks.bed' and $type ne 'origin.bw' and $type ne 'diff.bw' and $type ne 'bw' and $type ne 'bam' and $type ne 'bb')
{
	print STDERR "type must be one of peaks.bed, origin.bw, or diff.bw, or bw, or bb, while you input $type\n";
	die;
}

my $db = $opts{"r"};

if( $db ne 'mm10' and $db ne 'hg18' and $db ne 'hg19' )
{
	print STDERR "db must be one of mm9, hg18, or hg19, while you input $db\n";
	die;
}


my $path = `pwd`;
chomp($path);
$path = $path . '/';
$path =~ /(.*)jiali(.*)/;
my $relative_path = $2;
#$relative_path = $2.'/';
$relative_path = $2;
print $relative_path;
my $remote_www = "/var/www/html/lilab/deqiangs";
$remote_www = $remote_www . $relative_path;

print STDERR "\n....Generate txt for UCSC genome browser...................\n";
#bed type already has track name="MACS peaks for PMWT_227.export.txt.tag2m.bed.macs" as the first line.
#or for the grouped bed files it is: track name="MACS peaks for RMWT-Input"
my @selected_files = <*$type>;
my $ucsc_text_file = 'ucsc.'.$type.'.txt';
if( defined $opts{"o"} )
{
		$ucsc_text_file = $opts{"o"};
}
open(WRTER,">$ucsc_text_file") or die " can not open $ucsc_text_file: $!";
open(WRTDB,">$ucsc_text_file.db") or die " can not open $ucsc_text_file.db: $!";
#print WRTER "browser hide all\nbrowser full all\n"; 
my $file_abs_path = $path . $ucsc_text_file;
system( "ssh selenium018 'cd $remote_www && ln -s $file_abs_path' " );
print STDERR "This is the link for $db, $type:\n";
print STDERR "http://genome.ucsc.edu/cgi-bin/hgTracks?db=$db&position=chr1:46897500-46918500&hgt.customText=http://dldcc-web.brc.bcm.edu/lilab/deqiangs$relative_path$ucsc_text_file\n";	
foreach my $file ( @selected_files )
{
	my @file_fields = split('\.',$file);
	my $ucsc_name = $file_fields[0];
	$ucsc_name =~  s/_export//;
	my $newFile = "https://dsunlab.srv.tamhsc.edu/jiali$relative_path".$file;
	
	$file_abs_path = $path . $file;
	system( "ssh selenium018 'cd $remote_www && ln -s $file_abs_path' " );
	
	
	if($type eq 'peaks.bed')
	{
		#my @file_fields = split('.',$file);
		#my $seed = $file_fields[0];
		#my $track_name = $seed.'-Input';
		print WRTER "$newFile\n";
		#$ucsc_name = $ucsc_name.'.'.$type;
		#my $record ="track name=$ucsc_name url=$newFile";
		#print WRTER "$record\n";		
	}
	elsif( $type eq 'origin.bw' or $type eq 'diff.bw' or $type eq 'bw')
	{

		
		if ( $type eq 'origin.bw' )
		{
			$ucsc_name = $ucsc_name;#.'.'.$type;
		}elsif ( $type eq 'diff.bw' )
		{
			$ucsc_name = $ucsc_name.'-Input';#.'.'.$type;
		}elsif ( $type eq 'bw' )
		{
			$ucsc_name = $ucsc_name;#.'.'.$type;
		}

		my $record ="track type=bigWig name=\"$ucsc_name.bw\" db=$db color=0,60,120 visibility=2 windowingFunction=maximum viewLimits=0:$opts{s} autoScale=off bigDataUrl=$newFile";
		print WRTER "$record\n";
		print WRTDB join("\n", "track $ucsc_name.bw", "type bigWig", "shortLabel $ucsc_name.bw", "longLabel $ucsc_name.bw", "visibility 0", "windowingFunction maximum", "viewLimits 0:$opts{s}", "autoScale off", "bigDataUrl $newFile"),"\n\n";
	}
	elsif( $type eq 'bam' )
	{
		my $record ="track type=bam name=\"$ucsc_name.bam\" db=$db visibility=2 windowingFunction=maximum bigDataUrl=$newFile";
		print WRTER "$record\n";
		print WRTDB join("\n", "track $ucsc_name.bm", "type bam", "shortLabel $ucsc_name.bm", "longLabel $ucsc_name.bm", "visibility 0", "windowingFunction maximum", "bigDataUrl $newFile"),"\n\n";
	}
	elsif( $type eq 'bb' )
	{
		my $record ="track type=bigBed name=\"$ucsc_name.bb\" db=$db visibility=2 itemRgb=On useScore=1 color=0,60,120 windowingFunction=maximum bigDataUrl=$newFile";
		
		print WRTER "$record\n";
		print WRTDB join("\n", "track $ucsc_name.bb", "type bigBed", "shortLabel $ucsc_name.bb", "longLabel $ucsc_name.bb", "visibility 0", "itemRgb On", "useScore 1", "color 0,60,120", "windowingFunction maximum", "bigDataUrl $newFile"),"\n\n";
	}	
}
close(WRTER);
close(WRTDB);
print STDERR "\n\nFinished creating.....................................................................................\n";


