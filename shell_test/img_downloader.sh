#!/bin/bash
#用途:图片下载工具
#文件名: img_downloader.sh
#未理解清楚
if [ $# -ne 3 ];
then
 echo "Usage: $0 URL -d DIRECTORY"
 exit -1
fi
for i in {1..4}
do
 case $1 in
 -d) shift; directory=$1; shift ;;
 *) url=${url:-$1}; shift;;
 esac
done
mkdir -p $directory;
baseurl=$(echo $url | egrep -o "https?://[a-z.]+")
echo Downloading $url
curl -s $url | egrep -o "<img src=[^>]*>" |
sed 's/<img src=\"\([^"]*\).*/\1/g' > /tmp/$$.list
sed -i "s|^/|$baseurl/|" /tmp/$$.list
cd $directory;
while read filename;
do
 echo Downloading $filename
 curl -s -O "$filename" --silent
done < /tmp/$$.list