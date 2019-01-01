import tweepy
import twitter_tokens
import json
import sqlite3
import nltk_class
from textblob import TextBlob


auth = tweepy.OAuthHandler(twitter_tokens.CONSUMER_KEY, twitter_tokens.CONSUMER_SECRET)
auth.set_access_token(twitter_tokens.ACCESS_TOKEN, twitter_tokens.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

t_list = []


def build_db():
    conn = sqlite3.connect('tweetdata.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE user (screen_name, text, tweet_id, nltk, pol, subj)''')
    conn.commit()
    conn.close()


def get_nltk(text):
    nltk = nltk_class.get_nltk_data(text)
    return nltk


def get_tb(text):
    text = TextBlob(text)
    pol = text.sentiment.polarity
    subj = text.sentiment.subjectivity
    return pol, subj

def store_data(screen_name, text, tweet_id):
    conn = sqlite3.connect('tweetdata.db')
    c = conn.cursor()
    nltk = get_nltk(text)
    pol, subj = get_tb(text)
    c.execute("INSERT INTO user (screen_name, text, tweet_id, nltk, pol, subj) values (?,?,?,?,?,?)", (screen_name, text, tweet_id, nltk, pol, subj))
    conn.commit()
    conn.close


class StreamListener(tweepy.StreamListener):

    def on_data(self, data):
        try:
            datajson = json.loads(data)
            if datajson['text'].startswith('RT @') == True:
                pass
            else:
                text = datajson['text']
                screen_name = datajson['user']['screen_name']
                tweet_id = datajson['id']
                lang = datajson['lang']
                if lang == 'en':
                    store_data(screen_name, text, tweet_id)
        except Exception as e:
            print(str(e))
            if str(e) == 'no such table: user':
                build_db()

    def on_error(self, status_code):
        if status_code == 420:
            return False


stream_listener = StreamListener()
stream = tweepy.Stream(auth = api.auth, listener=stream_listener)
stream.filter(track=['#HappyNewYear2019'])


