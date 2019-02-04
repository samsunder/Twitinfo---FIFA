import csv
from textblob import TextBlob
import re
import matplotlib.pyplot as plt
import os
maindir = os.path.dirname(os.path.abspath(__file__))

tweets = []


infile = 'FIFA.csv'

def strip_non_ascii(string):
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

kl=0
with open(infile, 'r') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        if kl==0:
            kl+=1
            continue
        tweet=dict()
        tweet['orig'] = row[6]
        tweet['id'] = int(row[0])
        tweet['place'] = row[13]
        if re.match(r'^RT.*', tweet['orig']):
            continue

        tweet['clean'] = tweet['orig']
        tweet['clean'] = strip_non_ascii(tweet['clean'])
        tweet['clean'] = tweet['clean'].lower()

        tweet['clean'] = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', tweet['clean'])
        tweet['TextBlob'] = TextBlob(tweet['clean'])

        tweets.append(tweet)


for tweet in tweets:
    tweet['polarity'] = float(tweet['TextBlob'].sentiment.polarity)
    tweet['subjectivity'] = float(tweet['TextBlob'].sentiment.subjectivity)

    if tweet['polarity'] >= 0.1:
        tweet['sentiment'] = 'positive'
    elif tweet['polarity'] <= -0.1:
        tweet['sentiment'] = 'negative'
    else:
        tweet['sentiment'] = 'neutral'

tweets_sorted = sorted(tweets, key=lambda k: k['polarity'])

print("\n\nTOP NEGATIVE TWEETS")
negative_tweets = [d for d in tweets_sorted if d['sentiment'] == 'negative']
nfile= open("negative.csv","w")
pfile= open("positive.csv","w")
neutfile= open("neutral.csv","w")
for tweet in negative_tweets:

    nfile.write("%s, id=%d, polarity=%.2f, clean=%s, %s\n" % ('Negative',tweet['id'], tweet['polarity'], tweet['clean'], tweet['place']))
nfile.close()

print("\n\nTOP POSITIVE TWEETS")
positive_tweets = [d for d in tweets_sorted if d['sentiment'] == 'positive']
for tweet in positive_tweets:

    pfile.write("%s, id=%d, polarity=%.2f, clean=%s, %s\n" % ('Positive',tweet['id'], tweet['polarity'], tweet['clean'], tweet['place']))
pfile.close()

print("\n\nTOP NEUTRAL TWEETS")
neutral_tweets = [d for d in tweets_sorted if d['sentiment'] == 'neutral']
for tweet in neutral_tweets:

    neutfile.write("%s, id=%d, polarity=%.2f, clean=%s, %s\n" % ('Neutral',tweet['id'], tweet['polarity'], tweet['clean'], tweet['place']))
neutfile.close()

x = [d['polarity'] for d in tweets_sorted]
num_bins = 21
n, bins, patches = plt.hist(x, num_bins, normed=1, facecolor='green', alpha=0.5)
plt.xlabel('Polarity')
plt.ylabel('Probability')
plt.title(r'Histogram of polarity')

plt.subplots_adjust(left=0.15)
plt.show()


pos = len(positive_tweets)
neu = len(negative_tweets)
neg = len(neutral_tweets)
labels = 'Positive', 'Neutral', 'Negative'
sizes = [pos, neu, neg]
colors = ['yellowgreen', 'gold', 'lightcoral']
plt.pie(sizes, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)
plt.axis('equal')
plt.show()
