import requests
import numpy as np
import csv
import pandas as pd

current_offset = 100

url = f"https://api.opensea.io/api/v1/collections?offset={current_offset}&limit=2"

headers = {"Accept": "application/json"}

response = requests.get(url, headers=headers)
response_json = response.json()['collections'][0]



df = pd.read_csv('OpenseaScrapedNFTs.csv', index_col=0)
print(df)