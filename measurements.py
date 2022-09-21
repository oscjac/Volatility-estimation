from .ticker import Ticker
from numpy import log
from cmath import sqrt

def close_to_close(ticker: Ticker) -> complex:
    """Returns close to close volatility over past 100 days. Assumes zero drift

    Args:
        ticker (Ticker): Ticker to get volatility from

    Returns:
        float: Colatility
    """
    f = 252 # Frequency of returns
    data = ticker.get_close_prices(100)
    sum = 0.0
    for i in range(1,len(data)):
        sum += ((data[i])/data[i-1])**2
    return sqrt(sum * f/99)

def parkinson(ticker: Ticker):
    f = 252 # Frequency of returns
    highs = ticker.get_high_prices(100)
    lows = ticker.get_low_prices(100)
    sum = 0.0
    for i in range(0,len(highs)):
        sum += (highs[i]/lows[i])**2
    return sqrt(sum * f/(400*log(2)))

def garman_klass(ticker: Ticker):
    f = 252 # Frequency of returns
    highs = ticker.get_high_prices(100)
    lows = ticker.get_low_prices(100)
    open = ticker.get_open_prices(100)
    close = ticker.get_close_prices(100)
    sum = 0.0
    for i in range(0,len(highs)):
        high_low = (log(highs[i]/lows[i]))**2 * (1/2)
        close_open = (2*log(2)-1) * (log(close[i]/open[i]))**2
        sum += high_low - close_open
    return sqrt((f/100)*sum)

def rogers_satchell(ticker: Ticker):
    f = 252 # Frequency of returns
    highs = ticker.get_high_prices(100)
    lows = ticker.get_low_prices(100)
    open = ticker.get_open_prices(100)
    close = ticker.get_close_prices(100)
    sum = 0.0
    for i in range(0,len(highs)):
        sum += log(highs[i]/close[i]) + log(highs[i]/open[i]) +\
                log(lows[i]/close[i]) + log(lows[i]/open[i])
    return sqrt(f/100 * sum)

def gk_yz_extension(ticker: Ticker):
    f = 252 # Frequency of returns
    highs = ticker.get_high_prices(100)
    lows = ticker.get_low_prices(100)
    open = ticker.get_open_prices(100)
    close = ticker.get_close_prices(100)
    sum = 0.0
    for i in range(1,len(highs)):
        overnight_high_low = (log(open[i]/close[i-1]))**2 + (1/2)*(log(highs[i]/lows[i]))**2
        close_open = (2*log(2)-1) * (log(close[i]/open[i]))**2
        sum += overnight_high_low - close_open
    return sqrt(f/100 * sum)

def yang_zhang(ticker: Ticker):
    f = 252 # Frequency of returns
    K = 0.34/(1.34 + 101/99)
    open = ticker.get_open_prices(100)
    close = ticker.get_close_prices(100)
    overnight = 0.0
    open_to_close = 0.0
    overnight_mean = 0.0
    open_to_close_mean = 0.0

    #Calculate mean
    for i in range(1,len(open)): 
        overnight_mean += log(open[i]/close[i-1])
    overnight_mean = overnight_mean/(len(open)-1)
    for i in range(0,len(open)):
        open_to_close_mean += log(close[i]/open[i])
    open_to_close_mean = open_to_close_mean/len(open)

    for i in range(1,len(open)):
        overnight += (log(open[i]/close[i-1])-overnight_mean)**2
    overnight = overnight * (f/(len(open-2)))
    for i in range(0,len(open)):
        open_to_close += (log(close[i]/open[i])-open_to_close_mean)**2
    open_to_close = open_to_close * (f/(len(open)-1))
    sum = overnight + K * open_to_close + (1-K) * rogers_satchell(ticker)**2
    return sqrt(sum)