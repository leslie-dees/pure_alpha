import tweepy
import config as config
import pandas as pd
import csv
import numpy as np



def get_tweet_data(my_id_enter):
    """
    Creates a csv file of all tweet fields specified in the Paginator
    params:
    >my_id_enter: id information returned by get_user_data. run get_user_data with a given screen name and input the result in here
    return vals:
    >csv of all info witihn the tweets
    -id -> tweet id
    -date -> date that the tweet was made
    -this_is_reply -> True if the tweet was a reply to another tweet. False if the tweet was a retweet or an original
    -text -> the text contained in the tweet
    -retweets -> number of retweets
    -replies -> number of replies
    -likes -> number of likes
    -quotes -> number of times the tweet was quoted
    -attachments -> attachments in the tweet, gifs, pics
    -entities -> urls, hashtags, mentions
    """
    my_id = int(my_id_enter[1])
    
    column_names = ['id', 'date', 'this_is_reply', 'text', 'retweets', 'replies', 'likes', 'quotes','attachments', 'entities']
    df = pd.DataFrame(columns = column_names)

    client = tweepy.Client(bearer_token=config.BEARER_TOKEN, wait_on_rate_limit = True)
    NoneType = type(None)
    
    for tweet in tweepy.Paginator(client.get_users_tweets, id = my_id, max_results = 100, tweet_fields=['id', 'created_at', 'in_reply_to_user_id', 'public_metrics', 'attachments', 'text', 'entities']).flatten(limit=1000):
        rowAdd = pd.DataFrame({
            'id':[tweet.id],
            'date':[tweet.created_at],
            'this_is_reply': [type(tweet.in_reply_to_user_id) != NoneType],
            'text':[tweet.text],
            'retweets':[tweet.public_metrics['retweet_count']],
            'replies':[tweet.public_metrics['reply_count']],
            'likes':[tweet.public_metrics['like_count']],
            'quotes':[tweet.public_metrics['quote_count']],
            'attachments':[tweet.attachments],
            'entities':[tweet.entities]
        })

        df = pd.concat([df, rowAdd], ignore_index = True, axis=0)

    df.to_csv(str(my_id_enter[0])+'.csv')    



def get_user_data(screen_name):
    """
    params:
    >screen_name: twitter screen name for a single user (do not include the @)
    return vals:
    >returns a list of values associated with the user
    -[0]: screen name of the user
    -[1]: id of the user
    -[2]: followers count of the user
    -[3]: following count of the user
    """
    client = tweepy.Client(bearer_token=config.BEARER_TOKEN, wait_on_rate_limit = True)
    twitterid = client.get_user(username=screen_name, user_fields='public_metrics')
    my_array = []

    my_array.append(screen_name)
    my_array.append(twitterid.data.id)
    my_array.append(twitterid.data.public_metrics['followers_count'])
    my_array.append(twitterid.data.public_metrics['following_count'])

    

    


    return my_array

def get_user_followers(screen_name):
    client = tweepy.Client(bearer_token=config.BEARER_TOKEN, wait_on_rate_limit = True)
    twitterid = client.get_user(username=screen_name)
    my_id = twitterid.data.id
    
    all_follower_ids = []
    for follower in tweepy.Paginator(client.get_users_followers, id = twitterid.data.id, max_results = 100).flatten(limit=1000):
        this_twitter_follower_id = client.get_user(username=follower).data.id
        all_follower_ids.append(this_twitter_follower_id)

    
def get_influencer_ids(path):
    with open(path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        list_of_rows = list(csv_reader)
    list_of_rows = np.array(list_of_rows)
    twitter_handles_list = list_of_rows[1:]
    twitter_names_list = []
    for twitter_name in twitter_handles_list:
        twitter_names_list.append(twitter_name[0][20:])

    screen_and_id_list = []
    for screen_name in twitter_names_list:
        my_screen_and_id = get_user_data(screen_name)
        screen_and_id_list.append(my_screen_and_id)

    col_names = ['screen_name', 'id', 'followers', 'following']
    df = pd.DataFrame(screen_and_id_list, columns = col_names)
    df.to_csv('Influencer_id_whitelist.csv')
path = 'twitter_data/Reputable_influencers.csv'


#get_influencer_ids('twitter_data/Reputable_influencers.csv')
#get_user_followers('ailoverse')

#my_id = get_user_data('ailoverse')
#print(my_id)


#thingy = get_tweet_data(my_id)
#print(thingy)
