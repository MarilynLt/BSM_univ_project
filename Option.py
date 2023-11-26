from random import randrange
import numpy as np
from scipy.stats import norm
import bs4 as bs
import pandas as pd
import requests
import yfinance as yf
import time


class Options:
    """
       Valuation of options in Black-Scholes-Merton Model (include dividend)
       Attributes
       ==========
       strike: strike price
       spot: initial stock/index level
       t: time to maturity (in year fractions)
       r: constant risk-free short rate, assume flat term structure
       q: yield of the dividend
       sigma: volatility factor in diffusion term

    """

    def __init__(self, strike: float, spot: float, t: float, sigma: float, r: float = 0.05, q: float = 0.04):
        self.strike = strike
        self.spot = spot
        self.r = r
        self.q = q
        self.t = t
        self.sigma = sigma

        # private
        self._d1 = self.d1()
        self._d2 = self.d2()
        # self._tickers = self.retrieve_ticker()

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

    def bsm(self, option_type: str) -> float:
        """
        :param option_type: whether it is a Call or a Put
        :return: price of the put or call
        """
        try:
            if option_type == 'CALL' or 'CALLS':
                call = self.spot * np.exp(-self.q * self.t) * self.n(self._d1) - self.strike * np.exp(
                    -self.r * self.t) * \
                       self.n(self._d2)
                return call.round(3)
            elif option_type == 'PUT' or 'PUTS':
                put = self.strike * np.exp(- self.r * self.t) * self.n(-self._d2) - self.spot * np.exp(
                    - self.q * self.t) \
                      * self.n(-self._d1)
                return put.round(3)
        except Exception as e:
            print(f"{e}: Please enter the option type in string. It should be either Call or Put")

    def delta(self, option_type: str) -> float:
        """
        Delta measures the change in the option price for a $1 change in the stock price (sensitivity)
        :param option_type: whether it is a Call or a Put
        :return: delta of the option
        """
        try:
            if option_type == 'CALL'or 'CALLS':
                delta = np.exp(-self.q * self.t) * self.n(self._d1)
            elif option_type == 'PUT' or 'PUTS':
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
        # get the ticker from wikipedia ETF S&P 100 page
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

        # get the spot of each stocks from yahoo finance
        spots = yf.download(tickers, interval="1m")['Adj Close'].iloc[-1, :]
        stock_price = list(
            pd.DataFrame({"stocks": tickers, "spot": spots}).reset_index(drop=True).to_records(index=False))

        return stock_price

    @staticmethod
    def get_spot(ticker_list):
        """
        get spot price of a stocks list
        :param ticker_list: list of stock ticker
        :return: dataframe with stocks and spots
        """
        spot = yf.download(ticker_list)['Adj Close'].iloc[-1]
        return spot.round(2)

    @staticmethod
    def get_option(stock_price) -> pd.DataFrame:
        """
        Get the option characteristics from yahoo finance (s, k, t, sigma)
        :return: dataframe with the options data
        """
        # start = time.time()
        option_data = []
        for t, s in stock_price:
            try:
                maturity = yf.Ticker(str(t)).options
                exp = maturity[randrange(len(maturity))]
            except ValueError:
                continue

            for option_type in ['calls', 'puts']:
                opt = getattr(yf.Ticker(str(t)).option_chain(exp), option_type)
                for row in opt.itertuples():
                    option_data.append({
                        'Ticker': t,
                        'Spot': s,
                        'Maturity': exp,
                        'Type': option_type,
                        'Contract Symbol': row.contractSymbol,
                        'Strike': row.strike,
                        'Volatility': row.impliedVolatility,
                        'Volume': row.volume,
                        'Currency': row.currency
                    })
                    break

        # df = pd.DataFrame()
        # df['Ticker'] = 0
        # df['Spot'] = 0
        # for t, s in Options.retrieve_ticker():
        #     try:
        #         maturity = yf.Ticker(str(t)).options
        #         exp = maturity[randrange(len(maturity))] # return a random range from the maturity list
        #     except ValueError:
        #         continue
        #
        #     opt = yf.Ticker(str(t)).option_chain(exp)
        #     opt = pd.concat([opt.calls, opt.puts], ignore_index=True)
        #     df = pd.concat([df, opt], ignore_index=True)
        #     df.loc[max(df.index), ('Ticker', 'Spot')] = t, s
        #     df.iloc[:, 0:2] = df.iloc[:, 0:2].fillna(method='bfill')
        #
        # # column to know if option is a call or a put
        # df['Type'] = df['contractSymbol'].str[4:].apply(lambda x: 'P' if "P" in x else 'C')

        # print(time.time() - start)

        return pd.DataFrame(option_data)


"""
# Get option data
tickers = ['AAPL', 'MSFT', 'GOOGL']
option_data = BlackScholes.get_option_data(tickers)

# Compute option prices
option_data['Option Price'] = option_data.apply(
    lambda row: BlackScholes.get_option_price(
        row['Strike'], row['Strike'], (row['Expiry'] - datetime.datetime.now()).days / 365, 0.01, 0.2, row['Type']), axis=1)
        """