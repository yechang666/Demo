#!/bin/bash

#文件名：success_test.sh
CMD="command"
$CMD
if [ $? -eq 0 ];
then
    echo "$CMD executed successfully"
else
    echo "$CMD terminated unsuccessfully"
fi