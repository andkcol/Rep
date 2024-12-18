# Andrew Kane
# Trading bot moving averages

import pandas as pd

# Load dataset
data = pd.read_csv('AAPL1980.csv')

# Inspect first few rows, ensure data is read correctly
print(data.head())

# Remove missing values
data = data.dropna()

# Calculate moving averages
data['shortMA'] = data['close'].rolling(window = 13).mean()
data['longMA'] = data['close'].rolling(window = 21).mean()

# Inspect data
print(data[['close', 'shortMA', 'longMA']].tail())

# Create signal
data['Signal'] = 0
data.loc[data['shortMA'] > data['longMA'], 'Signal'] = 1 #Buy
data.loc[data['shortMA'] <= data['longMA'], 'Signal'] = -1 #Sell

# Ispect signals
print(data[['close', 'shortMA', 'longMA', 'Signal']].tail())

# BACKTESTING
# initialise backtesting variables
initial_balance = 10000
balance = initial_balance
positions = 0
data['Portfolio'] = 0 #Track portfolio value

for i in range(2, len(data)):
    if data['Signal'].iloc[i] == 1 and positions == 0: #Buy signal
        positions = balance / data['close'].iloc[i] #Buy as many shares as possible
        balance = 0
    elif data['Signal'].iloc[i] == -1 and positions > 0: #Sell signal
        balance = positions * data['close'].iloc[i] #Sell all shares
        positions = 0

    # Update portfolio value
    data['Portfolio'].iloc[i] = balance + (positions * data['close'].iloc[i])

# Final portfolio value
final_balance = balance + (positions * data['close'].iloc[-1])
print(f"Final portfolio value: {final_balance}")