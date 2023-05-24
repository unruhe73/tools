#!/bin/bash

# you can clean any USB storage you mounted under Mac OS mounting on Linux under a directory and then running this script
# of course you must be root user

if [ -z "$1" ];
then
  echo "*** ERROR: you must specify the directory to clean as parameter..."
  exit 1
else
  if [ ! -d "$1" ];
  then
    echo "*** ERROR: you must specify a directory..."
    exit 2
  fi
fi

rm -fv $(find "$1" -name .DS_Store)
rm -fv $(find "$1" -name ._*)
rm -rfv $(find "$1" -name .fseventsd)
rm -rfv $(find "$1" -name .Trash-1000)
rm -rfv $(find "$1" -name .Trashes)
