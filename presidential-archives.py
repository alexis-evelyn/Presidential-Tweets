#!/usr/bin/python

import sys
import pandas as pd
import json
import logging

from doltpy.core import Dolt, system_helpers
from doltpy.etl import get_df_table_writer
from doltpy.core.system_helpers import get_logger

# Dolt Logger
logger = get_logger(__name__)
log_level = logging.WARN  # Set to Info To Set Useful Info, Set to Debug To See Everything


def main(args: list):
    # Set Logging Level
    logging.Logger.setLevel(system_helpers.logger, log_level)  # DoltPy's Log Level
    logger.setLevel(log_level)  # This Script's Log Level

    # Print Command Line Arguments
    logger.debug("Command Line Arguments: ")
    logger.debug(str(args))

    # Test Data (Will Be Replaced With Function Args For Handling Different Presidents)
    repoPath = 'tests'
    table = 'trump'
    url = 'alexis-evelyn/presidential-tweets'
    message = 'Automated Tweet Update'

    # Defaults
    createRepo = False
    branch = 'master'

    data = retrieveData()
    tweet = extractTweet(data)
    df = getDataFrame(tweet)
    repo = initRepo(repoPath, createRepo)

    writeData(repo, table, df, tweet)

    # commitData(repo, table, message)
    # pushData(repo, url, branch)

    # Dolthub Employees - Uncomment to See Debug JSON Output
    logger.debug(json.dumps(tweet, indent=4))

    # Debug DataFrame
    # debugDataFrame(df)


def debugDataFrame(dataFrame: pd.DataFrame):
    # Setup Print Options
    pd.set_option('display.max_colwidth', None)
    pd.set_option('max_columns', None)

    # Print DataFrame Info
    logger.debug("DataFrame: ")
    logger.debug(dataFrame.head())


def retrieveData() -> dict:
    # Read JSON From File
    with open('tests/regular-test.json') as f:
        data = json.load(f)

    # Print JSON For Debugging
    logger.debug(data)

    return data


def extractTweet(data: dict) -> dict:
    # Extract Tweet Info
    tweet = data['data']
    metadata = data['includes']

    # Detect if Retweet
    isRetweet = False
    retweetedTweetId = None
    iteration = -1

    # If Has Referenced Tweets Key
    if 'referenced_tweets' in tweet:
        for refTweets in tweet['referenced_tweets']:
            iteration = iteration + 1

            if refTweets['type'] == 'retweeted':
                isRetweet = True
                retweetedTweetId = refTweets['id']
                break

    # Get Retweeted User's ID and Tweet Date
    retweetedUserId = None
    retweetedTweetDate = None

    # Pull From Same Iteration
    if 'tweets' in metadata and iteration < len(metadata['tweets']):
        retweetedUserId = metadata['tweets'][iteration]['author_id']
        retweetedTweetDate = metadata['tweets'][iteration]['created_at']

    logger.debug("User ID: " + "Not Set" if retweetedUserId is None else retweetedUserId)
    logger.debug("Tweet Date: " + "Not Set" if retweetedTweetDate is None else retweetedTweetDate)

    # Not Handled Columns
    repliedToTweetId = None
    repliedToUserId = None
    repliedToTweetDate = None

    retweetedTweetDate = None
    expandedUrls = None

    return {
        'id': tweet['id'],

        # This Tweet's Metadata
        'date': tweet['created_at'],
        'text': tweet['text'],
        'device': tweet['source'],

        # Engagement Statistics
        'favorites': tweet['public_metrics']['like_count'],
        'retweets': tweet['public_metrics']['retweet_count'],
        'quoteTweets': tweet['public_metrics']['quote_count'],
        'replies': tweet['public_metrics']['reply_count'],

        # This Tweet's Booleans
        'isRetweet': int(isRetweet),
        'isDeleted': 0,  # Currently hardcoded

        # Replied Tweet Info
        'repliedToTweetId': repliedToTweetId,
        'repliedToUserId': repliedToUserId,
        'repliedToTweetDate': repliedToTweetDate,

        # Retweet Info
        'retweetedTweetId': retweetedTweetId,
        'retweetedUserId': retweetedUserId,
        'retweetedTweetDate': retweetedTweetDate,

        # Expanded Urls
        'expandedUrls': expandedUrls,

        # Raw Json For Future Processing
        'json': data
    }


def getDataFrame(tweet: dict) -> pd.DataFrame:
    # Import JSON Into Panda DataFrame
    return pd.DataFrame([tweet])


def initRepo(path: str, create: bool) -> Dolt:
    # Prepare Repo For Data
    if create:
        return Dolt.init(path)

    return Dolt(path)


def writeData(repo: Dolt, table: str, dataFrame: pd.DataFrame, data: dict):
    # Prepare Data Writer
    raw_data_writer = get_df_table_writer(table, lambda: dataFrame, list(data.keys()))

    # Write Data To Repo
    raw_data_writer(repo)


def commitData(repo: Dolt, table: str, message: str):
    repo.add(table)
    repo.commit(message)


def pushData(repo: Dolt, url: str, branch: str):
    repo.remote(add=True, name='origin', url=url)
    repo.push('origin', branch)


if __name__ == '__main__':
    main(sys.argv)
