#!/bin/bash

repoFolder="presidential-tweets"
source venv/bin/activate

echo "Repo Folder: $repoFolder"

while true; do
  echo "Saving Current Tweets Left To CSV"
  results=$(cd $repoFolder && dolt sql -q "select id from trump where isDeleted=0 and json is null" -r csv > ../existing_tweets/trump-ids-exists.csv)

  echo "Downloading New Tweets"
  python3 presidential-archives.py

  waitTime=$?

  if [ "$waitTime" -lt 1 ]
  then
    waitTime=$((16*60))
  fi

  echo "Waiting $((waitTime/60)) Minutes"
  sleep $waitTime
done