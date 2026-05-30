#!/bin/bash

file="/home/dcback/systemd/*.service"


for f in $file; do
    if [ -f $f ] && [ ! -e /etc/systemd/system/$(basename $f) ]; then
        ln $f /etc/systemd/system/
        echo "Hardlink created for $f"
    fi
done
sudo systemctl daemon-reload