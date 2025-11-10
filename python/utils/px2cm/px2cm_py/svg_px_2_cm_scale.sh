#!/bin/bash

#set -x

shellxname=${0##*/}
scriptname=${shellxname%.*}

/usr/bin/python $scriptname.py ./HRS.svg ./HRS_cm.svg
/usr/bin/python $scriptname.py ./MNS.svg ./MNS_cm.svg

#set +x
