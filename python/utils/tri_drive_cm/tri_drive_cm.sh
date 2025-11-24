#!/bin/bash

#set -x

shellxname=${0##*/}
scriptname=${shellxname%.*}

/usr/bin/python $scriptname.py

#set +x
