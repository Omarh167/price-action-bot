import ccxt
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from datetime import datetime

# Initialize exchange
exchange = ccxt.binance()

# Parameters
symbol = 'BTC/USDT'
timeframe = '1m'
limit = 100
save_file = 'btc_live_data.csv'

# Create CSV file if it doesn't exist
try:
    df_existing = pd.read_csv(save_file)
except FileNotFoundError:
    df_existing = pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df_existing.to_csv(save_file, index=False)

# Fetch new data
def fetch_data():
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# Update and save data
def update_data():
    global df_existing
    new_df = fetch_data()
    df_existing = pd.concat([df_existing, new_df]).drop_duplicates(subset='timestamp', keep='last')
    df_existing.to_csv(save_file, index=False)
    return df_existing

# Live chart setup
fig, ax = plt.subplots()
plt.title(f"Live BTC/USDT Chart ({timeframe})", fontsize=14)
plt.xlabel("Time")
plt.ylabel("Price (USD)")

def animate(i):
    df = update_data()
    ax.clear()
    ax.plot(df['timestamp'], df['close'], label='BTC Price', linewidth=2)
    df['MA20'] = df['close'].rolling(window=20).mean()
    ax.plot(df['timestamp'], df['MA20'], label='MA 20', linestyle='--', color='orange')
    ax.legend(loc='upper left')
    ax.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

ani = animation.FuncAnimation(fig, animate, interval=5000)
plt.show()

