import requests

url = f'https://eodhd.com/api/sentiments?s=tsla.us,aapl.us&from=2022-01-01&to=2022-04-22&api_token=67c0bd1ad182a2.20799335&fmt=json'
data = requests.get(url).json()

print(data)