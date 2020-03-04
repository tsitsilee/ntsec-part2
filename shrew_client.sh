#!/bin/bash 


rto=0.9
echo running iperf-client
while true; do
	iperf -c $1 -u -b 5M -t 0.5 &
	echo $rto
	sleep $rto
done
#TODO: add your code
