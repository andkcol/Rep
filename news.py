import yfinance as yf
import pandas as pd
from textblob import TextBlob
import schedule
import time
import os

CSV_FILE = "apple_news_sentiment.csv"

def fetch_news_sentiment():
    #Fetches Apple (AAPL) news, analyzes sentiment, and appends only unique entries to a CSV file.
    
    # Get news from Yahoo Finance
    ticker = yf.Ticker("AAPL")
    news = ticker.news  # Fetch news data

    if not news:
        print("No news found for AAPL.")
        return

    data = []

    for article in news:
        # Ensure article has 'content' field
        content = article.get("content", {})
        if not isinstance(content, dict):
            continue  # Skip invalid entries
        
        # Extract relevant fields
        title = content.get("title", "").strip()
        link = content.get("canonicalUrl", {}).get("url", "").strip()
        publisher = content.get("provider", {}).get("displayName", "Unknown").strip()
        pub_date = content.get("pubDate", "")

        # Convert date format
        date = pd.to_datetime(pub_date) if pub_date else pd.NaT

        # Ensure we have valid data
        if not title or not link or not publisher:
            continue  # Skip invalid entries

        # Sentiment analysis using TextBlob
        sentiment = round(TextBlob(title).sentiment.polarity, 3)  # Rounded to 3 decimal places


        data.append([date, title, publisher, link, sentiment])

    # Convert new data to DataFrame
    if not data:
        print("No valid news articles found.")
        return
    
    new_df = pd.DataFrame(data, columns=["Date", "Title", "Publisher", "Link", "Sentiment"])
    
    # Ensure datetime is formatted correctly
    new_df["Date"] = pd.to_datetime(new_df["Date"]).dt.strftime("%Y-%m-%d")

    # Load existing CSV to check for duplicates
    if os.path.exists(CSV_FILE):
        existing_df = pd.read_csv(CSV_FILE)
        existing_links = set(existing_df["Link"])  # Store existing links for quick lookup

        # Filter out duplicate entries
        new_df = new_df[~new_df["Link"].isin(existing_links)]

    # If no new data remains after filtering, exit early
    if new_df.empty:
        print("No new unique articles to add.")
        return

    # Append only unique data to CSV
    new_df.to_csv(CSV_FILE, mode='a', header=not os.path.exists(CSV_FILE), index=False)

    print(f"Added {len(new_df)} unique news articles to {CSV_FILE}")

# Schedule the task to run daily
schedule.every().day.at("09:00").do(fetch_news_sentiment)  # Adjust time as needed

if __name__ == "__main__":
    fetch_news_sentiment()  # Run once when script starts
    while True:
        schedule.run_pending()
        time.sleep(60)  # Wait 1 minute before checking again
