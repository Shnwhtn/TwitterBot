import datetime
import sys
import time
from bs4 import BeautifulSoup
import requests
import twitter
import tweepy
import json
from tweepy.parsers import JSONParser

USERDETAILS = 'userdetails.txt'



def check_twitter_api(api):
    try:
        print(api.VerifyCredentials())
    except:
        print("Could not authenticate with API")
        sys.exit()

def get_tweets():
    # init tweepy
    print (consumer_key)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.search("#rttowin", count=10, lang="en")

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) < 0:
        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.search("#rttowin", count=10, lang="en",max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print("...%s tweets downloaded so far" % (len(alltweets)))

    # write tweet objects to JSON

    file = open('tweet.json', 'w', encoding="utf8")
    print ("Writing tweet objects to JSON please wait...")
    for status in alltweets:
        #dump tweets to json file
        json.dump(status._json, file, sort_keys=False, indent=4)
        print(status._json["text"])

        #print id,url,message,user,@tag -> array

    # close the file
    print ("done")
    file.close()




def init():
    try:
        tokendetails = open(USERDETAILS,"r")
    except:
        print("No valid user tokens supplied, See Readme")
        sys.exit()
    try:
        #consumer key
        consumer_key_c = tokendetails.readline().rstrip()
        consumer_key_d = consumer_key_c.split("consumer_key = ")
        consumer_key = consumer_key_d[1]
        #consumer secret key
        consumer_secret_c = tokendetails.readline().rstrip()
        consumer_secret_d = consumer_secret_c.split("consumer_secret = ")
        consumer_secret = consumer_secret_d[1]
        #access token key
        access_token_key_c = tokendetails.readline().rstrip()
        access_token_key_d = access_token_key_c.split("access_token_key = ")
        access_token_key = access_token_key_d[1]
        #access token secret key
        access_token_secret_c = tokendetails.readline().rstrip()
        access_token_secret_d = access_token_secret_c.split("access_token_secret = ")
        access_token_secret = access_token_secret_d[1]
                        ## debug ##
        print(consumer_key)
        print(consumer_secret)
        print(access_token_key)
        print(access_token_secret)
    except:
        print("Invalid tokens in the user details file")
        sys.exit()

    api = twitter.Api(consumer_key,consumer_secret,access_token_key,access_token_secret)
    #Got User Details now check the api
    check_twitter_api(api)
    print("Working")
    get_tweets()





    #r = requests.get("https://twitter.com/search?q=Babylon%205&src=typd")
    #data = r.text
    #soup = BeautifulSoup(data,"html.parser")
    #tweets = [p.text for p in soup.findAll('p',class_='tweet-text')]
    #print(tweets)

init()