#!/bin/bash

SHUTDOWN_HOSTS=shutdown_hosts.txt
RETVAL=1

file_not_found() {
  RETVAL=1
  echo "$SHUTDOWN_HOSTS not found!"
}


genkey() {
   ssh-keygen -t rsa -b 4096
   RETVAL=1
}


exchangekey() {
  if [ -f shutdonw_hosts ];
  then
    while read line
    do
      ssh-copy-id root@"$line"
    done < $SHUTDOWN_HOSTS
  else
    file_not_found
  fi
}


setup() {
  genkey
  exchangekey
}


run() {
  if [ -z "$1" ];
  then
    echo "command NOT specified"
    RETVAL=1
  else
    if [ -f shutdonw_hosts ];
    then
      while read line
      do
        ssh root@"$line" "$1"
      done < $SHUTDOWN_HOSTS
    else
      file_not_found
    fi
  fi
}


# See how we were called.
case "$1" in
  setup)
    setup
    ;;
  run)
    run poweroff
    ;;
  *)
    echo "Usage: $0 {setup|run}"
esac

exit $RETVAL
