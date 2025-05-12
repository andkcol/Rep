import os
import pandas as pd

# Define paths
input_folder = "Sentiment Data"
output_folder = "Sentiment Summaries"

# Ensure the summaries folder exists
os.makedirs(output_folder, exist_ok=True)

def process_sentiment_data():
    for filename in os.listdir(input_folder):
        if filename.endswith("_news_sentiment.csv"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename.replace("_news_sentiment.csv", "_summary.csv"))

            # Load data
            df = pd.read_csv(input_path)

            # Group by date and calculate daily average sentiment
            summary = df.groupby("Date")["Sentiment"].mean().round(3).reset_index()
            summary.rename(columns={"Sentiment": "Average Score"}, inplace=True)

            # Add 7-day moving average
            summary["7 MA"] = summary["Average Score"].rolling(window=7).mean().round(3)

            # Save the result
            summary.to_csv(output_path, index=False)
            print(f"Processed {filename} -> {output_path}")

if __name__ == "__main__":
    process_sentiment_data()

    