import requests

current_offset = 100

url = f"https://api.opensea.io/api/v1/collections?offset={current_offset}&limit=2"

headers = {"Accept": "application/json"}

response = requests.get(url, headers=headers)
response_json = response.json()['collections'][0]

print(response_json['stats'].keys())
