from Historic_Crypto import HistoricalData
from datetime import datetime, timedelta
import pytz
import pandas as pd
import numpy as np

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

    return pd.DataFrame([np.array([averageEthPriceOne, averageEthPriceThree, averageEthPriceFive, averageEthPriceWeek])], columns=["MAOne", "MAThree", "MAFive", "MAWeek"])

#timezone used for date calculations
timezone = pytz.timezone('America/New_York')
time_rn = datetime.now().astimezone(tz=timezone)

my_time = ['5/4/2022','10:00 PM']

this_datetime_obj = datetime.strptime(my_time[0]+my_time[1], '%m/%d/%Y%I:%M %p').replace(tzinfo=timezone)

thingy = get_moving_average_crypto(this_datetime_obj)
print(thingy)