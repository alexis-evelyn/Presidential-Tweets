#!/usr/bin/python

# Apparently, I Cannot Figure Out How To Get Twython to Give Me The Original JSON,
# So I'm Just Downloading The Tweets Myself

import requests
import json


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token: str):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


class TweetDownloader:
    def __init__(self, auth: BearerAuth):
        self.auth = auth

    def get_tweet(self, tweet_id: str) -> json:
        params = {
            "tweet.fields": "id,text,attachments,author_id,conversation_id,created_at,entities,geo,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,source,withheld",
            "expansions": "author_id,referenced_tweets.id,in_reply_to_user_id,attachments.media_keys,attachments.poll_ids,geo.place_id,entities.mentions.username,referenced_tweets.id.author_id",
            "media.fields": "media_key,type,duration_ms,height,preview_image_url,public_metrics,width",
            "place.fields": "full_name,id,contained_within,country,country_code,geo,name,place_type",
            "poll.fields": "id,options,duration_minutes,end_datetime,voting_status",
            "user.fields": "id,name,username,created_at,description,entities,location,pinned_tweet_id,profile_image_url,protected,public_metrics,url,verified,withheld"
        }

        # 1183124665688055809 = id
        api_url = 'https://api.twitter.com/2/tweets/{}'.format(tweet_id)
        response = requests.get(api_url, params=params, auth=self.auth)
        return json.loads(response.text)
