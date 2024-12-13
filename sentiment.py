import csv
import yfinance as yf

# Define the stock ticker
ticker = "AAPL"

# Get the Ticker object
stock = yf.Ticker(ticker)

# Fetch news articles
news = stock.news

# Save articles to a CSV file
with open("aapl_news.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(["Title", "Link", "Publisher", "Date"])
    # Write each article's details
    for article in news:
        writer.writerow([
            article['title'],
            article['publisher'], 
            article['providerPublishTime']
        ])