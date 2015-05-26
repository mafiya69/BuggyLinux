#!/bin/zsh

#Exits on error
set -e

#Output Every command
set -x

#CF.JPG not copied
cp src_linux/CF.sublime-build Buggy---Linux
cp src_linux/Default\ \(Linux\).sublime-keymap Buggy---Linux
#ini.py not copied
cp src_linux/ini.sh CF/dist
cp src_linux/Main.sublime-menu Buggy---Linux
cp src_linux/start.sh CF/dist
cp src_linux/template.cpp CF/dist
cp src_linux/zx.sh CF/dist
cp src_linux/zy.sh CF/dist
cp src_linux/zz.sh CF/dist

cp README.md Buggy---Linux
