#!/bin/bash

echo
echo Update Lucid debian folder from standard debian folder...
sleep 1
echo
echo
echo Copy files from standard debian folder
rsync -rlvptD --exclude rules --exclude compat --exclude control ../debian/* .
echo
echo Add Lucid fix in patches/series
echo fix_lucid >> patches/series
echo
echo Done !
