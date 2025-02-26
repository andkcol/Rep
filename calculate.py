import os
import pandas as pd

# Define paths
sentiment_data_folder = "Sentiment Data"
sentiment_summaries_folder = "Sentiment Summaries"

# Ensure the summaries folder exists
os.makedirs(sentiment_summaries_folder, exist_ok=True)

def process_sentiment_data():
    for file in os.listdir(sentiment_data_folder):
        if file.endswith(".csv"):
            file_path = os.path.join(sentiment_data_folder, file)
            stock_name = file.replace(".csv", "")
            
            # Load CSV
            df = pd.read_csv(file_path, parse_dates=['Date'])
            
            # Ensure 'date' column is in datetime format and sort by date
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.sort_values('Date')
            
            # Group by date and calculate daily average sentiment score
            summary_df = df.groupby('Date')['Sentiment'].mean().round(3).reset_index()
            summary_df.rename(columns={'Sentiment': 'Average Score'}, inplace=True)
            
            # Calculate 7-day moving average
            summary_df['7 MA'] = summary_df['Average Score'].rolling(window=7).mean().round(3)
            
            # Save to Sentiment Summaries folder
            summary_file_path = os.path.join(sentiment_summaries_folder, f"{stock_name}_summary.csv")
            summary_df.to_csv(summary_file_path, index=False)
            print(f"Processed and saved summary for {stock_name}")

if __name__ == "__main__":
    process_sentiment_data()