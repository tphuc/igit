#!/usr/bin/env bash
rm -r .lgit
echo abc > abc
echo xyz > xyz
./lgit.py init
./lgit.py add abc
./lgit.py commit -m "abc"
./lgit.py branch new
./lgit.py checkout new
echo "modified abc" > abc
./lgit.py add xyz abc
./lgit.py commit -m "xyz"
./lgit.py checkout master
echo "ON BRANCH MASTER"
cat abc xyz
./lgit.py checkout new
echo "ON BRANCH NEW"
cat abc xyz
./lgit.py checkout master
echo "ON BRANCH MASTER AGAIN"
cat abc xyz
