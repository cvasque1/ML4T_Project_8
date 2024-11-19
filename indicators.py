import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from util import get_data

def calculate_SMA(prices, window=20):
    return prices.rolling(window=window).mean()