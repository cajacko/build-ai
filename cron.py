import ConfigParser
import tweepy
from pymongo import MongoClient


config = ConfigParser.ConfigParser()
config.read('config.ini')

Config = ConfigParser.ConfigParser()
consumerKey = config.get('twitter', 'consumerKey')
consumerSecret = config.get('twitter', 'consumerSecret')
accessToken = config.get('twitter', 'accessToken')
accessSecret = config.get('twitter', 'accessSecret')
mongodbURI = config.get('mongodb', 'uri')


client = MongoClient(mongodbURI)
db = client.buildai
coll = db.retweets

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessSecret)

api = tweepy.API(auth)

def insertRetweet(tweetID):
  coll.insert_one(
    {
      "id": tweetID
    }
  )

def hasNotRetweeted(tweetID):
  if coll.find({'id': tweetID}).count() > 0:
    return False
  else:
    return True

def retweetNext():
  for tweet in tweepy.Cursor(api.search,
                             q="#artificialintelligence filter:links",
                             rpp=100,
                             result_type="popular",
                             lang="en").items(100):
    tweetID = tweet.id

    if hasNotRetweeted(tweetID):
      try:
        api.retweet(tweetID)
      except Exception, e:
        pass

        if e.message[0]['code'] == 327:
          insertRetweet(tweetID)
          continue
        else:
          return False

      insertRetweet(tweetID)
      return True

  return False

retweetNext()
