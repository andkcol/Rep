import csv
import yfinance as yf

ticker = "AAPL" # Pick the stock

stock = yf.Ticker(ticker) # Get the stock object

news = stock.news # Find news articles

# Save article details to a CSV file
with open("aapl_news.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Link", "Publisher", "Date"]) # Header
    # Article's details
    for article in news:
        writer.writerow([
            article['title'],
            article['publisher'], 
            article['providerPublishTime']
        ])