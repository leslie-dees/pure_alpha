# Import Libraries
import requests
import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
# The CoinDesk 20
coindesk20_list = ['ETH']
raw_df = pd.DataFrame()
for coin in coindesk20_list:
    coin_df = pd.DataFrame()
    df = pd.DataFrame(index=[0])
    
    # Define the Start Date and End Date
    end_datetime = datetime(2022, 5, 19, 0, 0)
    datetime_checkpt = datetime(2022, 5, 18, 0, 0)
    
    while len(df) > 0:
        if end_datetime == datetime_checkpt:
            break
        start_datetime = end_datetime - relativedelta(hours = 12)
        url = 'https://production.api.coindesk.com/v2/price/values/' + coin + '?start_date=' + start_datetime.strftime("%Y-%m-%dT%H:%M") + '&end_date=' + end_datetime.strftime("%Y-%m-%dT%H:%M") + '&ohlc=true'
        temp_data_json = requests.get(url)
        temp_data = temp_data_json.json()
        df = pd.DataFrame(temp_data['data']['entries'])
        df.columns = ['Timestamp', 'Open', 'High', 'Low', 'Close']
        
        # Handle the Missing Data
        insert_idx_list = [np.nan]
        while len(insert_idx_list) > 0:
            timestamp_checking_array = np.array(df['Timestamp'][1:]) - np.array(df['Timestamp'][:-1])
            insert_idx_list = np.where(timestamp_checking_array != 60000)[0]
            if len(insert_idx_list) > 0:
                print('There are ' + str(len(insert_idx_list)) + ' timestamp mismatched.')
                insert_idx = insert_idx_list[0]
                temp_df = df.iloc[insert_idx.repeat(int(timestamp_checking_array[insert_idx]/60000)-1)].reset_index(drop=True)
                temp_df['Timestamp'] = [temp_df['Timestamp'][0] + i*60000 for i in range(1, len(temp_df)+1)]
                df = df.loc[:insert_idx].append(temp_df).append(df.loc[insert_idx+1:]).reset_index(drop=True)
                insert_idx_list = insert_idx_list[1:]
        
        df = df.drop(['Timestamp'], axis=1)
        df['Datetime'] = [end_datetime - relativedelta(minutes=len(df)-i) for i in range(0, len(df))]
        coin_df = df.append(coin_df)
        end_datetime = start_datetime
    coin_df['Symbol'] = coin
    raw_df = raw_df.append(coin_df)
raw_df = raw_df[['Datetime', 'Symbol', 'Open', 'High', 'Low', 'Close']].reset_index(drop=True)

raw_df.to_csv('raw_df.csv', index=False)