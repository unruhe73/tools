#!/bin/bash
BASE_IP="192.168.0"
i=1
while [ $i -lt 255 ];
do
  ping -c 1 -W1 $BASE_IP.$i 1>/dev/null 2>/dev/null
  if [ $? -eq 0 ];
  then
    echo "$BASE_IP.$i reachable"
  fi
  i=$((i+1))
done
