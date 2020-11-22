#!/bin/bash

repoFolder="presidential-tweets"
source venv/bin/activate

echo "Repo Folder: $repoFolder"

while true; do
  echo "Saving Current Tweets Left To CSV"
  results=$(cd $repoFolder && dolt sql -q "select id from trump where json is null" -r csv > ../presidential-tweets/download-ids.csv)

  echo "Downloading New Tweets"
  python3 presidential-archives.py

  waitTime=$?
  # echo "Debug: $waitTime"

  if [ "$waitTime" -lt 1 ]
  then
    waitTime=16
  fi

  echo "Waiting $waitTime Minutes"
  sleep $((waitTime*60))
done