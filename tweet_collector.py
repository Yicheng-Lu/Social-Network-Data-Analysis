import tweepy
import csv
import pandas as pd
from time import time

print("Started")

#API key:
consumer_key = 'AcgJgEnjNdEQIyCjXB14vG9n9'

#API secret key:
consumer_secret = 'JiXHa1JQImgjJVECRjw9nTAmnUEQSaGJgRC84qfTbHGK7wa5Zd'

#Access token:
access_token = '1694114796-Gs14uxJhaJYsu4pgkaCmCCP1mDMi6oe738vhazN'

#Access token secret:
access_token_secret = 'H12jMiBb8JbsCG8nYqsCmiIDfOs2RiRXeQNycO0N1CUKr'


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth,wait_on_rate_limit=True)


datastorage = None


search_words = "#CoronaVirus"

# yyyy/mm/dd
date_since = "2020-03-04"
print("Date since:", date_since)

new_search = search_words + " -filter:retweets"


start_time = time()
print("Collection started at:", start_time)

tweets = tweepy.Cursor(api.search, q=new_search,lang="en", since=date_since).items(1000)

details = [[tweet.id,tweet.user.screen_name,tweet.created_at,tweet.user.location,tweet.place.bounding_box.coordinates[0][0][0],tweet.place.bounding_box.coordinates[0][0][1],tweet.text] for tweet in tweets if tweet.place]
tweet_data = pd.DataFrame(data=details, columns=['ID',"Name","Created_at","Location","Lat","Long","Text"])
if datastorage is None:
    datastorage = tweet_data
else:
    datastorage = datastorage.append(tweet_data)
print(len(datastorage), "currently read tweets.")
if time() - start_time > 300:
    start_time = time()
    print("Collection started at:", start_time)
    print("***", len(datastorage), "SAVED TWEETS.")
    try:
            dataset = pd.read_csv(r'./Dataset_Twitter.csv')
            dataset = dataset.append(datastorage)
            dataset.to_csv(r'./Dataset_Twitter.csv', index = False, header=True)
    except IOError:
            datastorage.to_csv(r'./Dataset_Twitter.csv', index=False, header=True)
    datastorage = None
