#!/bin/bash

file="/home/dcback/systemd/*.service"

for f in $file; do
    if systemctl is-active --quiet $(basename $f); then
        echo "Service wird ausgeführt."
    else
        echo "Service wird restarted."
        # systemctl enable $(basename $f)
        systemctl restart $(basename $f)
    fi
done