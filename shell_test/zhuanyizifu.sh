#!/bin/bash
#echo  "\n"
#echo "\""
#echo "\."
#echo '\n'
#echo '\"'
#echo '\'\'
#echo '\'
#echo  "1\nhello\n"
#echo "\'"
#echo "abc\'abc"
#echo \n
#echo "\\"
ls -lS --time-style=long-iso | awk 'BEGIN { getline; getline; name1=$8; size=$5; print name1,size}'