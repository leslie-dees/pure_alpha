import requests
import numpy as np
import pandas as pd

all_collections_df = pd.DataFrame(columns= ['Project Name', 'Twitter', 'Opensea Link', 'Launch Date'])

current_offset = 0
while current_offset <= 50000:
    url = f"https://api.opensea.io/api/v1/collections?offset={current_offset}&limit=300"
    current_offset+=300
    print(f"Current Offset: {current_offset}")

    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers)

    response_json = response.json()

    all_collections = response_json['collections']

    for collection in all_collections:
        if collection['twitter_username'] is None:
            None
        if (collection['stats']['one_day_volume'] > 0.1) & (collection['stats']['num_owners'] > 50):
            twitter_username = collection['twitter_username']
            slug = collection['slug']
            print(slug)

            created_date = collection['created_date']
            created_year = created_date[0:4]
            created_month = int(created_date[5:7])
            created_day = int(created_date[8:10])

            datetime_format = f"{created_month}/{created_day}/{created_year}"

            this_url = f"https://opensea.io/collection/{slug}"
            NFT_feats = [slug, twitter_username, this_url, datetime_format]
            this_NFT = pd.DataFrame([np.array(NFT_feats)], columns = ['Project Name', 'Twitter', 'Opensea Link', 'Launch Date'])
            
            if slug not in all_collections_df.values:
                all_collections_df = all_collections_df.append(this_NFT, ignore_index = True)
    

all_collections_df.to_csv("OpenseaScrapedNFTs.csv")
        

# 'twitter_username