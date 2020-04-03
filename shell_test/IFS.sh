#!/bin/bash
#data="name,sex,rollno,location"
#oldIFS=$IFS
#IFS=,
#for VAR in $data ; do
#    echo Item: $VAR
#done
#IFS=$oldIFS
#line="root:x:0:0:root:/root:/bin/bash"
#oldIFS=$IFS
#IFS=:
#count=0
#for item in $line ; do
#    [ $count -eq 0 ] && user=$item
#    [ $count -eq 6 ] && shell=$item
#    let count++
#done
#IFS=$oldIFS
#echo $user \'s shell is $shell
#
#for i in {a..z}; do echo $i; done;
str1="Not empty "
str2="Not empty "
#if [[ -n $str1 ]] && [[ -z $str2 ]];
#then
# echo str1 is nonempty and str2 is empty string.
#fi

#if [[ -n $str1 ]] && [[ -z $str2 ]];
#then
#    echo "True"
#fi
var=2
#if test $var -eq 2
#then
#    echo "True"
#fi
if (($var<3)); then
    echo "True"
fi