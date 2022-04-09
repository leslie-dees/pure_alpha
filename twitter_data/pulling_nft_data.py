import pull_data_from_twitter
import csv
import numpy as np
import pandas as pd

#RUN THIS TO COLLECT CSV DATA

#Open twitter handles of projects we are looking at
with open('twitter_data/Projects.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    list_of_rows = list(csv_reader)
    
#Get twitter screen names of twitter handles
list_of_rows = np.array(list_of_rows)
twitter_handles_list = list_of_rows[1:, 1]
twitter_names_list = []
for twitter_name in twitter_handles_list:
    twitter_names_list.append(twitter_name[20:])

#Get twitter ids from screen names
screen_and_id_list = []
for screen_name in twitter_names_list:
    my_screen_and_id = pull_data_from_twitter.get_user_data(screen_name)
    screen_and_id_list.append(my_screen_and_id)

#Put twitter info into csv
col_names = ['screen_name', 'id', 'followers', 'following']
df = pd.DataFrame(screen_and_id_list, columns=col_names)
df.to_csv('Account_Info.csv')

#Get tweets data from twitter ids
for my_ids in screen_and_id_list:
    pull_data_from_twitter.get_tweet_data(my_ids)
    print("Data collected from..."+str(my_ids[0]))
