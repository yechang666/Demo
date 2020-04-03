#!/bin/bash
if [ $# -ne 1 ];
then
    echo "Usage:$0 filename";
    exit -1
fi

filename=$1
egrep -o "\b[[:alpha:]]+\b" $filename |
awk '{ count[$0]++ }
END{ printf("%-14s%s\n","Word","Count") ;
for(ind in count)
{ printf("%-14s%d\n",ind,count[ind]) |"sort  -k2nr  -k1";} #
}'
#sort -k2nr -k1 解释：根据第二列按照数字降序排列 要是相等用第一列升序排列