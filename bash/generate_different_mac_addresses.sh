#!/bin/bash

hexchars="0123456789ABCDEF"
MACSFILE_PREFIX="$HOME/macs0"
if [ -z "$MACS_PER_FILE" ];
then
  MACS_PER_FILE=200
fi

if [ -z "$NUMBER_OF_FILES" ];
then
  NUMBER_OF_FILES=5
fi
rm -f $MACSFILE_PREFIX?.txt

if [ -z "$DEBUG" ];
then
  DEBUG=0
fi

function isInFile
{
  if [ -z "$1" ];
  then
    echo "*** ERROR: no input MAC address"
    exit 1
  fi

  II=1
  while [ $II -le $NUMBER_OF_FILES ];
  do
    FILENAME="$MACSFILE_PREFIX$II.txt"
    if [ -f $FILENAME ];
    then
      while read line
      do
        if [ "z$1" == "z$lilne" ];
        then
          if [ $DEBUG -eq 1 ];
          then
            echo "*** FOUND an existing MAC address: $1"
          fi
          return 1
        fi
      done < $FILENAME
    else
      return 0
    fi
    II=$((II+1))
  done
  return 0
}
export -f isInFile

x=0
JJ=1
MAC_FILENAME="$MACSFILE_PREFIX$JJ.txt"
while [ $x -lt $MACS_PER_FILE ] && [ $JJ -le $NUMBER_OF_FILES ];
do
  mac="00:0C:29$(for i in {1..6}; do echo -n ${hexchars:$(( $RANDOM % 16 )):1} ; done | sed -e 's/\(..\)/:\1/g')"
  isInFile $mac
  if [ $? -eq 0 ];
  then
    echo "$mac" >> $MAC_FILENAME
    x=$((x+1))
    if [ $DEBUG -eq 1 ];
    then
      echo "$x: $mac"
    fi
    if [ $x -eq $MACS_PER_FILE ];
    then
      echo "... wrote $MAC_FILENAME file"
      JJ=$((JJ+1))
      x=0
      MAC_FILENAME="$MACSFILE_PREFIX$JJ.txt"
    fi
  fi
done
