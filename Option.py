from random import randrange
import numpy as np
from scipy.stats import norm
import bs4 as bs
import pandas as pd
import requests
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


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
            if option_type == 'CALL':
                call = self.spot * np.exp(-self.q * self.t) * self.n(self._d1) - self.strike * np.exp(
                    -self.r * self.t) * self.n(self._d2)
                return call.round(3)
            elif option_type == 'PUT':
                put = self.strike * np.exp(- self.r * self.t) * self.n(-self._d2) - self.spot * np.exp(
                    - self.q * self.t) * self.n(-self._d1)
                return put.round(3)
        except Exception as e:
            print(f"{e} \n"
                  f"Please enter the option type in string. It should be either Call or Put")

    def delta(self, option_type: str) -> float:
        """
        Delta measures the change in the option price for a $1 change in the stock price (sensitivity)
        :param option_type: whether it is a Call or a Put
        :return: delta of the option
        """
        try:
            if option_type == 'CALL':
                delta = np.exp(-self.q * self.t) * self.n(self._d1)
            elif option_type == 'PUT':
                delta = np.exp(-self.q * self.t) * (self.n(self._d1) - 1)
            return delta.round(4)
        except Exception as e:
            print(f"{e} \n"
                  f"Option type missing, please enter the option type. It should be a string")

    def gamma(self) -> float:
        """
        Gamma measure the change on delta when the stock price change (convexity)
        :return: gama of the option
        """
        gamma = np.exp(-self.q * self.t) * norm.pdf(self._d1) / self.spot * self.sigma * np.sqrt(self.t)
        return gamma.round(4)

    def vega(self) -> float:
        """
        Vega measures the change in the option price per percentage point change in the volatility
        :return: vega of the option
        """
        vega = self.spot * np.exp(-self.q * self.t) * np.sqrt(self.t) * norm.pdf(self._d1) / 100
        return vega.round(4)

    def theta(self, option_type) -> float:
        """
        Vega measures the change in the option price per one calendar day (or 1/365 of a year)
        :return: theta of the option
        """
        try:
            if option_type == 'CALL':
                theta = (self.q * self.spot * np.exp(-self.q * self.t) * self.n(
                    self._d1) - self.r * self.strike * np.exp(-self.r * self.t) * self.n(self._d2) - norm.pdf(
                    self._d1) * self.spot * self.sigma * np.exp(-self.q * self.t) / 2 * np.sqrt(self.t)) / 365
            elif option_type == 'PUT':
                theta = (self.r * self.strike * np.exp(-self.r * self.t) * self.n(
                    -self._d2) - self.q * self.spot * np.exp(-self.q * self.t) * self.n(-self._d1) - norm.pdf(
                    self._d1) * self.spot * self.sigma * np.exp(-self.q * self.t) / 2 * np.sqrt(self.t)) / 365
            return theta.round(4)
        except Exception as e:
            print(f"{e} \n"
                  f"Option type missing, please enter the option type. It should be a string")

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
            pd.DataFrame({"stocks": tickers, "spot": spots}).reset_index(drop=True).dropna().to_records(index=False))

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
                    type_op = 'call' if option_type == 'calls' else 'put'
                    option_data.append({
                        'Ticker': t,
                        'Spot': s,
                        'Maturity': exp,
                        'Type': type_op,
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

    @staticmethod
    def option_chart():
        with PdfPages('Options_graph.pdf') as pdf:
            with plt.style.context('seaborn-v0_8-darkgrid'):
                spot = np.arange(1, 150)

                # Greek plot

                fig, axes = plt.subplots(5, 1, figsize=(10, 25))
                fig.suptitle('Greeks', ha='center', fontweight='bold', fontsize=15)
                fig.tight_layout(pad=7.0)
                strike = [63, 87, 124]

                for s in strike:
                    del_call = [Options(float(s), float(x), 5.0, 0.1).delta('CALL') for x in spot]
                    del_put = [Options(float(s), float(x), 5.0, 0.1).delta('PUT') for x in spot]
                    axes[0].plot(del_call, linestyle='--', label=("Delta Call K=%s" % s))
                    axes[0].plot(del_put, label=("Delta Put K=%s" % s))

                axes[0].set_ylabel('Delta')
                axes[0].legend()

                for s in strike:
                    gam = [Options(float(s), float(x), 5.0, 0.1).gamma() for x in spot]
                    axes[1].plot(gam, linestyle='--', label=("Options Gamma K=%s" % s))

                axes[1].set_ylabel('Gamma')
                axes[1].legend()

                for s in strike:
                    veg = [Options(float(s), float(x), 5.0, 0.1).vega() for x in spot]
                    axes[2].plot(veg, label=("Options Vega K=%s" % s))

                axes[2].set_ylabel('Vega')
                axes[2].set_title('Volatility = 0.1 ')
                axes[2].legend()

                for s in strike:
                    theta_call = [Options(float(s), float(x), 5.0, 0.1).theta('CALL') for x in spot]
                    theta_put = [Options(float(s), float(x), 5.0, 0.1).theta('PUT') for x in spot]
                    axes[3].plot(theta_call, linestyle='--', label=("Theta Call K=%s" % s))
                    axes[3].plot(theta_put, label=("Theta Put K=%s" % s))

                axes[3].set_ylabel('Theta')
                axes[3].set_title('Maturity = 5 years')
                axes[3].legend()

                # Option plot

                call_val = [Options(87.0, float(x), 1.0, 0.5).bsm('CALL') for x in spot]
                put_val = [Options(87.0, float(x), 1.0, 0.5).bsm('PUT') for x in spot]

                axes[4].set_title(f'Change in option value with stock price'
                                  f'\n \n Strike: 87, t: 1 an, sigma: 0.5, r: 5%, q: 4%', fontweight="bold")
                axes[4].set_xlabel('Stock Price')
                axes[4].set_ylabel("Option price")
                axes[4].plot(spot, call_val, color='green', label='Call')
                axes[4].plot(spot, put_val, color='blue', label='Put')
                axes[4].legend()

            pdf.savefig()
            plt.close()