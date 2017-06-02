#!/usr/bin/perl

#input gene list first, for example: cat CDS.mouse.out.bed  CDS.frog.out.bed  CDS.zebrafish.out.bed  Lat.out.bed  Ola.seq.uniq.out.bed Pma.seq.uniq.out.bed  Tru.seq.uniq.out.bed|cut -f1|sort|uniq > base


$m=0;
open (BASE, "$ARGV[0]") || die $!;
 while($id=<BASE>){
   chomp $id;
     $hash{$id}=$m;
       $matrix[$m][0]=$id;
         $m++;
         }
         close (BASE);

         #===================================
         $n=1;
         while ($n<@ARGV){
            open (INPUT, "$ARGV[$n]") || die $!;
               $line="";
                  while($line=<INPUT>){
                    chomp $line;
                         ($a,$other)=split('\t', $line, 2);
                           $matrix[$hash{$a}][$n]=$other;

                             }
                              $n++
                              }  
                              close (INPUT);

                              for ($x=0;$x<=$m-1;$x++){
                               for ($y=0;$y<=$n-1;$y++){
                                 $matrix[$x][$y]="NULL" if $matrix[$x][$y] eq "";
                                   print "$matrix[$x][$y]\t" if $y<$n-1;
                                     print "$matrix[$x][$y]\n" if $y==$n-1;
                                      }
                                       }
