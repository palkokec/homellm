#!/usr/bin/env bash
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )" 
. $SCRIPTPATH/bin/activate

python3 $SCRIPTPATH/main.py $1