#!/bin/bash

repoFolder="presidential-tweets"

if [ -f "./venv/bin/activate" ]
then
    echo "Using Venv ./venv/"
    source ./venv/bin/activate
fi

echo "Repo Folder: $repoFolder"

while true; do
  # echo "Saving Current Tweets Left To CSV"
  # results=$(cd $repoFolder && dolt sql -q "select id from trump where json is null" -r csv > ../presidential-tweets/download-ids.csv)

  echo "Downloading New Tweets"
  python3 main.py --log=verbose

  waitTime=$?
  # echo "Debug: $waitTime"

  # Originally Less Than 2
  if [ "$waitTime" -lt 1 ]
  then
    # Originally 16
    waitTime=1
  fi

  echo "Waiting $waitTime Minutes"
  sleep $((waitTime*60))
done