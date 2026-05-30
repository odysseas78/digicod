#!/bin/bash

if [ "$(ls -A /home/dcback/deploy/)" ]; then
   echo "Der Ordner deploy ist nicht leer. Lösche den Inhalt des Ordners."
   rm -r /home/dcback/deploy/*
else
   echo "Der Ordner deploy ist leer."
fi
