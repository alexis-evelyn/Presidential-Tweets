# Presidential Tweets

Will be used for automated retrieval of presidential tweets until Dolthub provides its own means to run CI. Check out this [dolt repo][repo] for more info. I linked the dolt repo as described by [this ReadMe][dolt-link].

## Trump
```sql
CREATE TABLE `trump` (
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

## Obama
```sql
CREATE TABLE `obama` (
  `id` bigint unsigned NOT NULL,
  `date` datetime NOT NULL,
  `text` longtext NOT NULL,
  `device` longtext NOT NULL,
  `favorites` bigint unsigned,
  `retweets` bigint unsigned,
  `quoteTweets` bigint unsigned,
  `replies` bigint unsigned,
  `isRetweet` tinyint,
  `isDeleted` tinyint,
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

## Biden
```sql
CREATE TABLE `biden` (
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

[repo]: https://www.dolthub.com/repositories/alexis-evelyn/presidential-tweets
[dolt-link]: https://github.com/dolthub/dolt/blob/master/go/cmd/git-dolt/README.md