#!/bin/bash

args=("$@")

cut -f 1,2,3 ${args[0]} > colname
for((i=0;i<$#;i++))
    do
       cut -f 4 ${args[$i]} > ${args[$i]}.clean
    done
rm merge.clean
paste colname *.clean |sed 's/\t$//g'| sed 's/\t\t/\t/g' > merge.clean

#for a in args; do sed '1d' ${$a%???} |awk '{for (i=7;i<=NF;i++) a[i]+=$i}END{for (i=7;i<=NF;i++) printf a[i]/26392"\t"; printf "\n"}' > ${$a%???}\.ave;done 

