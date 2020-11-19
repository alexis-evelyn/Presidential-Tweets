#!/usr/bin/python

import argparse
import pandas as pd
import json
import logging

from doltpy.core import Dolt, system_helpers
from doltpy.etl import get_df_table_writer
from doltpy.core.system_helpers import get_logger

# Custom Log Levels
VERBOSE = logging.DEBUG - 1
logging.addLevelName(VERBOSE, "VERBOSE")

# Dolt Logger
logger = get_logger(__name__)

# Argument Parser Setup
parser = argparse.ArgumentParser(description='Arguments For Presidential Tweet Archiver')
parser.add_argument("-log", "--log", help="Set Log Level (Defaults to WARNING)",
                    dest='logLevel',
                    default='WARNING',
                    type=str.upper,
                    choices=['VERBOSE', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])


def main(arguments: argparse.Namespace):
    # Set Logging Level
    logging.Logger.setLevel(system_helpers.logger, arguments.logLevel)  # DoltPy's Log Level
    logger.setLevel(arguments.logLevel)  # This Script's Log Level

    # Print Command Line Arguments
    logger.log(VERBOSE, "Command Line Arguments: ")
    logger.log(VERBOSE, str(arguments))

    # Test Data (Will Be Replaced With Function Args For Handling Different Presidents)
    repoPath = 'tests'
    table = 'test'
    url = 'alexis-evelyn/test'  # 'alexis-evelyn/presidential-tweets'
    message = 'Automated Tweet Update'

    # Defaults
    branch = 'master'

    # Setup Repo
    repo = setupRepo(repoPath=repoPath, createRepo=False, table=table, url=url)

    # TODO: Move Me To Loop Function For Looping Through Tweets - Add Tweet To Database
    addTweetToDatabase(repo=repo, table=table)

    # Commit Changes If Any
    madeCommit = commitData(repo=repo, table=table, message=message)

    # Don't Bother Pushing If Not Commit
    if madeCommit:
        pushData(repo=repo, branch=branch)


def downloadTweetsFromFile():
    None


def setupRepo(repoPath: str, createRepo: bool, table: str, url: str = None) -> Dolt:
    repo = initRepo(path=repoPath, create=createRepo, url=url)
    createTableIfNotExists(repo=repo, table=table)  # , dataFrame=df, keys=list(tweet.keys())
    return repo


def addTweetToDatabase(repo: Dolt, table: str):
    data = retrieveData()
    tweet = extractTweet(data)
    df = getDataFrame(tweet)

    # Use `python3 this-script.py --log=VERBOSE` in order to see this output
    logger.log(VERBOSE, json.dumps(tweet, indent=4))

    writeData(repo=repo, table=table, dataFrame=df, requiredKeys=['id'])

    # Debug DataFrame
    # debugDataFrame(df)


def debugDataFrame(dataFrame: pd.DataFrame):
    # Setup Print Options
    pd.set_option('display.max_colwidth', None)
    pd.set_option('max_columns', None)

    # Print DataFrame Info
    logger.log(VERBOSE, "DataFrame: ")
    logger.log(VERBOSE, dataFrame.head())


def retrieveData() -> dict:
    # Read JSON From File
    with open('tests/embedded-link.json') as f:
        data = json.load(f)

    # Print JSON For Debugging
    logger.log(VERBOSE, data)

    return data


