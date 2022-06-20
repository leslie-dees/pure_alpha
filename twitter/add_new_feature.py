from matplotlib.pyplot import hist
import numpy as np
import csv
import pandas as pd
import tweepy
import config as config
import discord_message_collection as dmc
import pytz
from Historic_Crypto import HistoricalData
import requests

#console_response = input("Adding features to old or new data? (old/new/exit): ")
console_response = 'old'
proceed_from_console = 0
while proceed_from_console != 1:
    if console_response == "old":
        with open('Projects - Historic Data.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            list_of_rows = list(csv_reader)
            projects_list = np.array(list_of_rows)
            projects_list = projects_list[1:]
        
        with open('Historic_Info.csv', 'r') as account_file:
            account_reader = csv.reader(account_file)
            account_list = list(account_reader)
            account_list = np.array(account_list)

        proceed_from_console = 1
        databaseType = 'old'

    elif console_response == "new":
        with open('Projects - Upcoming Projects (ETH).csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            list_of_rows = list(csv_reader)
            projects_list = np.array(list_of_rows)
            projects_list = projects_list[1:]


        #open existing list of account info
        with open('Account_Info.csv', 'r') as account_file:
            account_reader = csv.reader(account_file)
            account_list = list(account_reader)
            account_list = np.array(account_list)
        
        proceed_from_console = 1
        databaseType = 'new'

    elif console_response == "exit":
        quit()
    

#convert account info to dataframe
fullDataframe = pd.DataFrame(account_list[1:], columns=account_list[0])

#insert new functions to add features right here
def add_opensea_features(opensea_url):
    index_of_collection = opensea_url.index('.io') + 4
    collection = opensea_url[index_of_collection:]
    my_collection = "https://api.opensea.io/api/v1/%s" % (collection)
    
    my_request = requests.get(my_collection).json()
    features = my_request['collection']

    features_to_add = {
        'one_day_volume': features['stats']['one_day_volume'],
        'one_day_change': features['stats']['one_day_change'],
        'one_day_average_price': features['stats']['one_day_change'],
        'average_price': features['stats']['average_price'],
        'thirty_day_average_price': features['stats']['thirty_day_average_price'],
        'total_supply': features['stats']['total_supply'],
        'num_owners': features['stats']['total_supply'],
        'floor_price': features['stats']['floor_price'],
        'is_subject_to_whitelist': features['is_subject_to_whitelist'],
        'featured': features['featured']        
    }
    dct = {k:[v] for k,v in features_to_add.items()}
    opensea_df = pd.DataFrame(dct)
    return opensea_df


df = pd.DataFrame()
account_indices_used = []
for i in range(len(account_list[1:, 0])):
    this_project_entry = account_list[i, 0]

    for j in range(len(projects_list[:, 1])):
        unentered_database_entry = projects_list[j, 1][(projects_list[j, 1].index('.com')+5):]
        
        if (unentered_database_entry == this_project_entry) & (i not in account_indices_used):
            account_indices_used.append(i)
            opensea_id = projects_list[j, 2]
            this_opensea_object = add_opensea_features(opensea_id)
            df = df.append(this_opensea_object)

df.to_csv('opensea_test_data.csv', index=False)


print(account_indices_used)

#print(account_indices_used)