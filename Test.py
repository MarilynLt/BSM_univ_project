from random import randrange
import bs4 as bs
import numpy as np
import pandas as pd
import requests
import yfinance as yf
import concurrent.futures


# tickers = pd.read_html(
#     'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
# print(tickers.Symbol.to_list())


def retrieve_ticker():
    """ get sp100 stock ticker from wikipedia
        output:  list of stocks ticker """

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


def get_spot(stocks: list) -> pd.DataFrame:
    """ get spot price of a stocks list
        output: dataframe with stocks and spots"""

    spots = yf.download(retrieve_ticker(), interval="1m")['Adj Close'].iloc[-1, :]
    df = pd.DataFrame({"stocks": stocks, "spot": spots}).reset_index(drop=True)
    return df


# get stock spot
# spot = get_spot(retrieve_ticker())


def random_ticker():
    t = retrieve_ticker()
    i = randrange(len(t))
    random_ticker = t[i]

    return random_ticker


# def options_getter(symbol):
#
#     stock = yf.Ticker(symbol)
#     maturity = stock.options
#     options = pd.DataFrame()
#
#     for item in maturity:
#         opt = stock.option_chain(item)
#         opt= pd.DataFrame().append(opt.calls).append(opt.puts)
#         opt['expirationDate'] = maturity
#         options = options.append(opt, ignore_index=True)
#
#     return options

for t in random_ticker():
    maturity = yf.Ticker(str(t)).options
    df = pd.DataFrame()
    for exp in maturity:
        opt = yf.Ticker(str(t)).option_chain(exp)
        opt = pd.concat([opt.calls, opt.puts], ignore_index=True)
        # opt = pd.DataFrame().append(opt.calls).append(opt.puts)
    df = pd.concat([df, opt], ignore_index=True)
    # df = df.append(opt, ignore_index=True)

    # column to know if option is a call or a put
    df['Type'] = df['contractSymbol'].str[4:].apply(lambda x: 'P' if "P" in x else 'C')

df.to_clipboard()

# def get_cp(exp, dataframe: pd.DataFrame):
#     opt = tickers.option_chain(exp)
#     opt = pd.concat([opt.calls, opt.puts], ignore_index=True)
#     df = pd.concat([dataframe, opt], ignore_index=True)


# # tickers = yf.Ticker(['AAPL','MSFT','ABBV'])
# tickers = yf.Ticker('AAPL')
# maturity = tickers.options
# df = pd.DataFrame()
# # for exp in maturity:
# #     opt = tickers.option_chain(exp)
# #     # opt = pd.DataFrame().append(opt.calls).append(opt.puts)
# #     opt = pd.concat([opt.calls, opt.puts], ignore_index=True)
# # # df = df.append(opt, ignore_index=True)
# with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
#     executor.map(get_cp, maturity)
# df = pd.concat([df, opt], ignore_index=True)


# print(df.columns)
