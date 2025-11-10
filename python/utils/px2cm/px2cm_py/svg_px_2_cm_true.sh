#!/bin/bash

#set -x

shellxname=${0##*/}
scriptname=${shellxname%.*}

/usr/bin/python $scriptname.py --dpi 90 ./HRS.svg ./HRS_cm.svg
/usr/bin/python $scriptname.py --dpi 90 ./MNS.svg ./MNS_cm.svg

#set +x
