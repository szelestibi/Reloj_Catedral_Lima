#!/bin/bash

clear

scriptname=${0##*/}
progname=${scriptname%.*}

/usr/bin/python ./$progname.py
