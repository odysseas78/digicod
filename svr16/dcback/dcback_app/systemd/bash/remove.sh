#!/bin/bash

file="/home/dcback/systemd/*.service"


for f in $file; do
    if [ -f $f ] && [ -e /etc/systemd/system/$(basename $f) ]; then
        rm -rf /etc/systemd/system/$(basename $f)
        echo "$f deleted"
    fi
done
