#!/bin/bash

repoFolder="presidential-tweets"
latestHash=$(cd $repoFolder && dolt log -n 1 | grep commit | cut -d' ' -f2)

updateResults=$(git dolt update $repoFolder.git-dolt $latestHash)

echo "Repo Folder: $repoFolder"
echo "Hash: $latestHash"
echo "Results: $updateResults"