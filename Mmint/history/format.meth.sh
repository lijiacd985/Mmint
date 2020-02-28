#!/bin/bash

args=("$@")

for ((i=0;i<$#;i++))
do
   #echo ${args[$i]}
   #echo ${args[$i]%???}
   #echo `wc -l ${args[$i]%???}`
#   sed "1d" ${args[$i]%???} | awk '{for (i=7;i<=NF;i++) a[i]+=$i}END{for (i=7;i<=NF;i++) printf a[i]/FNR"\t"; printf "\n"}' > ${args[$i]%???}.ave.txt
    sed "1d" ${args[$i]%???} | awk '{for (i=7;i<=NF;i++) if($i!~/nan/)c[i]+=1;for (i=7;i<=NF;i++)if($i!~/nan/)a[i]+=$i}END{for (i=7;i<=NF;i++) printf a[i]/c[i]"\t"; printf "\n"}' >> merge.ave.txt
   #cat ${args[$i]%???}.txt > merge.ave.txt
    sed -i 's/\t$//g' merge.ave.txt
done

#cat *.ave.txt|sed 's/\t$//g' > merge.ave.txt

#for a in args; do sed '1d' ${$a%???} |awk '{for (i=7;i<=NF;i++) a[i]+=$i}END{for (i=7;i<=NF;i++) printf a[i]/26392"\t"; printf "\n"}' > ${$a%???}\.ave;done 

