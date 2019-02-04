

import tweepy
import csv
import json


with open('twitter_credentials.json') as cred_data:
    info = json.load(cred_data)
    consumer_key = info['CONSUMER_KEY']
    consumer_secret = info['CONSUMER_SECRET']
    access_key = info['ACCESS_KEY']
    access_secret = info['ACCESS_SECRET']


def get_all_tweets(screen_name):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)


    all_the_tweets = []

    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    all_the_tweets.extend(new_tweets)

    oldest_tweet = all_the_tweets[-1].id - 1

    while len(new_tweets) > 0:

        new_tweets = api.user_timeline(screen_name=screen_name,
                count=200, max_id=oldest_tweet)

        all_the_tweets.extend(new_tweets)

        oldest_tweet = all_the_tweets[-1].id - 1
        print ('...%s tweets have been downloaded so far' % len(all_the_tweets))

    outtweets = [[tweet.id_str, tweet.created_at,
                 tweet.text.encode('utf-8')] for tweet in all_the_tweets]

    with open(screen_name + '_tweets.csv', 'w', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'created_at', 'text'])
        writer.writerows(outtweets)


if __name__ == '__main__':

    get_all_tweets(input("Enter the twitter handle of the person whose tweets you want to download:- "))