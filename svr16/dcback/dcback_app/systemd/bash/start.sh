#!/bin/bash

file="/home/dcback/systemd/*.service"

for f in $file; do
    if systemctl is-active --quiet $(basename $f); then
        echo "Service wird ausgeführt."
    else
        echo "Service wird eingeschaltet und ausgeführt."
        systemctl enable $(basename $f)
        systemctl start $(basename $f)
    fi
done