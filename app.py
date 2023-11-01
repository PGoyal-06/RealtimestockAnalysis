import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.dates as mdates
import numpy as np
import requests

st.title('Real-time Stock Market Dashboard')
# Ask user for the ticker symbols
ticker_symbols = st.text_input("Enter ticker symbols separated by comma:", 'AAPL,MSFT')
# We'll show data for last N days
n_days = st.slider('Enter number of days:', 1, 100, 30)
# Download data for all stocks and store in dictionary
response = requests.get(f'http://localhost:8501/data/{ticker_symbols}')
print(f"Server response: {response.text}")  # Check the server response
data = response.json()
ticker_data = {}
for ticker_symbol in ticker_symbols.split(','):
    ticker_data[ticker_symbol] = pd.DataFrame(data[ticker_symbol])
# Show the data in a line chart
st.subheader('Closing Prices Over Time')
fig1, ax1 = plt.subplots()
for ticker_symbol, data in ticker_data.items():
    ax1.plot(data.index, data.Close, label=ticker_symbol)
plt.legend()
plt.xlabel('Date')
plt.ylabel('Price')
st.pyplot(fig1)
# Show volume of stocks traded each day
st.subheader('Volume of Stocks Traded Each Day')
fig2, ax2 = plt.subplots()
for ticker_symbol, data in ticker_data.items():
    ax2.bar(data.index, data.Volume, label=ticker_symbol)
plt.legend()
plt.xlabel('Date')
plt.ylabel('Volume')
st.pyplot(fig2)
st.subheader('Statistics')
for ticker_symbol, data in ticker_data.items():
    st.write(f"Statistics for {ticker_symbol}:")
    st.table(data.describe())
st.subheader('Predictive Analysis')
fig3, ax3 = plt.subplots()
for ticker_symbol, data in ticker_data.items():
    X = mdates.date2num(data.index.to_pydatetime()).reshape(-1, 1)  # Convert dates to ordinal numbers
    y = data.Close.values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    ax3.scatter(X_test, y_test, color='black')
    ax3.plot(X_test, predictions, linewidth=3)
ax3.set_xlabel('Date')
ax3.set_ylabel('Stock Price')
ax3.set_title('Predicted vs Actual Stock Prices')
st.pyplot(fig3)
st.subheader('Risk Analysis')
volatilities = {}
for ticker_symbol, data in ticker_data.items():
    returns = np.log(data['Close'] / data['Close'].shift(1))
    volatility = returns.std() * np.sqrt(252)  # Annualize the standard deviation
    volatilities[ticker_symbol] = volatility
# Plot volatilities
fig4, ax4 = plt.subplots()
ax4.bar(volatilities.keys(), volatilities.values())
ax4.set_xlabel('Ticker Symbol')
ax4.set_ylabel('Volatility')
ax4.set_title('Volatility (Risk) for Each Stock')
st.pyplot(fig4)