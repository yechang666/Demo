#!/bin/bash
#统一端口号
swhls=10080           						#由hls_port来代替这个值
swserver=10081
fesservice=10082
monservice=10083
fesmonitor=10084
forwarder=10085
fesagent=10086
bfpscheduler_info=10087
bfpscheduler_worker=10088
bfpsymbol=10089
fesconsole=10090
logserver=10091


mq_port=5672
rsyn_port=873
mysql_port=3306




#test
echo $BUILD_USER
echo $BUILD_USER_FIRST_NAME
echo $BUILD_USER_LAST_NAME
echo $BUILD_USER_ID
echo $BUILD_USER_EMAIL


###############################################################################################################
#配置fes-i node

cd $latest_folder/fes-i/conf/


#distributor-site
sed -i "s/^\(.*\)hosts allow = .*$/\1hosts allow = $fes_s_ip/g" rsyncd.conf


#fesagent
sed -i "s/^node_name=.*$/node_name=i-node1/g" fesagent.conf
sed -i "s/^node_ip=.\+$/node_ip=$fes_i_ip/g" fesagent.conf
sed -i "s/^listen_port=[0-9]\+$/listen_port=$fesagent/g" fesagent.conf
sed -i "s/^mq_server_ip=.\+$/mq_server_ip=$fes_m_ip/g" fesagent.conf
sed -i "s/^mq_server_port=[0-9]\+$/mq_server_port=$mq_port/g" fesagent.conf
sed -i "s/^esg_server_ip=.\+$/esg_server_ip=$fes_m_ip/g" fesagent.conf
sed -i "s/^esg_server_port=[0-9]\+$/esg_server_port=$fesservice/g" fesagent.conf


#swhls
sed -i "s/^.*listen.*[0-9]\+;$/\tlisten $hls_port;/g" nginx-swhls.conf

if [ "$port_in_redirect" != "Off" ];then
   sed -i "s/^\(.*\)port_in_redirect off;$/\1#port_in_redirect off;/g" nginx-swhls.conf
else
   sed -i "s/^\(.*\)port_in_redirect off;$/\tport_in_redirect off;/g" nginx-swhls.conf
fi

sed -i "s/^\(.*\)proxy_pass http:\/\/[0-9\.]\+:[0-9]\+\/fesconsole\/;$/\1proxy_pass http:\/\/$fes_m_ip:$fesconsole\/fesconsole\/;/g" nginx-swhls.conf

sed -i "s/^\(.*\)proxy_pass http:\/\/[0-9\.]\+:[0-9]\+\/v1;$/\1proxy_pass http:\/\/$fes_i_ip:$swserver\/v1;/g" nginx-swhls.conf
sed -i "s/^\(.*\)proxy_pass http:\/\/[0-9\.]\+:[0-9]\+\/v1\/raptor\/;$/\1proxy_pass http:\/\/$fes_i_ip:$bfpsymbol\/v1\/raptor\/;/g" nginx-swhls.conf
sed -i "s/^\(.*\)proxy_pass http:\/\/[0-9\.]\+:[0-9]\+\/bfp\/info;$/\1proxy_pass http:\/\/$fes_m_ip:$bfpscheduler_info\/bfp\/info;/g" nginx-swhls.conf


#swserver
sed -i "s/^server\.port=[0-9]\+$/server.port=$swserver/g" swserver.properties
sed -i "s/^server\.address=.\+$/server.address=0.0.0.0/g" swserver.properties

sed -i "s/^fesservices.server.port=[0-9]\+$/fesservices.server.port=$fesservice/g" swserver.properties
sed -i "s/^fesservices.server.address=.\+$/fesservices.server.address=$fes_m_ip/g" swserver.properties

sed -i "s/^web.resource.url=.*$/web.resource.url=http:\/\/${hls_domain_name}:${hls_port}\/resources/g" swserver.properties
sed -i "s/^user.portrait.image-path=.*$/user.portrait.image-path=..\/run\/web\/resources/g" swserver.properties


 sed -i "s/^spring\.datasource\.url=jdbc:mysql:\/\/.*:[0-9]*/spring\.datasource\.url=jdbc:mysql:\/\/$fes_m_ip:$mysql_port/g" swserver.properties
sed -i "s/^spring.datasource.username=.*$/spring.datasource.username=silkwave/g" swserver.properties
sed -i "s/^spring.datasource.password=.*$/spring.datasource.password=ggzbtech/g" swserver.properties

