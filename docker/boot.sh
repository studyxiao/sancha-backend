#!/bin/sh
while true; do
  flask db migrate
  flask db upgrade
  if [[ "$?" == "0" ]]; then
    break
  fi
  echo $?
  echo Deploy command failed, retrying in 5 secs...
  sleep 5
done
