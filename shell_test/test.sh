#!/bin/bash
#if [[ "up" = "up" && "up" = "up" ]];then
#echo "up"
#fi
#
#if [ "up" = "up" ] && [[ "up" = "up" ]];
#then
#echo "up"
#fi
##vard="eee"
#var="ddd"
#
#if [[ 2 > 3 ]]; then
#echo 2
#fi
#pp=ab
#a23=aa
##_ab=ab
#if [ ${_ab}x == "ab"x ]; then
#    echo "you had enter ab"
#elif [ $12 == "cd"2 ]; then
#    echo "you had enter cd"
#else
#    echo "you had enter unexpected word"
#fi
#var="cc"
#if [[ -n $var ]];
#var=args.txt
ip_list=$(egrep -o "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+" $1 | sort -nk4| uniq)
echo $ip_list