#!/usr/bin/env bash

cd /app || exit

echo -e "\e[95mRunning Unit Tests...\e[39m"
coverage run manage.py test
echo -e "\e[95mDone\e[39m"

if [ "$1" = '--no-html' ] || [ "$1" = '-nh' ]; then
  echo -e "\e[95mGenerating HTML Coverage Report\e[39m"
  coverage html
  echo -e "\e[95mDone\e[39m"
fi
