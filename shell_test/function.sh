#!/bin/bash
function f_name()
{
    echo "*****************"
    echo $1 $2
    echo "$@"
    echo "$*"


}

f_name c n m cm ;
f_name commmm