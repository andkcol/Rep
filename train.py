import pandas as pd

# Load dataset
data = pd.read_csv("trainingdata.csv") 

# Clean the data
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()

# Normalise price and volume fields
data[['price', 'volume']] = scaler.fit_transform(data[['price', 'volume']])

# Split hte data 70% training
from sklearn.model_selection import train_test_split
X = data.drop(columns = ['Date', 'Close', 'Volume', 'Open', 'High', 'Low', '12 EMA', '26 EMA', 'Histogram'])
y = data['MACD', '9 EMA MACD']
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size = 0.3, random_state = 42)
X_val, X_test, y_val, y_test, train_test_split(X_temp, y_temp, test_size = 0.5, random_state = 42)