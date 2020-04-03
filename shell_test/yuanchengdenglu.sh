#!/bin/bash
/usr/bin/expect << EOF
set timeout 5
spawn ssh root@192.168.10.220
expect "*password:"
send "123456\r"
EOF
cd /opt/rh
mkdir temp
cd temp
wget  ftp://192.168.10.27/fes-dependence/jre-8u121-linux-x64.rpm --ftp-user=jekins --ftp-password=jekins
rpm -ivh jre-8u121-linux-x64.rpm
rm -rf ../temp