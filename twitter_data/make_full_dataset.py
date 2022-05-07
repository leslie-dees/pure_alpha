import tweet_analytics
import glob
import numpy as np
import pandas as pd
import csv
import datetime as dt
#RUN THIS IN ORDER TO CONSOLIDATE TWEET DATA WITH NFT METRICS


#add the twitter data to the total dataframe

def make_full_dataset(path):
    my_twitter_data_full = pd.DataFrame()

    for fname in glob.glob(path):
        metrics = tweet_analytics.get_tweet_metrics(fname)
        my_nft_twitter_name = fname[11:-4]
        metrics['my_nft_twitter_name'] = my_nft_twitter_name

        my_twitter_data_full = pd.concat([my_twitter_data_full, metrics])
    first_column = my_twitter_data_full.pop('my_nft_twitter_name')
    my_twitter_data_full.insert(0, 'my_nft_twitter_name', first_column)

    #add the nft metadata to the total dataframe
    with open('twitter_data/Projects_full.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        nft_metadata = list(csv_reader)
    nft_metadata = np.array(nft_metadata)

    useThisNFTdata = nft_metadata[:,[1, 4, 6, 7]]
    
    colnames = useThisNFTdata[0][1:]

    final_data = []
    for i in range(1, len(useThisNFTdata)):
        my_nft_name_here = useThisNFTdata[i][0][20:]
        my_nft_metadata = useThisNFTdata[i][1:]
        my_nft_metadata = np.insert(my_nft_metadata, 0, my_nft_name_here, axis=0)
        
        for j in range(len(my_twitter_data_full)):
            if my_nft_name_here == my_twitter_data_full.iloc[j]['my_nft_twitter_name']:

                this_row = my_twitter_data_full.iloc[j].to_numpy()
                my_nft_metadata = np.concatenate([my_nft_metadata, this_row[1:]])
        final_data.append(my_nft_metadata)
    final_data = np.array(final_data)

    with open('influencer_followings_by_nft.csv', 'r') as influencer_file:
        csv_reader_i = csv.reader(influencer_file)
        influencer_metadata = list(csv_reader_i)
    influencer_metadata = np.array(influencer_metadata)
    influencer_metadata = np.delete(influencer_metadata, 0, 1)
    influencer_metadata = influencer_metadata[1:]
    influencer_cols = ['nft_name', 'influencers_following', 'regularized_influencers_following']
    

    first_cols = useThisNFTdata[0]
    other_cols = my_twitter_data_full.columns.values.tolist()
    final_cols = np.append(first_cols, other_cols[1:])
    #final_cols = np.append(final_cols, influencer_cols[1:])


    final_dataframe = pd.DataFrame(final_data, columns = final_cols)
    final_dataframe['Launch date'] = pd.to_datetime(final_dataframe['Launch date'])
    final_dataframe['Launch date'] = final_dataframe['Launch date'].map(dt.datetime.toordinal)
    return final_dataframe

my_data = make_full_dataset(path = "nft_tweets\*.csv")
#print(my_data)
