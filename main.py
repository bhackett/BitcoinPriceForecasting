import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
from datetime import datetime
import math
import statistics
from datetime import timedelta


def cdf(array, b, a):  # p(r) -> a < r < b
    mean = statistics.mean(array)
    std = statistics.stdev(array)
    p1 = 0.5 * (1 + math.erf((a - mean) / math.sqrt(2 * std ** 2)))
    p2 = 0.5 * (1 + math.erf((b - mean) / math.sqrt(2 * std ** 2)))
    return (p2 - p1)


start_date = datetime(2018, 6, 27)
end_date = datetime(2021, 6, 28)
dt = timedelta(days=1)
dates = np.arange(start_date, end_date, dt).astype(datetime)

file = pd.read_csv("BTC_1d.csv", parse_dates=True)
closes = file.close
plt.plot(dates, closes)
plt.show()

log_returns = np.log(1 + closes.pct_change())

u = log_returns.mean()
var = log_returns.var()
drift = u - (0.5 * var)
print("Drift: {}".format(drift))

stdev = log_returns.std()
days = 7
iterations = 10000
Z = norm.ppf(np.random.rand(days, iterations))
daily_returns = np.exp(drift + stdev * Z)

price_paths = np.zeros_like(daily_returns)
price_paths[0] = closes.iloc[-1]
for t in range(1, days):
    price_paths[t] = price_paths[t - 1] * daily_returns[t]

start_date = datetime(2021, 6, 27)
end_date = datetime(2021, 7, 4)
dt = timedelta(days=1)
future_dates = np.arange(start_date, end_date, dt).astype(datetime)

plt.plot(dates[-14:], closes[-14:], linestyle='dashed')
plt.plot(future_dates, price_paths)
plt.ylabel("Close price (BTC/USDT)")
plt.show()

sns.histplot(price_paths[-1, :], bins=20, stat="frequency")
plt.xlabel("Close price (BTC/USDT)")
plt.ylabel("Frequency")
plt.show()

pricemin = 30000
pricemax = 40000
print("Probability that the price will be between {} and {}: {}".format(pricemin, pricemax,
                                                                        cdf(price_paths[-1, :], pricemax, pricemin)))
