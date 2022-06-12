import requests

r5 = requests.get('https://api.opensea.io/api/v1/collection/rektguy')

request_json = r5.json()

keys = request_json['collection']
eth_price = keys['payment_tokens'][0]['usd_price'] #this is insane! We instantly have eth price from this call


this_info = keys['stats']['count']
this_other_info = keys['stats']['total_supply']

#Most important opensea stats below (but basically everything is going to be helpful)
one_day_volume = stats["one_day_volume"] #volume in a given day 
one_day_change = stats["one_day_change"] #change in volume day over day
one_day_average_price = stats["one_day_average_price"] #average price traded today
average_price = stats["average_price"] #total average price. Thinking it would be good to see one day average price / total average price
thirty_day_average_price = stats["thirty_day_average_price"] #same as above
total_supply = stats["total_supply"] #super important - gets holder ratio with below stat
num_owners = stats["num_owners"] #gets holder ratio, which is extremely helpful for predicting demand
floor_price = stats["floor_price"]

#Not necessary stats
num_reports = stats["num_reports"]
count = stats["count"] #same as total supply

#print(keys)
#print(eth_price)
print(one_day_volume)