import numpy as np
import csv
import pandas as pd
from datetime import datetime
import glob

#Retweet if RT at beginning of text
#Retweet if this_is_reply is TRUE
def get_tweet_metrics(my_csv_location):
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


#metrics = get_tweet_metrics('ailoverse.csv')
#print(metrics)
