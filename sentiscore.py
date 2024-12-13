from textblob import TextBlob
import pandas as pd

# Load CSV data
csv_file = "aapl_news.csv"
data = pd.read_csv(csv_file)

# Add a sentiment score for each article
def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity  # Polarity ranges from -1 (negative) to 1 (positive)

data['Sentiment_Score'] = data['Title'].apply(lambda x: analyze_sentiment(str(x)))

# Save results to a new CSV
output_file = "aapl_news_with_sentiment.csv"
data.to_csv(output_file, index=False)

print(f"Sentiment analysis completed. Results saved to {output_file}.")
