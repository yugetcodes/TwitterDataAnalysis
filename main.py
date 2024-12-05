from twikit import Client, TooManyRequests
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint


MINIMUM_TWEETS = 10
QUERY = 'Chatgpt'


def get_tweets(tweets):
    if tweets is None:
        #* get tweets
        print(f'{datetime.now()} - Getting tweets...')
        tweets = client.search_tweet(QUERY, product='Top')
    else:
        wait_time = randint(5, 10)
        print(f'{datetime.now()} - Getting next tweets after {wait_time} seconds ...')
        time.sleep(wait_time)
        tweets = tweets.next()

    return tweets


#* login credentials
config = ConfigParser()
config.read('config.ini')
username = config['X']['username']
email = config['X']['email']
password = config['X']['password']

#* create a csv file
with open('tweets.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Tweet_count', 'Username', 'Text', 'Created At', 'Retweets', 'Likes'])



#* authenticate to X.com
#! 1) use the login credentials. 2) use cookies.
client = Client(language='en-US')
try:
    login_success = client.login(auth_info_1=username, auth_info_2=email, password=password)
    if login_success:
        print("Login successful!")
        client.save_cookies(r'C:\Users\vishn\Desktop\wd-101\venv\cookies.json')

    else:
        print("Login failed!")
except Exception as e:
    print(f"An error occurred during login: {e}")

client.load_cookies('cookies.json')


tweet_count = 0
tweets = None

while tweet_count < MINIMUM_TWEETS:

    try:
        tweets = get_tweets(tweets)
    except TooManyRequests as e:
        rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
        print(f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
        wait_time = rate_limit_reset - datetime.now()
        time.sleep(wait_time.total_seconds())
        continue

    if not tweets:
        print(f'{datetime.now()} - No more tweets found')
        break

    for tweet in tweets:
        tweet_count += 1
        tweet_data = [tweet_count, tweet.user.name, tweet.text, tweet.created_at, tweet.retweet_count, tweet.favorite_count]
        
        with open('tweets.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(tweet_data)

    print(f'{datetime.now()} - Got {tweet_count} tweets')


print(f'{datetime.now()} - Done! Got {tweet_count} tweets found')