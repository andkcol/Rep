import requests
import csv

ticker = "META"
url = f'https://eodhd.com/api/news?s={ticker}.us&api_token=67c0bd1ad182a2.20799335&fmt=json&limit=1000'
response = requests.get(url)

#Parse JSON response
try:
    data = response.json()
except requests.exceptions.JSONDecodeError:
    print("API didn't return valid JSON")
    print("Response:", response.text)
    exit()

#Ensure populated response
if not data:
    print("Empty response from API")
    exit()

#CSV file template
csv_file = f"{ticker}sentiment_data.csv"
fieldnames = ["date", "title", "polarity"]

#file creation & writing
with open(csv_file, mode = "w", newline = "", encoding = "utf-8") as file:
    writer = csv.DictWriter(file, fieldnames = fieldnames)
    writer.writeheader()

    row_count = 0

    for entry in data:
        writer.writerow({
            "date": entry.get("date", ""),
            "title":entry.get("title", ""),
            "polarity": entry.get("sentiment", {}).get("polarity", "")
        })
        row_count += 1

if row_count > 0:
    print(f"{row_count} rows written to {csv_file}")
else:
    print("No rows written to file")