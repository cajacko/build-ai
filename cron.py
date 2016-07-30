import ConfigParser
import tweepy
import json
import os.path

jsonFile = "data.json"
jsonKey = "lastTweetID"

if os.path.isfile(jsonFile) is False:
  lastTweetID = 0
else:
  with open(jsonFile) as data_file:    
    data = json.load(data_file)
    lastTweetID = data[jsonKey]

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

for tweet in tweepy.Cursor(api.search,
                           q="#artificialintelligence filter:links",
                           rpp=20,
                           result_type="popular",
                           since_id=lastTweetID,
                           lang="en").items(3):
  tweetID = tweet.id

  if lastTweetID < tweetID:
    lastTweetID = tweetID

  try:
    api.retweet(tweetID)
  except Exception, e:
    pass

data = {jsonKey: lastTweetID}

with open(jsonFile, 'w') as outfile:
    json.dump(data, outfile)