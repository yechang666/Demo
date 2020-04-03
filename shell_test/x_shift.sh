#!/bin/bash
#while [ $# -gt 0 ]
#do
#    echo "第一个参数：$1 参数个数：$#"
#    shift
#done
#for i in {1..4}
echo $@
echo $*
while [ $# -gt 0 ]
do
 case $1 in
 -d) shift; directory=$1; echo $directory; shift ;;
 *) url=${url:-$1}; echo $url; shift;;
# *) url=$1; echo $url; shift;;
 esac
done