sed -i "s/^spring\.rabbitmq\.host=.*$/spring\.rabbitmq\.host=$fes_m_ip/g" swserver.properties
sed -i "s/^spring\.rabbitmq\.port=.*$/spring\.rabbitmq\.port=$mq_port/g" swserver.properties



    #CSServer update
    sed -i "s/^csserver.apk.url=.*$/csserver.apk.url=http:\/\/${hls_domain_name}:${hls_port}\/update\/csserver\/csserver.apk/g" swserver.properties
    sed -i "s/^csserver.apk.file.location=.*$/csserver.apk.file.location=\/opt\/fes\/run\/web\/update\/csserver\/csserver.apk/g" swserver.properties

    sed -i "s/^csserver.rom.url=.*$/csserver.rom.url=http:\/\/${hls_domain_name}:${hls_port}\/update\/mbox\/mbox_ota.zip/g" swserver.properties
    sed -i "s/^csserver.rom.file.location=.*$/csserver.rom.file.location=\/opt\/fes\/run\/web\/update\/mbox\/mbox_ota.zip/g" swserver.properties

    sed -i "s/^csserver.wifi-portal.url=.*$/csserver.wifi-portal.url=http:\/\/${hls_domain_name}:${hls_port}\/update\/wifi\/wifi_portal.zip/g" swserver.properties
    sed -i "s/^csserver.wifi-portal.file.location=.*$/csserver.wifi-portal.file.location=\/opt\/fes\/run\/web\/update\/wifi\/wifi_portal.zip/g" swserver.properties


    #App update
    sed -i "s/^app.android.mobile.url=.*$/app.android.mobile.url=http:\/\/${hls_domain_name}:${hls_port}\/update\/mobile\/silkwave.apk/g" swserver.properties
    sed -i "s/^app.android.mobile.file.location=.*$/app.android.mobile.file.location=\/opt\/fes\/run\/web\/update\/mobile\/silkwave.apk/g" swserver.properties

    sed -i "s/^app.android.vehicle.url=.*$/app.android.vehicle.url=http:\/\/${hls_domain_name}:${hls_port}\/update\/vehicle\/silkwave.apk/g" swserver.properties
    sed -i "s/^app.android.vehicle.file.location=.*$/app.android.vehicle.file.location=\/opt\/fes\/run\/web\/update\/vehicle\/silkwave.apk/g" swserver.properties

    sed -i "s/^app.appstore.url=.*$/app.appstore.url=http:\/\/${hls_domain_name}:${hls_port}\/update\/mobile\/silkwave.apk/g" swserver.properties


#bfpsymbol
cd $latest_folder/fes-i/conf/bfpserver
rm -f bfpsymbol.json
rm -f bfpsymbol.properties
wget ftp://$FTP_SERVER/TestResources/bfpstreams/bfpsymbol.properties --ftp-user=$FTP_SERVER_USER --ftp-password=$FTP_SERVER_PWD
wget ftp://$FTP_SERVER/TestResources/bfpstreams/bfpsymbol.json --ftp-user=$FTP_SERVER_USER --ftp-password=$FTP_SERVER_PWD

sed -i "s/^server.port=[0-9]\+$/server.port=$bfpsymbol/g" bfpsymbol.properties
sed -i "s/^server.address=.\+$/server.address=0.0.0.0/g" bfpsymbol.properties





###############################################################################################################
#配置fes-s node

cd $latest_folder/fes-s/conf/

#distributor-site


#fesagent
sed -i "s/^node_name=.*$/node_name=s-node1/g" fesagent.conf
sed -i "s/^node_ip=.\+$/node_ip=$fes_s_ip/g" fesagent.conf
sed -i "s/^listen_port=[0-9]\+$/listen_port=$fesagent/g" fesagent.conf
sed -i "s/^mq_server_ip=.\+$/mq_server_ip=$fes_m_ip/g" fesagent.conf
sed -i "s/^mq_server_port=[0-9]\+$/mq_server_port=$mq_port/g" fesagent.conf
sed -i "s/^esg_server_ip=.\+$/esg_server_ip=$fes_m_ip/g" fesagent.conf
sed -i "s/^esg_server_port=[0-9]\+$/esg_server_port=$fesservice/g" fesagent.conf


