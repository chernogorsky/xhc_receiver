#!/bin/bash

trap ctrl_c INT

function ctrl_c() {
        echo "** Trapped CTRL-C"
	exit 1
}

COUNTER=0; 
while true; do 
    ./main.py; 
    echo $COUNTER; 
    let COUNTER=COUNTER+1; 
done
