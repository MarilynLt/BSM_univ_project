import numpy as np
from scipy.stats import norm
import bs4 as bs
import pandas as pd
import requests
import yfinance as yf


class Option:
    """
       Valuation of options in Black-Scholes-Merton Model (include dividend)
       Attributes
       ==========
       spot: initial stock/index level
       strike: strike price
       t: time to maturity (in year fractions)
       r: constant risk-free short rate, assume flat term structure
       q: yield of the dividend
       sigma: volatility factor in diffusion term

    """

    def __int__(self, strike: float, spot: float, r: float, q: float, t: float, sigma: float):
        self.strike = strike
        self.spot = spot
        self.r = r
        self.q = q
        self.t = t
        self.sigma = sigma

        # private
        self._d1 = self.d1()
        self._d2 = self.d2()
        self._tickers = self.retrieve_ticker()

    @property
    def S(self):
        return self.spot

    @property
    def K(self):
        return self.strike

    @property
    def R(self):
        return self.r

    @property
    def Q(self):
        return self.q

    @property
    def T(self):
        return self.t

    @staticmethod
    def n(x):
        return norm.cdf(x)

    def d1(self) -> float:
        return (np.log(self.spot / self.strike) + (self.r - self.q + 0.5 * self.sigma ** 2) * self.t) / (
                self.sigma * np.sqrt(self.t))

    def d2(self) -> float:
        return - (self.sigma * np.sqrt(self.t)) + self._d1

    # def bsm(self, option_type: str) -> float:
    #     if option_type == 'Call':
    #         call = self.n(self._d1) * self.spot - self.n(self._d2) * self.strike * np.exp(-self.r * self.t)
    #         return call
    #     else:
    #         put = self.n(- self._d2) * self.strike * np.exp(-self.r * self.t) - self.n(- self._d1) * self.spot
    #     return put

    def bsm(self, option_type: str) -> float:
        """
        :param option_type: whether it is a Call or a Put
        :return: price of the put or call
        """
        try:
            if option_type == 'Call':
                call = self.spot * np.exp(-self.q * self.t) * self.n(self._d1) - self.strike * np.exp(-self.r * self.t) * \
                       self.n(self._d2)
                return call
            elif option_type == 'Put':
                put = self.strike * np.exp(- self.r * self.t) * self.n(-self._d2) - self.spot * np.exp(- self.q * self.t) \
                      * self.n(-self._d1)
                return put
        except:
            print("Please enter the option type in string. It should be either Call or Put")

    def delta(self, option_type: str) -> float:
        """
        Delta measures the change in the option price for a $1 change in the stock price (sensitivity)
        :param option_type: whether it is a Call or a Put
        :return: delta of the option
        """
        try:
            if option_type == 'Call':
                delta = np.exp(-self.q * self.t) * self.n(self._d1)
            elif option_type == 'Put':
                delta = np.exp(-self.q * self.t) * (self.n(self._d1) - 1)
            return delta
        except:
            print("Option type missing, please enter the option type. It should be a string")

    def gamma(self) -> float:
        """
        Gamma measure the change on delta when the stock price change (convexity)
        :return: gama of the option
        """
        gamma = np.exp(-self.q * self.t) * norm.pdf(self._d1) / self.spot * self.sigma * np.sqrt(self.t)
        return gamma

    def vega(self) -> float:
        """
        Vega measures the change in the option price per percentage point change in the volatility
        :return: vega of the option
        """
        vega = self.spot * np.exp(-self.q * self.t) * np.sqrt(self.t) * norm.pdf(self._d1) / 100
        return vega

    @staticmethod
    def retrieve_ticker() -> list:
        """
        get sp100 stock ticker from wikipedia
        :return: list of stocks ticker
        """

        r = requests.get("https://en.wikipedia.org/wiki/S%26P_100#Components")
        soup = bs.BeautifulSoup(r.text, 'lxml')
        table = soup.find('table', {'class': 'wikitable', 'id': 'constituents'})
        tickers = []

        for i in table.findAll('tr')[1:]:
            for x in i.findAll('td'):
                ticker = x.get_text()
                tickers.append(ticker)
                break

        tickers = [i.replace('\n', '') for i in tickers]

        return tickers

    def get_spot(self, stocks: list) -> pd.DataFrame:
        """
        get spot price of a stocks list
        :param stocks: list of stock ticker
        :return: dataframe with stocks and spots
        """
        spots = yf.download(self._tickers, interval="1m")['Adj Close'].iloc[-1, :]
        df = pd.DataFrame({"stocks": stocks, "spot": spots}).reset_index(drop=True)
        return df

    def get_option(self) -> pd.DataFrame:
        """
        Get the option characteristics from yahoo finance (s, k, t, sigma)
        :return: dataframe with the options data
        """
        for t in self.retrieve_ticker():
            maturity = yf.Ticker(str(t)).options
            df = pd.DataFrame()
            for exp in maturity:
                opt = yf.Ticker(str(t)).option_chain(exp)
                opt = pd.concat([opt.calls, opt.puts], ignore_index=True)
                # opt = pd.DataFrame().append(opt.calls).append(opt.puts)
            df = pd.concat([df, opt], ignore_index=True)
            # df = df.append(opt, ignore_index=True)

            # column to know if option is a call or a put
            df['Type'] = df['contractSymbol'].str[7].apply(lambda x: 'Put' if "P" in x else 'Call')

        return df