#segmenter
sed -i "s/^node_name=.*$/node_name=s-node1/g" segmenter.conf
sed -i "s/^mq_server_ip=.\+$/mq_server_ip=$fes_m_ip/g" segmenter.conf
sed -i "s/^mq_server_port=[0-9]\+$/mq_server_port=$mq_port/g" segmenter.conf
sed -i "s/^esg_server_port=[0-9]\+$/esg_server_port=$fesservice/g" segmenter.conf
sed -i "s/^esg_server_ip=.\+$/esg_server_ip=$fes_m_ip/g" segmenter.conf
sed -i "s/^drm_server_ip=.\+$/drm_server_ip=$drm_server_ip/g" segmenter.conf

sed -i "s/^cache_num=[0-9]\+$/cache_num=$segmenter_cache_num/g" segmenter.conf
sed -i "s/^file_num=[0-9]\+$/file_num=$segmenter_file_num/g" segmenter.conf
sed -i "s/^delay_time=[0-9]\+$/delay_time=$segmenter_delay/g" segmenter.conf


#scheduler
sed -i "s/^node_name=.*$/node_name=s-node1/g" scheduler.conf
sed -i "s/^mq_server_ip=.\+$/mq_server_ip=$fes_m_ip/g" scheduler.conf
sed -i "s/^mq_server_port=[0-9]\+$/mq_server_port=$mq_port/g" scheduler.conf
sed -i "s/^esg_server_ip=.\+$/esg_server_ip=$fes_m_ip/g" scheduler.conf
sed -i "s/^esg_server_port=[0-9]\+$/esg_server_port=$fesservice/g" scheduler.conf
sed -i "s/^mux_ip=.\+$/mux_ip=$mux_ip/g" scheduler.conf
sed -i "s/^mux_port=.\+$/mux_port=$mux_port/g" scheduler.conf
sed -i "s/^log_server_ip=.\+$/log_server_ip=$fes_l_ip/g" scheduler.conf
sed -i "s/^log_server_port=[0-9]\+$/log_server_port=$logserver/g" scheduler.conf


#forwarder
sed -i "s/^node_name=.*$/node_name=s-node1/g" forwarder.conf
sed -i "s/^mq_server_ip=.\+$/mq_server_ip=$fes_m_ip/g" forwarder.conf
sed -i "s/^mq_server_port=[0-9]\+$/mq_server_port=$mq_port/g" forwarder.conf
sed -i "s/^data_listen_port=[0-9]\+$/data_listen_port=$forwarder/g" forwarder.conf
sed -i "s/^esg_server_ip=.\+$/esg_server_ip=$fes_m_ip/g" forwarder.conf
sed -i "s/^esg_server_port=[0-9]\+$/esg_server_port=$fesservice/g" forwarder.conf




#bfpworker
cd $latest_folder/fes-s/conf/bfpserver
rm -f bfpworker.json
wget ftp://$FTP_SERVER/TestResources/bfpstreams/bfpworker.json --ftp-user=$FTP_SERVER_USER --ftp-password=$FTP_SERVER_PWD


wget ftp://${FTP_SERVER}/TestResources/Script/modify-json.py --ftp-user=$FTP_SERVER_USER --ftp-password=$FTP_SERVER_PWD

python modify-json.py -f bfpworker.json -p /ser_ip -v "$fes_m_ip"
python modify-json.py -f bfpworker.json -p /ser_port -v $bfpscheduler_worker

rm -rf modify-json.py





###############################################################################################################

#配置fes-m node

cd $latest_folder/fes-m/conf/

#fesagent
sed -i "s/^node_name=.*$/node_name=m-node1/g" fesagent.conf
sed -i "s/^node_ip=.\+$/node_ip=$fes_m_ip/g" fesagent.conf
sed -i "s/^listen_port=[0-9]\+$/listen_port=$fesagent/g" fesagent.conf
sed -i "s/^mq_server_ip=.\+$/mq_server_ip=$fes_m_ip/g" fesagent.conf
sed -i "s/^mq_server_port=[0-9]\+$/mq_server_port=$mq_port/g" fesagent.conf
sed -i "s/^esg_server_ip=.\+$/esg_server_ip=$fes_m_ip/g" fesagent.conf
sed -i "s/^esg_server_port=[0-9]\+$/esg_server_port=$fesservice/g" fesagent.conf



