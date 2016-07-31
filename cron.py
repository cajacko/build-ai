import ConfigParser
import tweepy
from pymongo import MongoClient
import time
import datetime

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

def logCron(message):
  ts = time.time()
  date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

  db.log.insert_one(
    {
      "date": date,
      "message": message
    }
  )

def hasNotRetweeted(tweetID):
  if coll.find({'id': tweetID}).count() > 0:
    return False
  else:
    return True

def retweetNext():
  print 'retweetNext init'

  for tweet in tweepy.Cursor(api.search,
                             q="#artificialintelligence filter:links",
                             rpp=100,
                             result_type="mixed",
                             lang="en").items(100):
    tweetID = tweet.id
    print tweetID

    if hasNotRetweeted(tweetID):
      print 'is not in db'

      try:
        api.retweet(tweetID)
      except Exception, e:
        pass
        print 'tweepy error'

        if e.message[0]['code'] == 327:
          print 'already retweeted'

          insertRetweet(tweetID)
          continue
        else:
          print e
          logCron(e.message[0]['code'])
          return False

      print 'retweeted'
      insertRetweet(tweetID)
      logCron('Retweeted')
      return True
    else:
      print 'already retweeted and in db'

  logCron('Ran out of tweets')
  print 'ran out of tweets'
  return False

print 'run function'
logCron('Cron run')
retweetNext()
