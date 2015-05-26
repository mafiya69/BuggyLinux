#!/bin/zsh

echo -n "Enter the round number : "
read round
./ini.py < $round
if [ ! -d "$round" ]; then
  exit
fi
chmod -R 777 $round
subl ./$round
subl $round/A/prog.cpp
alias xdg-open="xdg-open 2>/dev/null"
xdg-open http://codeforces.com/contest/$round/problems
