import pandas as pd

# Load the CSV file
df = pd.read_csv("Temp/AAPL_test.csv")

# Convert 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'])

# Remove weekends (Saturday=5, Sunday=6)
df = df[~df['date'].dt.weekday.isin([5, 6])]

# Save the cleaned CSV
df.to_csv("filtered_file.csv", index=False)

print("Weekends removed and file saved as filtered_file.csv")
