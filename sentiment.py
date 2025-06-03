import csv
import requests
import os
from textblob import TextBlob
from datetime import datetime

AV_Key = "TXAYZZLDCPD0Q9XS"
NEWS_Key = "7c10f069074544178fc634da5bcdb094"

outputFolder = "Sentiment Data"
os.makedirs(outputFolder, exist_ok=True)

# Add multiple (ticker, company) pairs here
companies = [
    ("AMZN", "Amazon"),
    ("AMD", "AMD"),
    ("AAPL", "Apple"),
    ("NET", "Cloudflare"),
    ("FSLY", "Fastly"),
    ("GOOGL", "Google"),
    ("IBM", "IBM"),
    ("META", "Meta"),
    ("MSFT", "Microsoft"),
    ("NFLX", "Netflix"),
    ("NVDA", "Nvidia"),
    ("OKTA", "Okta"),
    ("PTON", "Pelaton"),
    ("ROKU", "Roku"),
    ("TSLA", "Tesla"),
    ("U", "Unity"),
    ("ZM", "Zoom")
]

def fetch_AV_news(ticker):
    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={AV_Key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("feed", [])
    return []

def fetch_news_API(company):
    url = f"https://newsapi.org/v2/everything?q={company}&apiKey={NEWS_Key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("articles", [])
    return []

def process_news(news_data, source):
    processed_news = []
    for item in news_data:
        title = item.get("title", "No Title")

        if source == "Alpha Vantage":
            date_str = item.get("time_published", "")
            try:
                date = datetime.strptime(date_str[:8], "%Y%m%d").strftime("%d/%m/%Y")
            except Exception:
                date = "Unknown"
        else:
            date_str = item.get("publishedAt", "")
            try:
                date = datetime.strptime(date_str[:10], "%Y-%m-%d").strftime("%d/%m/%Y")
            except Exception:
                date = "Unknown"

        sentiment = TextBlob(title).sentiment.polarity
        processed_news.append((date, title, round(sentiment, 4), source))
    return processed_news

def read_existing_data(csv_file):
    try:
        with open(csv_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            return {row[1] for row in reader}
    except FileNotFoundError:
        return set()

def save_news_to_csv(news, company):
    csv_file = os.path.join(outputFolder, f"{company}_news_sentiment.csv")
    existing_titles = read_existing_data(csv_file)
    unique_news = [entry for entry in news if entry[1] not in existing_titles]

    if not unique_news:
        print(f"No new articles found for {company}")
        return

    with open(csv_file, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if os.stat(csv_file).st_size == 0:
            writer.writerow(["Date", "Title", "Sentiment", "Source"])
        writer.writerows(unique_news)

    print(f"Updated {csv_file} with {len(unique_news)} new articles")

def main():
    for ticker, company in companies:
        print(f"\nFetching news for {company} ({ticker})...")
        av_news = fetch_AV_news(ticker)
        api_news = fetch_news_API(company)
        processed_av = process_news(av_news, "Alpha Vantage")
        processed_api = process_news(api_news, "News API")
        all_news = processed_av + processed_api
        save_news_to_csv(all_news, company)
    print("\nAll companies processed.")

if __name__ == "__main__":
    main()
