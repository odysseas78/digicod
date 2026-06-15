#!/bin/bash

if [ "$(ls -A deploy)" ]; then
   echo "Der Ordner deploy ist nicht leer. Lösche den Inhalt des Ordners."
   rm -r deploy/*
else
   echo "Der Ordner deploy ist leer."
fi
