import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from util import get_data

def calculate_SMA(prices, window=20):
    return prices.rolling(window=window).mean()


def calculate_bollinger_bands_percent(prices, sma, window):
    rolling_std = prices.rolling(window=window).std()
    upper_band = sma + (2 * rolling_std)
    lower_band = sma - (2 * rolling_std)

    return (prices - lower_band) / (upper_band - lower_band)


def calculate_MACD(prices, fast_window=12, slow_window=26, signal_window=9):
    fast_ema = prices.ewm(span=fast_window, adjust=False).mean()
    slow_ema = prices.ewm(span=slow_window, adjust=False).mean()
    macd_line = fast_ema - slow_ema
    signal_line = macd_line.ewm(span=signal_window, adjust=False).mean()
    macd_histogram = macd_line - signal_line

    return macd_histogram