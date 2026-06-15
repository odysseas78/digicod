#!/bin/bash

file="/home/dcback/systemd/*.service"

for f in $file; do
    if systemctl is-active --quiet $(basename $f); then
        echo "Service wird gestopt und disabled."
        systemctl disable $(basename $f)
        systemctl stop $(basename $f)
    else
        echo "Service nicht ausgeführt."
    fi
done