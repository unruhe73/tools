#!/bin/bash

# suppose you want let only your host access to a server: specify your host IP into ADMIN_NET2
ADMIN_NET1=127.0.0.1/8
ADMIN_NET2=192.168.0.209/32

DEFAULT_OU=DROP
DEFAULT_FO=DROP
DEFAULT_IN=DROP
IPTABLES="/sbin/iptables -t filter"

echo "configuring firewall"
echo "setting chains empty..."
for TABLE in filter nat mangle ; do
  $IPTABLES -t $TABLE -F
  $IPTABLES -t $TABLE -X
done

echo "setting to DROP as the firewall default policy..."
$IPTABLES -P FORWARD $DEFAULT_FO
$IPTABLES -P OUTPUT  $DEFAULT_OU
$IPTABLES -P INPUT   $DEFAULT_IN
echo "   FORWARD  -->  $DEFAULT_FO"
echo "   OUTPUT   -->  $DEFAULT_OU"
echo "   INPUT    -->  $DEFAULT_IN"

echo "enabling (ACCEPT) localhost $ADMIN_NET1"
$IPTABLES -A INPUT -s $ADMIN_NET1   -j ACCEPT
$IPTABLES -A OUTPUT -d $ADMIN_NET1  -j ACCEPT
$IPTABLES -A FORWARD -s $ADMIN_NET1 -j ACCEPT
$IPTABLES -A FORWARD -d $ADMIN_NET1 -j ACCEPT

echo "enabling host: the only host can access (ACCEPT) here is $ADMIN_NET2"
$IPTABLES -A INPUT -s $ADMIN_NET2   -j ACCEPT
$IPTABLES -A OUTPUT -d $ADMIN_NET2  -j ACCEPT
$IPTABLES -A FORWARD -s $ADMIN_NET2 -j ACCEPT
$IPTABLES -A FORWARD -d $ADMIN_NET2 -j ACCEPT