def extractTweet(data: dict) -> dict:
    # Extract Tweet Info
    tweet = data['data']
    metadata = data['includes']

    # RETWEET SECTION ----------------------------------------------------------------------

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
    if 'tweets' in metadata and isRetweet and iteration < len(metadata['tweets']):
        retweetedUserId = metadata['tweets'][iteration]['author_id']
        retweetedTweetDate = metadata['tweets'][iteration]['created_at']

    logger.debug("Retweeted User ID: " + ("Not Set" if retweetedUserId is None else retweetedUserId))
    logger.debug("Retweeted Tweet ID: " + ("Not Set" if retweetedTweetId is None else retweetedTweetId))
    logger.debug("Retweeted Tweet Date: " + ("Not Set" if retweetedTweetDate is None else retweetedTweetDate))

    # REPLY SECTION ----------------------------------------------------------------------

    # TODO: IMPLEMENT
    repliedToTweetId = None
    repliedToUserId = None
    repliedToTweetDate = None
    isReplyTweet = False
    iteration = -1

    # If Has Referenced Tweets Key
    if 'referenced_tweets' in tweet:
        for refTweets in tweet['referenced_tweets']:
            iteration = iteration + 1

            if refTweets['type'] == 'replied_to':
                isReplyTweet = True
                repliedToTweetId = refTweets['id']
                break

    if 'tweets' in metadata and isReplyTweet and iteration < len(metadata['tweets']):
        repliedToUserId = metadata['tweets'][iteration]['author_id']
        repliedToTweetDate = metadata['tweets'][iteration]['created_at']

    logger.debug("Replied To User ID: " + ("Not Set" if repliedToUserId is None else repliedToUserId))
    logger.debug("Replied To Tweet ID: " + ("Not Set" if repliedToTweetId is None else repliedToTweetId))
    logger.debug("Replied To Tweet Date: " + ("Not Set" if repliedToTweetDate is None else repliedToTweetDate))

    # EXPANDED URLS SECTION ----------------------------------------------------------------------

    # Look For Expanded URLs in Tweet
    expandedUrls = None

    if 'entities' in tweet and 'urls' in tweet['entities']:
        expandedUrls = ""  # Set to Blank String

        # Loop Through Expanded URLs
        for url in tweet['entities']['urls']:
            expandedUrls = expandedUrls + url['expanded_url'] + ', '

        # Remove Extra Comma
        expandedUrls = expandedUrls[:-2]

    # FORM DICTIONARY SECTION ----------------------------------------------------------------------

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


def initRepo(path: str, create: bool, url: str = None) -> Dolt:
    # Prepare Repo For Data
    if create:
        repo = Dolt.init(path)
        repo.remote(add=True, name='origin', url=url)
        return repo

    return Dolt(path)


def writeData(repo: Dolt, table: str, dataFrame: pd.DataFrame, requiredKeys: list):
    # Prepare Data Writer
    raw_data_writer = get_df_table_writer(table, lambda: dataFrame, requiredKeys)

    # Write Data To Repo
    raw_data_writer(repo)


def createTableIfNotExists(repo: Dolt, table: str) -> str:
    columns = '''
        `id` bigint unsigned NOT NULL,
        `date` datetime NOT NULL,
        `text` longtext NOT NULL,
        `device` longtext NOT NULL,
        `favorites` bigint unsigned NOT NULL,
        `retweets` bigint unsigned NOT NULL,
        `quoteTweets` bigint unsigned,
        `replies` bigint unsigned,
        `isRetweet` tinyint NOT NULL,
        `isDeleted` tinyint NOT NULL,
        `repliedToTweetId` bigint unsigned,
        `repliedToUserId` bigint unsigned,
        `repliedToTweetDate` datetime,
        `retweetedTweetId` bigint unsigned,
        `retweetedUserId` bigint unsigned,
        `retweetedTweetDate` datetime,
        `expandedUrls` longtext,
        `json` longtext,
        PRIMARY KEY (`id`)
    '''

    settings = '''
        ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    '''

    create_table = '''
        CREATE TABLE IF NOT EXISTS {table} ({columns}) {settings}
    '''.format(table=table, columns=columns, settings=settings)

    return repo.sql(create_table, result_format='csv')


def commitData(repo: Dolt, table: str, message: str) -> bool:
    # Check to ensure changes need to be added first
    if not repo.status().is_clean:
        repo.add(table)
        repo.commit(message)
        return True
    return False


def pushData(repo: Dolt, branch: str):
    repo.push('origin', branch)


if __name__ == '__main__':
    # This is to get DoltPy's Logger To Shut Up When Running `this_script.py -h`
    logging.Logger.setLevel(system_helpers.logger, logging.CRITICAL)

    args = parser.parse_args()
    main(args)
