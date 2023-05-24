#!/bin/bash
ADMIN_NET1=127.0.0.1/8
ADMIN_NET2=192.168.0.209/32

DEFAULT_OU=ACCEPT
DEFAULT_FO=ACCEPT
DEFAULT_IN=ACCEPT
IPTABLES="/sbin/iptables -t filter"

echo "configuring firewall"
echo "setting chans empty..."
for TABLE in filter nat mangle ; do
  $IPTABLES -t $TABLE -F
  $IPTABLES -t $TABLE -X
done

echo "setting to ACCEPT as the firewall default policy..."
$IPTABLES -P FORWARD $DEFAULT_FO
$IPTABLES -P OUTPUT  $DEFAULT_OU
$IPTABLES -P INPUT   $DEFAULT_IN
echo "   FORWARD  -->  $DEFAULT_FO"
echo "   OUTPUT   -->  $DEFAULT_OU"
echo "   INPUT    -->  $DEFAULT_IN"
