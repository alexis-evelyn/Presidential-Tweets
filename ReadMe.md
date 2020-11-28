# Presidential Tweets

Will be used for automated retrieval of presidential tweets until Dolthub provides its own means to run CI. Check out this [dolt repo][repo] for more info. I linked the dolt repo as described by [this ReadMe][dolt-link].

To update the pointer file, run the bash script [./updatePointer.sh][update-pointer]. You need Dolt and git installed as well as having already fetched the latest commit by running `git dolt fetch presidential-tweets.git-dolt` and then pulling the latest commit via `dolt pull` inside the `presidential-tweets` folder.

On OSX, you may need to install the Python3 requirements yourself instead of letting your IDE do it. The command for that is `ARCHFLAGS="-arch x86_64" pip3 install -r ../requirements.txt`.

Raspberry Pi support does not exist because Dolt segfaults on it, however, to get numpy to work, install `sudo apt-get install libatlas-base-dev`. Also, you will need to create `credentials.json` at the root of the project in the format as described below.

### Credentials File

```json
{
  "BEARER_TOKEN": "YOUR-TWITTER-APP-BEARER-TOKEN-HERE"
}
```

## President Table
```sql
CREATE TABLE `your-president` (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

# Future Replacement Table Schema
```sql
CREATE TABLE `your-president` (
  `id` bigint unsigned NOT NULL, <-- Should Never Be Null, Otherwise Pointless To Record
  `date` datetime NOT NULL, <-- Should Never Be Null, Otherwise Pointless To Record
  `text` longtext NOT NULL, <-- Should Never Be Null, Otherwise Pointless To Record
  `device` longtext NOT NULL, <-- Defaults to N/A if Otherwise Null
  `likes` bigint unsigned NOT NULL, <-- Replaces favorites as Twitter refers to hearts/favorites as likes in it's API - Defaults to 0 if Otherwise Null
  `retweets` bigint unsigned NOT NULL, <-- Defaults to 0 if Otherwise Null
  `quoteTweets` bigint unsigned NOT NULL, <-- Defaults to 0 if Otherwise Null
  `replies` bigint unsigned NOT NULL, <-- Defaults to 0 if Otherwise Null
  `isRetweet` tinyint NOT NULL, <-- Defaults to 0 if Otherwise Null
  `isUnavailable` tinyint NOT NULL, <-- Replaces isDeleted. Should be 0 if null or tweet is otherwise inaccessible
  `repliedToTweetId` bigint unsigned, <-- Nullable
  `repliedToUserId` bigint unsigned, <-- Nullable
  `repliedToTweetDate` datetime, <-- Nullable
  `retweetedTweetId` bigint unsigned, <-- Nullable
  `retweetedUserId` bigint unsigned, <-- Nullable
  `retweetedTweetDate` datetime, <-- Nullable
  `expandedUrls` longtext, <-- Nullable
  `json` longtext NOT NULL, <-- Should Never Be Null, Can Retrieve JSON Response By Querying Twitter API For Tweet ID (represented by id)
  PRIMARY KEY (`id`) <-- Tweet IDs Are Unique Across The Whole Platform
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

[repo]: https://www.dolthub.com/repositories/alexis-evelyn/presidential-tweets
[dolt-link]: https://github.com/dolthub/dolt/blob/master/go/cmd/git-dolt/README.md
[update-pointer]: updatePointer.sh
