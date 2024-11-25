def calculate_SMA(prices, window=20):
    return prices.rolling(window=window).mean()


def calculate_bollinger_bands_percent(prices, sma, window):
    rolling_std = prices.rolling(window=window).std()
    upper_band = sma + (2 * rolling_std)
    lower_band = sma - (2 * rolling_std)
    return (prices - lower_band) / (upper_band - lower_band)


def calculate_momentum(prices, window):
    return (prices / prices.shift(window)) - 1