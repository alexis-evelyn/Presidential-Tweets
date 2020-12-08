#!/bin/bash

repoFolder="presidential-tweets"

if [ -f "./venv/bin/activate" ]
then
    echo "Using Venv ./venv/"
    source ./venv/bin/activate
fi

echo "Repo Folder: $repoFolder"

# The below is an artifact from when I left looping to the bash script
# echo "Saving Current Tweets Left To CSV"
# results=$(cd $repoFolder && dolt sql -q "select id from trump where json is null" -r csv > ../presidential-tweets/download-ids.csv)

python3 main.py