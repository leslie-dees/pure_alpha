# import libraries to make get request
import requests
import json

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
    print(j)
    return m