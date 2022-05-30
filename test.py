from Historic_Crypto import HistoricalData
from datetime import datetime, timedelta
import pytz
import pandas as pd

def get_moving_average_crypto(mint_time):
    one_week_back = mint_time - timedelta(days = 7)
    #five_days_back = mint_time  - timedelta(days = 5)
    #three_days_back = mint_time - timedelta(days = 3)
    #one_day_back = mint_time - timedelta(days = 1)

    str_time_week = one_week_back.strftime('%Y-%m-%d-%H-%M')
    #str_time_five = five_days_back.strftime('%Y-%m-%d-%H-%M')
    #str_time_three = three_days_back.strftime('%Y-%m-%d-%H-%M')
    #str_time_one = one_day_back.strftime('%Y-%m-%d-%H-%M')
    
    data_week = HistoricalData('ETH-USD', 900, str_time_week, verbose = False).retrieve_data()
    data_five = data_week.drop(index=data_week.index[:192], axis=0, inplace = False)
    data_three = data_five.drop(index=data_five.index[:192], axis=0, inplace = False)
    data_one = data_three.drop(index=data_three.index[:192], axis=0, inplace = False)    

    averageEthPriceWeek = data_week["close"].mean()
    averageEthPriceFive = data_five["close"].mean()
    averageEthPriceThree = data_three["close"].mean()
    averageEthPriceOne = data_one["close"].mean()

    return pd.DataFrame([[averageEthPriceOne, averageEthPriceThree, averageEthPriceFive, averageEthPriceWeek]], columns=["MAOne", "MAThree", "MAFive", "MAWeek"])

#timezone used for date calculations
timezone = pytz.timezone('America/New_York')
time_rn = datetime.now().astimezone(tz=timezone)

thingy = get_moving_average_crypto(time_rn)
print(thingy)