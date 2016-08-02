import ConfigParser
import tweepy
from pymongo import MongoClient
import time
import datetime
import os.path

fn = os.path.join(os.path.dirname(__file__), 'config.ini')

config = ConfigParser.ConfigParser()
config.read(fn)

Config = ConfigParser.ConfigParser()
consumerKey = config.get('twitter', 'consumerKey')
consumerSecret = config.get('twitter', 'consumerSecret')
accessToken = config.get('twitter', 'accessToken')
accessSecret = config.get('twitter', 'accessSecret')
mongodbURI = config.get('mongodb', 'uri')


client = MongoClient(mongodbURI)
db = client.buildai
coll = db.followers

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
# auth.set_access_token(accessToken, accessSecret) Disabled to use the app api limit

api = tweepy.API(auth)

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def getDBFollowers():
  results = coll.find()
  array = []

  for user in results:
    array.append(user)

  return array


dbFollowers = getDBFollowers()
followersTemp = dbFollowers

def insertUser(userID):
  coll.insert_one(
    {
      "id": userID,
      "log": [
        {
          "date": date,
          "follow": True
        }
      ]
    }
  )

def updateUser(userID, follow):
  coll.update_one(
    {"id": userID},
    {
      "$push": {
        "log": {
          "date": date,
          "follow": follow
        }
      }
    }
  )

def getUserFromDB(userID):
  global dbFollowers

  for user in dbFollowers:
    tempUserID = user.get('id')

    if tempUserID == userID:
      return user

  return False

def isUserFollowing(user):
  log = user.get('log')

  for action in log:
    lastAction = action.get('follow')

  return lastAction

def removeUserFromArray(userID):
  global followersTemp

  tempArray = []

  for user in followersTemp:
    tempUserID = user.get('id')

    if tempUserID != userID:
      tempArray.append(user)

  followersTemp = tempArray

def processFollowers():
  for user in tweepy.Cursor(api.followers, screen_name="buildingai").items():
    userID = user.id
    userProfile = getUserFromDB(userID)

    if userProfile and isUserFollowing(userProfile):
      removeUserFromArray(userID)
    elif userProfile:
      updateUser(userID, True)
    else:
      insertUser(userID)

processFollowers()

# followersTemp now stores all users who have unfollowed
for user in followersTemp:
  userID = user.get('id')

  if not isUserFollowing(user):
    updateUser(userID, False)
