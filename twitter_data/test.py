import csv
import numpy as np
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
print(influencer_data_use)