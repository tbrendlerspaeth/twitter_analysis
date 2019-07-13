import json
import tweepy
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# Let's gain access to Twitter using passwords from a .json file.
with open('twitter_passwords.json') as passwords:
    opensesame = json.load(passwords)
    consumer_key = opensesame['CONSUMER_KEY']
    consumer_secret = opensesame['CONSUMER_SECRET']
    access_key = opensesame['ACCESS_KEY']
    access_secret = opensesame['ACCESS_SECRET']
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

# Who is your person of interest?
screen_name = input('Enter a twitter handle of interest: ')
num_tweets = int(input('Enter the number of tweets you wish to acquire: ')) # (panda)bear in mind - there is a limit

# Let's fetch some data and feed some pandas.
tweets_array = [[tweet.created_at, tweet.full_text, tweet.id_str] for tweet in
                tweepy.Cursor(api.user_timeline, screen_name=screen_name, tweet_mode='extended').items(num_tweets)]
df = pd.DataFrame(tweets_array, columns=['tweet_time', 'tweets', 'tweet_id'])

# Checking to see how well fed the pandas are.
print(str(len(df)) + ' tweets fetched.')
print('Most recent tweet occurred on ' + str(df.tweet_time[0]))
print('Oldest tweet occurred on ' + str(df.tweet_time[len(df) - 1]))

# Quick solution to getting rid of would-be prominent words in the cloud due to web links.
stopwords = set(STOPWORDS)
stopwords.update(['https', 'co', screen_name, 'amp', 'RT'])

# Wordclouding time
words = " ".join(tweet for tweet in df.tweets)
worldcloud = WordCloud(stopwords=stopwords, background_color='white',
                       color_func=lambda *args,**kwargs: "black").generate(words)
plt.imshow(worldcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
