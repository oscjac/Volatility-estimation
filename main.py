from .ticker import API, Ticker
from statistics import stdev

def close_to_close(ticker: Ticker) -> float:
    """Returns close to close volatility over past 100 days. Assumes zero drift

    Args:
        ticker (Ticker): Ticker to get volatility from

    Returns:
        float: Colatility
    """
    data = ticker.get_close_prices(100)
    returns = []
    for i in range(1,len(data)):
        returns.append((data[i]+ticker.dividend)/data[i-1])
    return stdev(returns)

def parkinson(ticker: Ticker):
    
    return

def garman_klass(ticker: Ticker):
    return

def rogers_satchell(ticker: Ticker):
    return

def gk_yz_extension(ticker: Ticker):
    return

def yang_zhang(ticker: Ticker):
    return



def main():
    while(True):
        api = API()
        if (not api.key_exists()):
            while (True):
                key = input("Enter API Key: ")
                api.set_key(key)
                # if (not api.valid()):
        ticker = input("Historical volatility for: ")
        print(close_to_close(Ticker(api, ticker)))

if __name__ == '__main__':
    main()