#fesconsole
sed -i "s/^server\.port=[0-9]\+$/server\.port=$fesconsole/g" fesconsole.properties
sed -i "s/^server\.address=.\+$/server\.address=0.0.0.0/g" fesconsole.properties

sed -i "s/^spring\.rabbitmq\.host=.\+$/spring\.rabbitmq\.host=$fes_m_ip/g" fesconsole.properties
sed -i "s/^spring\.rabbitmq\.port=[0-9]\+$/spring\.rabbitmq\.port=$mq_port/g" fesconsole.properties

sed -i "s/^fesservices\.server\.address=.\+$/fesservices\.server\.address=$fes_m_ip/g" fesconsole.properties
sed -i "s/^fesservices\.server\.port=[0-9]\+$/fesservices\.server\.port=$fesservice/g" fesconsole.properties


#fesservice
sed -i "s/^server\.port=[0-9]\+$/server.port=$fesservice/g" fesservices.properties
sed -i "s/^server\.address=.\+$/server.address=0.0.0.0/g" fesservices.properties

sed -i "s/^bfp.server.address=.\+$/bfp.server.address=$fes_m_ip/g" fesservices.properties
sed -i "s/^bfp.server.port=[0-9]\+$/bfp.server.port=$bfpscheduler_info/g" fesservices.properties

sed -i "s/^esg.file.location=.*\.json$/esg.file.location=..\/run\/esg\/0.json/g" fesservices.properties
sed -i "s/^tag.file.location=.*\.json$/tag.file.location=..\/conf\/tag.json/g" fesservices.properties
sed -i "s/^encoder.file.location=.*\.json$/encoder.file.location=..\/conf\/info.json/g" fesservices.properties

sed -i "s/^spring\.rabbitmq\.host=.*$/spring\.rabbitmq\.host=$fes_m_ip/g" fesservices.properties
sed -i "s/^spring\.rabbitmq\.port=.*$/spring\.rabbitmq\.port=$mq_port/g" fesservices.properties





#bfpscheduler
#download bfp configure files
cd $latest_folder/fes-m/conf/bfpserver
rm -f bfpscheduler.json
wget ftp://$FTP_SERVER/TestResources/bfpstreams/bfpscheduler.json --ftp-user=$FTP_SERVER_USER --ftp-password=$FTP_SERVER_PWD


wget ftp://${FTP_SERVER}/TestResources/Script/modify-json.py --ftp-user=$FTP_SERVER_USER --ftp-password=$FTP_SERVER_PWD

python modify-json.py -f bfpscheduler.json -p /web_server/port -v $bfpscheduler_info
python modify-json.py -f bfpscheduler.json -p /bfpworker_server/port -v $bfpscheduler_worker

rm -rf modify-json.py






#生成tar包
cd $latest_folder/

if [ "$is_release" != "true" ]; then

data=$(date +%Y-%m-%d)

  fesi_name="fesi-$fes_version-$data-$today_build_times"
  fess_name="fess-$fes_version-$data-$today_build_times"
  fesm_name="fesm-$fes_version-$data-$today_build_times"


  #reuse latest_folder to maintain the link where the customer can get this package.
  latest_folder="http://${FTP_SERVER}/fes/fes_testing/${fes_version}/latest/"

else


  #对于相同的版本，累积rc号

  if [ -e rc_number ]; then
  	rc=$(cat rc_number)
    let rc=rc+1
    echo $rc > rc_number

  else
  	rc=1
    echo $rc > rc_number

  fi


  fesi_name="fesi-${fes_version}rc$rc"
  fess_name="fess-${fes_version}rc$rc"
  fesm_name="fesm-${fes_version}rc$rc"

  latest_folder="http://${FTP_SERVER}/fes/fes_release/${fes_version}/${hls_domain_name}/"

fi



mv fes-i $fesi_name
mv fes-s $fess_name
mv fes-m $fesm_name
tar -czvf $fesi_name.tar.gz ./$fesi_name/
tar -czvf $fess_name.tar.gz ./$fess_name/
tar -czvf $fesm_name.tar.gz ./$fesm_name/


#delete the useless files
rm -rf $fesi_name
rm -rf $fess_name
rm -rf $fesm_name


#anounce that the latest build is ready for use
rm -f *.txt




#export the download path
cd $WORKSPACE
echo download_link=$latest_folder > czguo_var
echo build_user=$BUILD_USER_EMAIL >> czguo_var