#!/bin/bash
cd /opt/rh/temp
wget  ftp://192.168.10.27/fes-dependence/jre-8u121-linux-x64.rpm --ftp-user=jekins --ftp-password=jekins
rpm -ivh jre-8u121-linux-x64.rpm
rm -rf ../temp