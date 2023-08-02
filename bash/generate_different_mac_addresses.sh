#!/bin/bash

DEFAULT_MAC_PREFIX="00:0C:29"

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


function checkMAC
{
  if [ -z "$1" ];
  then
    echo "* MAC prefix NOT assigned, using the default one: $DEFAULT_MAC_PREFIX"
    MAC_PREFIX=$DEFAULT_MAC_PREFIX
  fi
  MAC_PREFIX_SIZE=${#MAC_PREFIX}
  if [ -z "$MACS_PER_FILE" ];
  then
    MACS_PER_FILE=200
  fi

  case $MAC_PREFIX_SIZE in
    "2")
      TOTAL_POSSIBLE_MAC_ADDRESSES=$((256**5))
      echo "* I assigned $MAC_PREFIX as a MAC prefix, if you want a different one assign the MAC_PREFIX variable"
      ;;
    "5")
      TOTAL_POSSIBLE_MAC_ADDRESSES=$((256**4))
      echo "* I assigned $MAC_PREFIX as a MAC prefix, if you want a different one assign the MAC_PREFIX variable"
      ;;
    "8")
      TOTAL_POSSIBLE_MAC_ADDRESSES=$((256**3))
      echo "* I assigned $MAC_PREFIX as a MAC prefix, if you want a different one assign the MAC_PREFIX variable"
      ;;
    "11")
      TOTAL_POSSIBLE_MAC_ADDRESSES=$((256**2))
      echo "* I assigned $MAC_PREFIX as a MAC prefix, if you want a different one assign the MAC_PREFIX variable"
      ;;
    "14")
      TOTAL_POSSIBLE_MAC_ADDRESSES=$((256**1))
      echo "* I assigned $MAC_PREFIX as a MAC prefix, if you want a different one assign the MAC_PREFIX variable"
      ;;
    *)
      echo "* $MAC_PREFIX is NOT correct as a MAC prefix, replacing it with $DEFAULT_MAC_PREFIX"
      TOTAL_POSSIBLE_MAC_ADDRESSES=$((256**3))
      MAC_PREFIX=$DEFAULT_MAC_PREFIX
      ;;
  esac
  MAXIMUM_NUMBER_OF_FILES=$((TOTAL_POSSIBLE_MAC_ADDRESSES/MACS_PER_FILE))
}


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

checkMAC $MAC_PREFIX

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
  echo "* MAC list files is going to be written to $DESTDIR directory"
else
  echo "$DESTDIR does NOT exist"
  exit 1
fi

MACSFILE_PREFIX="$DESTDIR/macs0"
case $MACS_PER_FILE in
  "1")
    echo "* I'm going to generate $MACS_PER_FILE different MAC address per file, if you want a different value assign MACS_PER_FILE variable"
    ;;
  *)
    echo "* I'm going to generate $MACS_PER_FILE different MAC addresses per file, if you want a different value assign MACS_PER_FILE variable"
    ;;
esac

if [ -z "$NUMBER_OF_FILES" ];
then
  echo "* NUMBER_OF_FILES varibale is not assigned, so I set it to 5, if you prefer a different value assign it"
  NUMBER_OF_FILES=5
fi
if [ $NUMBER_OF_FILES -gt $MAXIMUM_NUMBER_OF_FILES ];
then
  NUMBER_OF_FILES=$MAXIMUM_NUMBER_OF_FILES
fi

TOTAL_POSSIBLE_MAC_ADDRESSES=$((MACS_PER_FILE*NUMBER_OF_FILES))
rm -f $MACSFILE_PREFIX*.txt
case $NUMBER_OF_FILES in
  "1")
    echo "* I'm going to generate $NUMBER_OF_FILES file"
    ;;
  *)
    echo "* I'm going to generate $NUMBER_OF_FILES files"
    ;;
esac

echo "* The total possible MAC addresses are: $TOTAL_POSSIBLE_MAC_ADDRESSES"
echo "* I'm going to give you $((NUMBER_OF_FILES*MACS_PER_FILE)) MAC addresses"
if [ $((NUMBER_OF_FILES*MACS_PER_FILE)) -gt $TOTAL_POSSIBLE_MAC_ADDRESSES ];
then
  echo "sorry, but I can't produce all the wanted MAC addresses using files and item per files as you wish"
  exit 1
fi

x=0
JJ=1
log10 $NUMBER_OF_FILES
NOZ=$(($?+1))
PREF=$(printf "$MACSFILE_PREFIX%0$(echo $NOZ)d" $JJ)
MAC_FILENAME="$PREF.txt"
while [ $x -lt $MACS_PER_FILE ] && [ $JJ -le $NUMBER_OF_FILES ];
do
  case $MAC_PREFIX_SIZE in
    "2")
      mac=$(printf "$MAC_PREFIX:%02x:%02x:%02x:%02x:%02x" $(($RANDOM % 256)) $(($RANDOM % 256)) $(($RANDOM % 256)) $(($RANDOM % 256)) $(($RANDOM % 256)))
      ;;
    "5")
      mac=$(printf "$MAC_PREFIX:%02x:%02x:%02x:%02x" $(($RANDOM % 256)) $(($RANDOM % 256)) $(($RANDOM % 256)) $(($RANDOM % 256)))
      ;;
    "8")
      mac=$(printf "$MAC_PREFIX:%02x:%02x:%02x" $(($RANDOM % 256)) $(($RANDOM % 256)) $(($RANDOM % 256)))
      ;;
    "11")
      mac=$(printf "$MAC_PREFIX:%02x:%02x" $(($RANDOM % 256)) $(($RANDOM % 256)))
      ;;
    "14")
      mac=$(printf "$MAC_PREFIX:%02x" $(($RANDOM % 256)))
      ;;
  esac
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
