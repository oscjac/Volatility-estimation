from .ticker import API, Ticker
from .measurements import *

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