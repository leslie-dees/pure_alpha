import requests

r5 = requests.get('https://api.opensea.io/api/v1/collection/rektguy')

request_json = r5.json()

keys = request_json['collection']


this_info = keys['stats']['count']
this_other_info = keys['stats']['total_supply']

print(this_info)
print(this_other_info)