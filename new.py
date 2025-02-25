import csv
import requests
import os
from textblob import TextBlob
from datetime import datetime

# API Keys
ALPHA_VANTAGE_API_KEY = "TXAYZZLDCPD0Q9XS"
NEWS_API_KEY = "7c10f069074544178fc634da5bcdb094"

# List of Companies (Stock Tickers & Keywords)
COMPANIES = [
    {"ticker": "AAPL", "name": "Apple"},
    {"ticker": "GOOGL", "name": "Google"},
    {"ticker": "MSFT", "name": "Microsoft"},
    {"ticker": "AMZN", "name": "Amazon"},
    {"ticker": "META", "name": "Meta"},
    {"ticker": "TSLA", "name": "Tesla"},
    {"ticker": "NFLX", "name": "Netflix"},
    {"ticker": "NVDA", "name": "Nvidia"},
    {"ticker": "IBM", "name": "IBM"},
    {"ticker": "AMD", "name": "AMD"}
]

def fetch_alpha_vantage_news(ticker): # Fetch news from Alpha Vantage for a given stock ticker
    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("feed", [])
    return []

def fetch_news_api_news(company_name): # Fetch news from NewsAPI for a given company name
    url = f"https://newsapi.org/v2/everything?q={company_name}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("articles", [])
    return []

def process_news(news_data, source): # Process news articles and extracts required fields
    processed_news = []
    for item in news_data:
        title = item.get("title", "No Title")

        if source == "alpha_vantage":
            date_str = item.get("time_published", "")  # Example: '20250225T091200'
            if len(date_str) >= 8:  # Ensure there are enough characters
                try:
                    date = datetime.strptime(date_str[:8], "%Y%m%d").strftime("%d/%m/%Y")  # Extract YYYYMMDD
                except ValueError:
                    date = "Unknown"
            else:
                date = "Unknown"
        else:  # NewsAPI format
            date_str = item.get("publishedAt", "")
            if date_str:
                try:
                    date = datetime.strptime(date_str[:10], "%Y-%m-%d").strftime("%d/%m/%Y")
                except ValueError:
                    date = "Unknown"
            else:
                date = "Unknown"

        sentiment = TextBlob(title).sentiment.polarity
        processed_news.append((date, title, round(sentiment, 4), source))

    return processed_news

def read_existing_news(csv_file): # Reads existing news from the company's CSV file to prevent duplicates
    try:
        with open(csv_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            return {row[1] for row in reader}  # Store existing titles
    except FileNotFoundError:
        return set()

def save_news_to_csv(news, company_name): # Saves new non-duplicate news articles to the company's CSV file ordering by date
    csv_file = f"{company_name}_news_sentiment.csv"
    existing_titles = read_existing_news(csv_file)

    # Filter out duplicates
    unique_news = [entry for entry in news if entry[1] not in existing_titles]

    if not unique_news:
        print(f"No new articles to add for {company_name}.")
        return

    # Load existing data for sorting
    all_news = []
    if os.path.exists(csv_file):
        with open(csv_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header
            all_news = list(reader)

    # Add new data
    all_news.extend(unique_news)

    # Sort by date (column index 0) in ascending order
    all_news.sort(key=lambda x: datetime.strptime(x[0], "%d/%m/%Y"))

    # Write sorted data back to CSV
    with open(csv_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Title", "Sentiment", "Source"])  # Write header
        writer.writerows(all_news)

    print(f"Updated {csv_file} with {len(unique_news)} new articles.")

def main(): # Main function to fetch and save news sentiment for multiple companies
    for company in COMPANIES:
        ticker = company["ticker"]
        name = company["name"]
        
        print(f"Fetching news for {name} ({ticker})...")
        alpha_vantage_news = fetch_alpha_vantage_news(ticker)
        news_api_news = fetch_news_api_news(name)
        
        processed_alpha_vantage = process_news(alpha_vantage_news, "Alpha Vantage")
        processed_news_api = process_news(news_api_news, "News API")
        
        all_news = processed_alpha_vantage + processed_news_api
        save_news_to_csv(all_news, name)
    
    print("News sentiment data updated successfully.")

if __name__ == "__main__":
    main()
