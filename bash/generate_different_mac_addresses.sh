#!/bin/bash

function log10
{
  if [ -z "$1" ];
  then
    VAL=10
  else
    VAL="$1"
  fi

  CALC="l($VAL)/l(10)"
  RET=$(echo $CALC | bc -l)
  RET=$(echo $RET | awk '{print int($1+0.5)}')
  return $RET
}


if [ -z "$DEBUG" ];
then
  DEBUG=0
else
  case $DEBUG in
    "0"|"1")
      ;;
    "y"|"yes"|"true")
      DEBUG=1
      ;;
    "n"|"no"|"false")
      DEBUG=0
      ;;
    *)
      DEBUG=0
      echo "DEBUG is NOT assigned correctly, used 'false' value in place of the wrong value"
  esac
fi

if [ -z "$DESTDIR" ];
then
  DESTDIR="$HOME"
fi

if [ -d "$DESTDIR" ];
then
  DESTDIR="$DESTDIR/mac_addresses"
  mkdir -p $DESTDIR
  echo "MAC list files is going to be written to $DESTDIR"
else
  echo "$DESTDIR does NOT exist"
  exit 1
fi

if [ -z "$MAC_PREFIX" ];
then
  MAC_PREFIX="00:0C:29"
  echo "I assigned $MAC_PREFIX as a MAC prefix"
else
  size=${#MAC_PREFIX}
  case $size in
    "3"|"5"|"7"|"9")
      echo "I assigned $MAC_PREFIX as a MAC prefix"
      ;;
    *)
      echo "$MAC_PREFIX is NOT correct as a MAC prefix, replacing it with 00:0C:29"
      MAC_PREFIX="00:0C:29"
      ;;
  esac
fi

hexchars="0123456789ABCDEF"
MACSFILE_PREFIX="$DESTDIR/macs0"
if [ -z "$MACS_PER_FILE" ];
then
  MACS_PER_FILE=200
fi

case $MACS_PER_FILE in
  "1")
    echo "I'm going to generate $MACS_PER_FILE different MAC address per file"
    ;;
  *)
    echo "I'm going to generate $MACS_PER_FILE different MAC addresses per file"
    ;;
esac

if [ -z "$NUMBER_OF_FILES" ];
then
  NUMBER_OF_FILES=5
fi
rm -f $MACSFILE_PREFIX*.txt
case $NUMBER_OF_FILES in
  "1")
    echo "I'm going to generate $NUMBER_OF_FILES file"
    ;;
  *)
    echo "I'm going to generate $NUMBER_OF_FILES files"
    ;;
esac

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
          echo "*** FOUND an existing MAC address"
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
log10 $NUMBER_OF_FILES
NOZ=$(($?+1))
PREF=$(printf "$MACSFILE_PREFIX%0$(echo $NOZ)d" $JJ)
MAC_FILENAME="$PREF.txt"
while [ $x -lt $MACS_PER_FILE ] && [ $JJ -le $NUMBER_OF_FILES ];
do
  mac="$MAC_PREFIX$(for i in {1..6}; do echo -n ${hexchars:$(( $RANDOM % 16 )):1} ; done | sed -e 's/\(..\)/:\1/g')"
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
      echo "wrote file n.$JJ: $MAC_FILENAME"
      JJ=$((JJ+1))
      x=0
      PREF=$(printf "$MACSFILE_PREFIX%0$(echo $NOZ)d" $JJ)
      MAC_FILENAME="$PREF.txt"
    fi
  fi
done
