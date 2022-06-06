import numpy as np
import csv
import pandas as pd
from datetime import datetime, timedelta
import tweepy
import config as config
import discord_message_collection as dmc
import pytz
from Historic_Crypto import HistoricalData

def get_user_data(screen_name):
    #input: Twitter handle
    #output: array of screen name, twitter id, follower count, and following count
    
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


def get_tweet_data(my_screen_name, my_id):
    #input: twitter handle, twitter id
    #output: csv file with all tweets

    """
    Creates a csv file of all tweet fields
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

    df.to_csv('nft_tweets/'+my_screen_name+'.csv')    

def time_between_posts(list_of_dates):
    #input: list of all ISO 8601 format dates
    #output: average number of hours between posts
    tot_time = 0
    for i in range(len(list_of_dates)-1):
        dateA = datetime.strptime(list_of_dates[i][:19], '%Y-%m-%d %H:%M:%S')
        dateB = datetime.strptime(list_of_dates[i+1][:19], '%Y-%m-%d %H:%M:%S')
        time_diff = dateA-dateB
        time_seconds = time_diff.total_seconds()
        time_hours = time_seconds / 3600
        tot_time +=time_hours
    
    return tot_time/len(list_of_dates)

def get_tweet_metrics(my_csv_location):
    #input: location of tweets for an nft
    #output: dataframe with tweet metrics
    #my_csv_location = the folder location along with the .csv of the tweet data that we are analyzing
    with open(my_csv_location, 'r', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file)
        list_of_rows = list(csv_reader)
    list_of_rows = np.array(list_of_rows)

    no_retweets_list = []
    

    for row in list_of_rows[1:]:
        if (row[4][:2] != "RT") & (row[3] != "True"):
            no_retweets_list.append(row)
        

    no_retweets_list = np.array(no_retweets_list)

    retweets_retweet_count = np.sum(list_of_rows[1:][:,5].astype(int))
    retweets_replies_count = np.sum(list_of_rows[1:][:,6].astype(int))
    retweets_likes_count = np.sum(list_of_rows[1:][:,7].astype(int))
    
    no_retweets_retweet_count = np.sum(no_retweets_list[:,5].astype(int))
    no_retweets_replies_count = np.sum(no_retweets_list[:,6].astype(int))
    no_retweets_likes_count = np.sum(no_retweets_list[:,7].astype(int))
    
    no_retweets_hours_between = time_between_posts(no_retweets_list[:, 2])
    retweets_hours_between = time_between_posts(list_of_rows[1:][:, 2])
    
    df = pd.DataFrame()
    df['my_retweets'] = [no_retweets_retweet_count]
    df['rt_retweets'] = [retweets_retweet_count]
    df['my_replies'] = [no_retweets_replies_count]
    df['rt_replies'] = [retweets_replies_count]
    df['my_likes'] = [no_retweets_likes_count]
    df['rt_likes'] = [retweets_likes_count]
    df['my_hrs_between'] = [no_retweets_hours_between]
    df['rt_hrs_between'] = [retweets_hours_between]
    return df

def influencer_data(nft_screen_name):
    #input: twitter handle
    #output: numpy array of screen name, total influencer followings, regularized influencer followings
    auth = tweepy.OAuthHandler(consumer_key=config.API_KEY, consumer_secret=config.API_KEY_SECRET)
    auth.set_access_token(key=config.ACCESS_TOKEN, secret=config.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    with open('Influencers_followers.csv', 'r') as filename:
        csv_reader = csv.reader(filename)
        my_influencers = list(csv_reader)
        my_influencers = np.array(my_influencers)
        my_influencers = my_influencers[1:, 1:]
    
    total_following = 0
    regularized_following = 0
    for influencer in my_influencers:
        my_influencer_name = influencer[0]
        friendship = api.get_friendship(source_screen_name = my_influencer_name, target_screen_name = nft_screen_name)
        is_following = friendship[0].following
        if is_following:
            total_following+=1
            regularized_following+=float(influencer[2])
    
    this_nft_array = [total_following, regularized_following]
    return np.array(this_nft_array)

def get_moving_average_crypto(mint_time):
    one_week_back = mint_time - timedelta(days = 7)

    str_time_week = one_week_back.strftime('%Y-%m-%d-%H-%M')
    strMintTime = mint_time.strftime('%Y-%m-%d-%H-%M')
    
    data_week = HistoricalData('ETH-USD', 900, start_date = str_time_week, end_date = strMintTime, verbose = False).retrieve_data()
    data_five = data_week.drop(index=data_week.index[:192], axis=0, inplace = False)
    data_three = data_five.drop(index=data_five.index[:192], axis=0, inplace = False)
    data_one = data_three.drop(index=data_three.index[:192], axis=0, inplace = False)    

    averageEthPriceWeek = data_week["close"].mean()
    averageEthPriceFive = data_five["close"].mean()
    averageEthPriceThree = data_three["close"].mean()
    averageEthPriceOne = data_one["close"].mean()

    return pd.DataFrame([np.array([averageEthPriceOne, averageEthPriceThree, averageEthPriceFive, averageEthPriceWeek])], columns=["MAOne", "MAThree", "MAFive", "MAWeek"])


#open twitter handles of projects we are looking at
with open('Projects - Historic Data.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    list_of_rows = list(csv_reader)
    projects_list = np.array(list_of_rows)
    projects_list = projects_list[1:]

projects_list = projects_list[9:12]

#open existing list of account info
with open('Historic_Info.csv', 'r') as account_file:
    account_reader = csv.reader(account_file)
    account_list = list(account_reader)
    account_list = np.array(account_list)

#convert account info to dataframe
fullDataframe = pd.DataFrame(account_list[1:], columns=account_list[0])

userDataCols = np.array(['screen_name', 'id', 'followers_count', 'following_count'])
#fullDataframe['screen_name'].str.contains(my_name).any()

#timezone used for date calculations
timezone = pytz.timezone('America/New_York')

for project in projects_list:
    my_name = project[1][20:]
    my_date = project[3]
    my_time = '12:00 AM'

    if my_date == '':
        print("Need to add time for "+str(project[0]))
        continue
    
    this_datetime_obj = datetime.strptime(my_date+my_time, '%m/%d/%Y%I:%M %p').replace(tzinfo=timezone)
    time_rn = datetime.now().astimezone(tz=timezone)

    if fullDataframe['screen_name'].str.contains(my_name).any():
        None
    else:

        print("Adding "+my_name+" to dataframe")
        #add basic nft data to dataframe
        user_data = get_user_data(my_name)
        user_data_df = pd.DataFrame([user_data], columns = userDataCols)

        #add tweet metrics to dataframe
            #collect tweets from the time of this running
        #ask if I need to collect tweet data
        my_response = input("Should twitter data be collected? (y/n): ")
        if my_response == 'y':
            get_tweet_data(my_name, user_data[1])
        if my_response =='n':
            None
        #run tweet metrics
        tweet_df = get_tweet_metrics('nft_tweets/'+str(my_name)+'.csv')

        #add time of collection to dataframe
        collection_date = pd.to_datetime('now')
        collection_time_df = pd.DataFrame([collection_date], columns=['collection_date'])

        #add influencer metrics to the dataframe
        my_influencer_data = influencer_data(my_name)
        influencer_df = pd.DataFrame([my_influencer_data], columns=['total_influencer_following', 'regularized_influencer_following'])

        new_nft_df = user_data_df.join(collection_time_df).join(tweet_df).join(influencer_df)

        #add price of ETH at mint to dataframe


        movingAverageEth = get_moving_average_crypto(this_datetime_obj)
        movingAverageEth_df = pd.DataFrame(movingAverageEth, columns=['MAOne','MAThree','MAFive','MAWeek'])
        new_nft_df = new_nft_df.join(movingAverageEth)
        #add new dataframe to full dataframe
        fullDataframe = fullDataframe.append(new_nft_df)

        
fullDataframe.to_csv('Historic_Info.csv', index=False)