# import libraries to make get request
import requests
import json
from dateutil import parser
import datetime
import numpy as np
import csv

h = {'authorization': 'MTUwNjkzNzU1OTMyOTAxMzc2.YTFB_Q.95nh5_MBkPLiF7kTgBW5iMGIIK4'}

# approximate_member_count (count of server members)
def get_approximate_member_count(server_id):
    r = requests.get('https://discord.com/api/guilds/' + str(server_id) + '/preview', headers=h)
    j = json.loads(r.text)
    if 'global' in j.keys():
        print("You are being rate limited, rerun this data!!!!!")
    else:
        return j['approximate_member_count']

# approximate_presence_count (count of currently online server members)
def get_approximate_presence_count(server_id):
    r = requests.get('https://discord.com/api/guilds/' + str(server_id) + '/preview', headers=h)
    j = json.loads(r.text)
    return j['approximate_presence_count']

# get the text content of the last messages posted to a specific channel/direct message
def get_last_messages_from_channel(channel_id):
    r = requests.get('https://discord.com/api/v9/channels/' + channel_id + '/messages?limit=100', headers=h)
    j = json.loads(r.text)
    m = [c['content'] for c in j]
    return m

def get_time_between_posts(channel_id):
    #returns the average time between the last 100 posts in the channel in minutes


    r = requests.get('https://discord.com/api/v9/channels/' + channel_id + '/messages?limit=100', headers=h)

    j = json.loads(r.text)
        
    times = [t['timestamp'] for t in j]
    total_dates = [parser.parse(x) for x in times]

    mydates = sorted(total_dates)

    time_diffs = []
    for i in range(len(mydates)-1):

        first_time = mydates[i+1]
        second_time = mydates[i]

        diff = first_time-second_time
        diff_secs = diff.total_seconds()
        diff_mins = diff_secs/60
        time_diffs.append(diff_mins)
        
    return np.average(time_diffs)