#!/bin/bash

#set -x

for f in ./*.py; do
 [ -f "$f" ] || continue
 echo "Running $f..."
 /usr/bin/python "$f" || { echo "❌ Error in $f"; exit 1; }
done

echo " ... all scripts ran successfully ..."

#set +x
