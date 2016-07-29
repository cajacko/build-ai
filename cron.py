import ConfigParser
import tweepy
import json

config = ConfigParser.ConfigParser()
config.read('config.ini')

Config = ConfigParser.ConfigParser()
consumerKey = config.get('twitter', 'consumerKey')
consumerSecret = config.get('twitter', 'consumerSecret')
accessToken = config.get('twitter', 'accessToken')
accessSecret = config.get('twitter', 'accessSecret')

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessSecret)

api = tweepy.API(auth)
tweets = 

for tweet in tweepy.Cursor(api.search,
                           q="#artificialintelligence filter:links",
                           rpp=100,
                           result_type="recent",
                           include_entities=True,
                           lang="en").items(5):
  print tweet.text
  print

# data = {"lastTweet": 49765987498479}

# with open('data.json', 'w') as outfile:
#     json.dump(data, outfile)