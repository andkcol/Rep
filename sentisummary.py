import pandas as pd

CSV_FILE = "apple_news_sentiment.csv"
OUTPUT_FILE = "apple_sentiment_summary.csv"

def process_sentiment_data():
    #Reads the Apple news sentiment CSV and calculates daily sentiment totals & 7-day moving average.
    
    # Load CSV
    try:
        df = pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        print(f"Error: {CSV_FILE} not found.")
        return
    except pd.errors.EmptyDataError:
        print(f"Error: {CSV_FILE} is empty.")
        return

    # Ensure Date column is in datetime format
    df["Date"] = pd.to_datetime(df["Date"])

    # Group by day and sum sentiment scores
    daily_sentiment = df.groupby(df["Date"].dt.date)["Sentiment"].sum().reset_index()

    # Rename columns for clarity
    daily_sentiment.columns = ["Date", "Total Sentiment"]

    # Convert Date back to datetime format for sorting
    daily_sentiment["Date"] = pd.to_datetime(daily_sentiment["Date"])
    daily_sentiment = daily_sentiment.sort_values("Date")

    # Calculate 7-day moving average
    daily_sentiment["7-Day MA"] = daily_sentiment["Total Sentiment"].rolling(window=7, min_periods=1).mean()

    # Save to a new CSV file
    daily_sentiment.to_csv(OUTPUT_FILE, index=False)

    print(f"Sentiment summary saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    process_sentiment_data()
