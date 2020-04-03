#!/bin/bash
cd /opt/rh/temp
wget  ftp://192.168.10.27/fes-dependence/*.rpm --ftp-user=jekins --ftp-password=jekins
#wget -b -c -q ftp://192.168.10.27/fes-dependence/*.rpm --ftp-user=jekins --ftp-password=jekins #-q不打印日志，-c断点续传 -b 后台下载
#while true
#do
#    result=$(du -sh /opt/rh/temp/|cut -f 1)
#    if [ "$result" = "256M" ]; then
#    echo "copy success"
#    break;
#    else
#    sleep 2
#    echo "等待中...."
#    fi
#done
rpm -ivh jre-8u121-linux-x64.rpm
old_mysql_version=$(rpm -qa |grep mysql)
rpm -e $old_mysql_version --nodeps
rpm -ivh MySQL-server-5.6.35-1.linux_glibc2.5.x86_64.rpm
rpm -ivh MySQL-client-5.6.35-1.linux_glibc2.5.x86_64.rpm
service mysql start
#password1=$(cat /root/.mysql_secret |cut -d " " -f 18)
password1=$(cat /root/.mysql_secret |cut -d : -f 4)
#export MYSQL_PWD=$password1
mysql -uroot -p$password1 -e"
set password=password('cmmbvision');
quit" --connect-expired-password
chkconfig mysql on
rpm -ivh erlang-19.0.4-1.el6.x86_64.rpm
rpm -ivh socat-1.7.1.3-1.el6.rf.x86_64.rpm
rpm -ivh rabbitmq-server-3.6.10-1.el6.noarch.rpm
chkconfig rabbitmq-server on
cd /usr/lib/rabbitmq/bin
rabbitmq-plugins enable rabbitmq_management
service rabbitmq-server restart
sleep 20
rabbitmqctl add_user admin 12345
rabbitmqctl set_user_tags admin administrator
rabbitmqctl set_permissions -p "/" admin ".*" ".*" ".*"
iptables -I INPUT -p tcp --dport 5672 -j ACCEPT
iptables -I INPUT -p tcp --dport 15672 -j ACCEPT
cd /opt/rh/
rm -rf temp
