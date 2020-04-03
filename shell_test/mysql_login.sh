#!/bin/bash
#pass="cmmbvision"
#mysql -uroot -p$pass -e"select 1;"
#if [ $# -eq 6 ];then
#while [ $# -gt 0 ]
#do
#    echo "第一个$1，参数个数$#"
#    shift
#done
#fi
while [ $# -gt 0 ]
do
case $1 in
    -h)
    echo "输入例如：./mysql_login.sh -m 192.168.10.11 -s 192.168.10.12 -i 192.168.10.13\
            -i 后加i节点ip，-m后加m节点ip，-s 后加s几点ip"

    exit 1
    ;;
    -m)
    fes_m=$2
    shift
    shift
    ;;
    -i)
    fes_i=$2
    shift
    shift
    ;;
    -s)
    fes_s=$2
    shift
    shift
    ;;
    *)
    echo "非法参数，请输入-h查看"
    exit 1
    ;;
esac
done
echo "fes_m="$fes_m
echo "fes_s="$fes_s
echo "fes_i="$fes_i