# https://www.linkedin.com/pulse/bitcoin-price-forecasting-monte-carlo-simulations-leonardo-araujo/?trackingId=3t77cstp3gUhKS21x1Rmvw%3D%3D
import config
import pandas as pd
from binance.client import Client
from binance.enums import *

client = Client(config.API_KEY, config.API_SECRET)


# valid intervals — 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M

def print_file(pair, interval, name):
    # request historical candle (or klines) data
    bars = client.get_historical_klines(pair, interval, “27 Jun, 2018”, “27 Jun, 2021”)

    # delete unwanted data — just keep date, open, high, low, close
    for line in bars:
        del line[5:]

    # save as CSV file
    df = pd.DataFrame(bars, columns=[‘date’, ‘open’, ‘high’, ‘low’, ‘close’])
    df.set_index(‘date’, inplace = True)
    df.to_csv(name)


print_file(‘BTCUSDT’, ‘1
d’, “BTC_1d.csv”)
