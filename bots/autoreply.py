#!/usr/bin/env python
# tweepy-bots/bots/autoreply.py

import tweepy
import logging
from config import create_api
import time
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def check_mentions(api, keywords, since_id, netflixIndia):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        if any(keyword in tweet.text.lower() for keyword in keywords):
            logger.info(f"Answering to {tweet.user.name}")
            ran = random.randint(0, 34)
            # if not tweet.user.following:
            #     tweet.user.follow()

            api.update_status(
                status="I think today you should watch "+netflixIndia[ran],
                in_reply_to_status_id=tweet.id,
            )
    return new_since_id

def main():
    api = create_api()
    since_id = 1
    f = open("NetflixIndia.txt","r")
    netflixIndia = []
    for x in f:
        netflixIndia.append(x)
    while True:
        since_id = check_mentions(api, ["@netflixIndia"], since_id,netflixIndia)
        logger.info("Waiting...")
        time.sleep(20)

if __name__ == "__main__":
    main()