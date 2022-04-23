import config
import tweepy
import csv
import numpy as np
import pandas as pd

auth = tweepy.OAuthHandler(consumer_key=config.API_KEY, consumer_secret=config.API_KEY_SECRET)
auth.set_access_token(key=config.ACCESS_TOKEN, secret=config.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

with open('Influencer_id_whitelist.csv', 'r') as filename:
    csv_reader = csv.reader(filename)
    my_influencers = list(csv_reader)
    my_influencers = np.array(my_influencers)
    my_influencers = my_influencers[:, 1:]

with open('Account_Info.csv', 'r') as these_nfts:
    csv_reader = csv.reader(these_nfts)
    my_nfts = list(csv_reader)
    my_nfts = np.array(my_nfts)
    my_nfts = my_nfts[:, 1:]




col_names = ['nft_name', 'influencer_name', 'is_influencer_following']

total_nft_list = []
for nfts in my_nfts[1:, 0][17:]:
    this_nft_list = []
    for influencer in my_influencers[1:, 0]:
        this_friendship = []
        friendship = api.get_friendship(source_screen_name = influencer, target_screen_name = nfts)
        this_friendship.append(nfts)
        this_friendship.append(influencer)
        this_friendship.append(friendship[0].following)

        this_nft_list.append(this_friendship)
    print(str(nfts))
    this_nft_list = np.array(this_nft_list)
    nft_df = pd.DataFrame(this_nft_list, columns = col_names)
    nft_df.to_csv(str(nfts)+'_Followings.csv')

total_nft_list = np.array(total_nft_list)

df = pd.DataFrame(total_nft_list, columns = col_names)
df.to_csv('Influencer_Followings.csv')