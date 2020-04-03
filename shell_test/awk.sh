#!/bin/bash

#awk '{getline cmdout;print cmdout}' args.txt
#cat  args.txt |awk '{getline cmdout ; print cmdout}'
#aa=`cat args.txt`
#for VAR in `cat args.txt` ; do
#    echo $VAR
#done
#cat sshd.txt |awk '{for(i=1;i<=NF;i++){ print $i}}'

#echo"" | awk '
#BEGIN {
#    a[1]="123"
#    a[2]="456"
#    a[3]="789"
#}
#END{
#    for(i in a) {
#        print i,a[i]
#    }
#}'
#cat sshd.txt |awk '{for(i=1;i<=NF;i++){print $i}}'
echo "`./word_freq.sh sshd.txt`"