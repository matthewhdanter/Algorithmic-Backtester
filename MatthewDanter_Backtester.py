# Matthew Danter - 8/6/2026 - Backtester
import numpy as np
import pandas as pd

# A backtester applies a trading strategy to historical market data to see how said strategy would perform
# For this backtester, I will implement a moving average crossover
# I will find the short and long term averages, and determine when they cross over one another to signal to buy or sell

# The name of the file containing historical data:
file = 'example5.csv'

# Amount of money to simulate with, in whatever currency the share is being traded as, a flat brokerage fee, and a slippage rate:
wallet = 10000
brokerage = 1
slippage = 0.001 # This accounts for the fact that you wont get the trades at the exact price you see

# Short and long term average lengths (days):
short = 50
long = 200

# Read in the file:
data = pd.read_csv(file)
data = data[::-1].reset_index(drop = True) # My testing files all started with the most recent day at the top, so this flips them.

# Find the moving averages and append to data:
data['ShortMA'] = data['Close'].rolling(window = short).mean()
data['LongMA'] = data['Close'].rolling(window = long).mean()

# Find when short crosses above long (buy) and below (sell):
# A buy signal (BS) happens when the short crosses above the long, when ShortMA > LongMA, the first time (the previous ShortMA < LongMA)
data['BS'] = (data['ShortMA'] > data['LongMA']) & (data['ShortMA'].shift(1) < data['LongMA'].shift(1))

# A buy signal will also appear on the first day the LongMA is calculated, if the ShortMA > LongMA
if data['ShortMA'].values[long - 1] > data['LongMA'].values[long - 1]:
    data.loc[long -1, 'BS'] = True

# A sell signal (SS) happens on the opposite:
data['SS'] = (data['ShortMA'] < data['LongMA']) & (data['ShortMA'].shift(1) > data['LongMA'].shift(1))

# Now, I will create a column of pure action, where a 1 is Buy, a 0 is hold, and a -1 is sell:
data['Action'] = data['BS'].astype(int) - data['SS'].astype(int)

# No action will happen on the final day since the price to buy (the following day) is not known:
data['Action'].values[-1] = 0

# To minimize computational expense, I will create a new dataframe of just action:
action = pd.DataFrame(data[data['Action'] != 0]['Action'])

# Now that the buy and sell signals have been determined, I can create the simulation:
# In order to be most realistic, the simulation should operate as follows:
# The strategy determines a buy or sell signal using the closing price, the trade will be executed first thing the following day, at the opening price.

# Now I can index through the Action dataframe and execute trades while keeping a compelte record in the data dataframe:
# Initialize:
price = None # The price that a trade is being executed at
quantity = 0 # The amount of shares owned
data['Quantity'] = np.nan
data['Cash'] = np.nan
data.loc[0, 'Cash'] = wallet
wl = 0 # This will be used to find the win/loss ratio
wins = 0
losses = 0
for row in action.itertuples():
    wallet -= brokerage
    if row.Action == 1:
        # When buying, find the price, find the maximum we can afford, and subtract the value from our total cash
        price = (data.loc[(row.Index + 1), 'Open']) * (1 + slippage)
        quantity = np.floor(wallet / price)
        wl = quantity * price + brokerage
        wallet -= (quantity * price)
    else:
        # When selling, find the price and sell everything. The win or loss counter will be updated at each sell too.
        price = (data.loc[(row.Index + 1), 'Open']) * (1 - slippage)
        wallet += quantity * price
        wl -= quantity * price - brokerage
        quantity = 0
        
        # Update the win/loss ratio:
        if wl < 0:
            wins += 1
        elif wl > 0:
            losses += 1

    # Update the record
    data.loc[(row.Index + 1), 'Quantity'] = quantity
    data.loc[(row.Index + 1), 'Cash'] = wallet

# On first day, no shares are owned. Fill in the missing values in 'Quanity' and 'Cash' columns:
data.loc[0, 'Quantity'] = 0
data = data.ffill()

# Now calculate the total portfolio value each day:
data['Total Value'] = data['Cash'] + (data['Quantity'] * data['Close'])

# Find the max drawdown:
# Find the running maximum:
data['Running Max'] = data['Total Value'].cummax()
data['Drawdown'] = (data['Total Value'] - data['Running Max']) / data['Running Max']

# Save data as a csv file and print the win/loss ratio and maximum drawdown:
data.to_csv('exout.csv')
print('\n', 'Wins: ', wins, '\n', 'Losses: ', losses)
if losses > 0:
    print('\n', 'Win to Loss Ratio: ', wins/losses)
print('\n', 'Maximum Percentage Drawdown: ', abs(min(data['Drawdown']) * 100), '%')