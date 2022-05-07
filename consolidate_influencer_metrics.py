import pandas as pd
import glob
import csv
import numpy as np

path = r'C:\Users\lesli\Desktop\vectr_ai\influencer_followings'
all_files= glob.glob(path+"/*.csv")

li = []
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header = 0)
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)
frame.to_csv('full_influencer_dataset.csv')

with open('Account_Info.csv', 'r') as filename:
    csv_reader = csv.reader(filename)
    my_list = list(csv_reader)
    my_list = np.array(my_list)
#print(my_list)

with open('Influencer_id_whitelist.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    list_of_rows = list(csv_reader)
    list_of_rows = np.array(list_of_rows)
    influencer_tot_list = list_of_rows[1:]

influencer_data_use = {}
for thing in influencer_tot_list:
    influencer_data_use[thing[1]] = int(thing[3])

max_val = max(influencer_data_use.values())

for key in influencer_data_use.keys():
    influencer_data_use[key] = influencer_data_use[key]/max_val
influencer_cols = ['influencer_follow_count', 'regularized_influencer_follows']


total_influencer_followings = []
for each_nft in my_list:
    true_count = 0
    regularized_count = 0
    my_nft_array = [each_nft[1]]
    my_name = each_nft[1]
    for i in range(len(frame)):
        if frame['nft_name'].iloc[i] == my_name:
            if frame['is_influencer_following'].iloc[i] == True:
                true_count+=1
                this_influencer = frame['influencer_name'].iloc[i]
                regularized_count += influencer_data_use[this_influencer]

    my_nft_array.append(true_count)
    my_nft_array.append(regularized_count)
    total_influencer_followings.append(my_nft_array)
total_influencer_followings = np.array(total_influencer_followings[1:])
this_df = pd.DataFrame(total_influencer_followings, columns = ['nft_name', 'total_following', 'regularized_following'])
this_df.to_csv('influencer_followings_by_nft.csv')