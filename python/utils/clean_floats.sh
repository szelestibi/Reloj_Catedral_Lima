#!/bin/bash

scriptname=${0##*/}
progname=${scriptname%.*}

/usr/bin/python ./$progname.py >./$progname.doc

