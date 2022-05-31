import numpy as np
import csv
import pandas as pd
from datetime import datetime, timedelta
from pyparsing import col
import tweepy
import config as config
import discord_message_collection as dmc
import pytz
from Historic_Crypto import HistoricalData

#open twitter handles of projects we are looking at
with open('Projects - Upcoming Projects.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    list_of_rows = list(csv_reader)
    projects_list = np.array(list_of_rows)
    projects_list = projects_list[1:]



#open existing list of account info
with open('Account_Info.csv', 'r') as account_file:
    account_reader = csv.reader(account_file)
    account_list = list(account_reader)
    account_list = np.array(account_list)

#convert account info to dataframe
fullDataframe = pd.DataFrame(account_list[1:], columns=account_list[0])

userDataCols = np.array(['screen_name', 'id', 'followers_count', 'following_count'])
#fullDataframe['screen_name'].str.contains(my_name).any()

#timezone used for date calculations
timezone = pytz.timezone('America/New_York')


def get_moving_average_crypto(mint_time):
    one_week_back = mint_time - timedelta(days = 7)
    #five_days_back = mint_time  - timedelta(days = 5)
    #three_days_back = mint_time - timedelta(days = 3)
    #one_day_back = mint_time - timedelta(days = 1)

    str_time_week = one_week_back.strftime('%Y-%m-%d-%H-%M')
    print(str_time_week)
    strMintTime = mint_time.strftime('%Y-%m-%d-%H-%M')
    #str_time_five = five_days_back.strftime('%Y-%m-%d-%H-%M')
    #str_time_three = three_days_back.strftime('%Y-%m-%d-%H-%M')
    #str_time_one = one_day_back.strftime('%Y-%m-%d-%H-%M')
    
    data_week = HistoricalData('ETH-USD', 900, start_date = str_time_week, end_date = strMintTime, verbose = False).retrieve_data()
    data_five = data_week.drop(index=data_week.index[:192], axis=0, inplace = False)
    data_three = data_five.drop(index=data_five.index[:192], axis=0, inplace = False)
    data_one = data_three.drop(index=data_three.index[:192], axis=0, inplace = False)    

    averageEthPriceWeek = data_week["close"].mean()
    averageEthPriceFive = data_five["close"].mean()
    averageEthPriceThree = data_three["close"].mean()
    averageEthPriceOne = data_one["close"].mean()

    return np.array([averageEthPriceOne, averageEthPriceThree, averageEthPriceFive, averageEthPriceWeek])

newFeatsDF = pd.DataFrame(columns = ['MAOne', 'MAThree', 'MAFive', 'MAWeek'])

for project in projects_list:
    #add new feature stuff here
    my_name = project[1][20:]
    my_date = project[4]
    my_time = project[5]
    
    
    this_datetime_obj = datetime.strptime(my_date+my_time, '%m/%d/%Y%I:%M %p').replace(tzinfo=timezone)
    time_rn = datetime.now().astimezone(tz=timezone)
    time_diff = this_datetime_obj - time_rn

    if time_diff < timedelta(hours=0):
        this_movingAverage = get_moving_average_crypto(this_datetime_obj)
        newFeatsDF.loc[len(newFeatsDF)] = this_movingAverage

#newFeatsDF = pd.DataFrame([newFeatsArray], columns = ['MAOne', 'MAThree', 'MAFive', 'MAWeek'])

newFeatsDF.to_csv('newFeaturesTest.csv', index=False)