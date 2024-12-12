import yfinance as yf

# Fetch Apple stock prices in 1 hour time frame over 60 days
aapl = yf.Ticker("AAPL")
data = aapl.history(period = "3mo", interval = "1h")

# Calculate the 12-period EMA
data['EMA12'] = data['Close'].ewm(span = 12, adjust = False).mean()

# Calculate the 26-period EMA
data['EMA26'] = data['Close'].ewm(span = 26, adjust = False).mean()

# Calculate MACD (difference between 12 and 26 period EMAs)
data['MACD'] = data['EMA12'] - data['EMA26']

# Calculate the Signal Line (9-period EMA of hte MACD)
data['Signal_Line'] = data['MACD'].ewm(span = 9, adjust = False).mean()

# Check for crossovers between MACD and Signal Line
last_row = data.iloc[-1]
second_last_row = data.iloc[-2]

if second_last_row['MACD'] > second_last_row['Signal_Line'] and last_row['MACD'] < last_row['Signal_Line']:
    print('Cross below signal line')
elif second_last_row['MACD'] < second_last_row['Signal_Line'] and last_row['MACD'] > last_row['Signal_Line']:
    print('Cross above signal line')
else:
    print('No Crossover')

print(aapl)