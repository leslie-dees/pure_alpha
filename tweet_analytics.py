from pickle import TRUE
import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
"""
vars to get:
time between posts STILL NEED TO DO
average posts per day STILL NEED TO DO
"""
#Retweet if RT at beginning of text
#Retweet if this_is_reply is TRUE
def get_tweet_metrics(my_csv_location):

    with open(my_csv_location, 'r') as csv_file:
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
    
    
    df = pd.DataFrame()
    df['my_retweets'] = [no_retweets_retweet_count]
    df['rt_retweets'] = [retweets_retweet_count]
    df['my_replies'] = [no_retweets_replies_count]
    df['rt_replies'] = [retweets_replies_count]
    df['my_likes'] = [no_retweets_likes_count]
    df['rt_likes'] = [retweets_likes_count]
    return df


#metrics = get_tweet_metrics('nft_data/cartoonsnft.csv')
#print(metrics)