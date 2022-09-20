from json import loads
from requests import get
from .api import API

class TickerDoesNotExistError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Ticker:
    name: str
    tckr: str
    latest_price: float
    exchange: str
    volatility: float
    volume: int
    key: str
    saved: bool
    dividend: float
    def __init__(self, api: API, tckr: str) -> None:
        self.key = api.key
        self.tckr = tckr
        self.saved = False
        response = get(f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={tckr}&apikey={self.key}")
        data = response.json()
        self.name = data["Name"]
        self.exchange = data["Exchange"]
        self.dividend = float(data["DividendPerShare"])
    def __repr__(self) -> str:
        return self.tckr
    
    def exists(self):
        """ Returns true if the ticker parameter exists\n
        Parameter:\n
        \tticker: equity ticker to verify\n
        Returns: boolean
        """
        if (not self.tckr):
            return False
        response = get(f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={self.tckr}&apikey={self.key}")
        data = response.json()
        matches = data["bestMatches"]
        if (not len(matches)): # No matches?
            return False
        if (matches[0]["1. symbol"] != self.tckr): # Match different than desired ticker
            return False
        return True

    def save_full(self):
        res = get(f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={self.tckr}&outputsize=full&apikey={self.key}")
        data = res.text
        with (open(f"{self.tckr}.txt", "w") as data_file):
            data_file.write(data)
        self.saved = True
        return

    def _fetch_prices(self, days: int, outputsize: str):
        assert days > 0
        assert outputsize == "compact" or outputsize == "full"
        data = []
        if (self.saved):
            with (open(f"{self.tckr}.txt") as data_file):
                data = loads(data_file.read())
        else:
            res = get(f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={self.tckr}&outputsize={outputsize}&apikey={self.key}")
            data = res.json()
        return data

    def get_close_prices(self, days: int):
        """ Fetches ticker prices from the past n days\n
        Parameters:\n
        \tticker: equity ticker to fetch\n
        \tdays: number of days to fetch\n
        Returns: List of tuples with day's closing price at index 0 and date at index 1
        """
        assert self.exists()
        outputsize = "full" if days > 100 else "compact"
        data = self._fetch_prices(days, outputsize)
        prices = []
        i=0
        while (i < days):
            for day, info in data["Time Series (Daily)"].items():
                prices.append((day, info["4. close"]))
                i += 1
        self.latest_price = prices[0][1]
        return prices

    def get_low_prices(self, days: int):
        return

    def get_high_prices(self, days: int):
        return
    
    def get_open_prices(self, days:int):
        