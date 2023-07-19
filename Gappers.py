#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import datetime, time, json, requests
#from config import client_id
from os import listdir
import yfinance as yf

# Function to fetch stock quote details
def get_quote_details(ticker):
    print("working on " + ticker)
    stock = yf.Ticker(ticker)
    quote = stock.info
    
    if quote is None:
        print("No data available for the given ticker symbol.")
        return
    
    quote_details = {
        "symbol": quote.get("symbol", ""),
        "description": quote.get("longName", ""),
        "bidPrice": quote.get("bid", 0),
        "bidSize": quote.get("bidSize", 0),
        "bidId": quote.get("bidId", ""),
        "askPrice": quote.get("ask", 0),
        "askSize": quote.get("askSize", 0),
        "askId": quote.get("askId", ""),
        "lastPrice": quote.get("regularMarketPrice", 0),
        "lastSize": quote.get("regularMarketVolume", 0),
        "lastId": quote.get("regularMarketTime", ""),
        "openPrice": quote.get("regularMarketOpen", 0),
        "highPrice": quote.get("regularMarketDayHigh", 0),
        "lowPrice": quote.get("regularMarketDayLow", 0),
        "closePrice": quote.get("regularMarketPreviousClose", 0),
        "netChange": quote.get("regularMarketChange", 0),
        "totalVolume": quote.get("regularMarketVolume", 0),
        "quoteTimeInLong": quote.get("quoteTime", 0),
        "tradeTimeInLong": quote.get("regularMarketTime", 0),
        "mark": quote.get("mark", 0),
        "exchange": quote.get("exchange", ""),
        "exchangeName": quote.get("exchangeName", ""),
        "marginable": quote.get("marginable", False),
        "shortable": quote.get("shortable", False),
        "volatility": quote.get("volatility", 0),
        "digits": quote.get("regularMarketPrice", 0),
        "52WkHigh": quote.get("fiftyTwoWeekHigh", 0),
        "52WkLow": quote.get("fiftyTwoWeekLow", 0),
        "peRatio": quote.get("trailingPE", 0),
        "divAmount": quote.get("dividendRate", 0),
        "divYield": quote.get("dividendYield", 0),
        "divDate": quote.get("exDividendDate", ""),
        "securityStatus": quote.get("quoteType", ""),
        "regularMarketLastPrice": quote.get("regularMarketPrice", 0),
        "regularMarketLastSize": quote.get("regularMarketVolume", 0),
        "regularMarketNetChange": quote.get("regularMarketChange", 0),
        "regularMarketTradeTimeInLong": quote.get("regularMarketTime", 0)
        # Fill in the details here
    }
    
    #return json.dumps(quote_details)
    return quote_details


# Read stocks to update from file
with open('stocks.txt', newline='') as f:
    lines = f.read().splitlines()
    stocks = list(lines[1:])


# Break into chunks as to not call the function with too many symbols
def chunks(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


# Create Close Date Dict
close_data = {}

for chunk in chunks(stocks, 10):
    for ticker in chunk:
        data = get_quote_details(ticker)
        close_data[ticker] = data

print(json.dumps(close_data, indent=4))

df = pd.DataFrame.from_dict(close_data, orient='index', columns=['symbol', 'openPrice', 'closePrice', '52WkHigh', 'totalVolume'])
df.to_csv('open_prices.csv', index=False)
df['Pct Change'] = (df['openPrice'] / df['closePrice']) - 1

file_location = 'stock_data/'

stock_20_day_high = {}
stock_50_day_high = {}
stock_100_day_high = {}

for file in listdir('./stock_data/'):
    if file.endswith('.csv'):
        data = pd.read_csv(file_location + file, parse_dates=[0])
        data = data.iloc[::-1]
        data = data.iloc[:100]
        stock_20_day_high[file.split(".csv")[0]] = data[:20]['High'].max()
        stock_50_day_high[file.split(".csv")[0]] = data[:50]['High'].max()
        stock_100_day_high[file.split(".csv")[0]] = data['High'].max()

df['20 Day High'] = df['symbol'].map(stock_20_day_high)
df['50 Day High'] = df['symbol'].map(stock_50_day_high)
df['100 Day High'] = df['symbol'].map(stock_100_day_high)


def twitter_auth():
	"""Twitter session authorization"""

	config_file = '.tweepy.json'
	with open(config_file) as fh:
			config = json.load(fh)

	auth = tweepy.OAuthHandler(
			config['consumer_key'], config['consumer_secret']
	)
	auth.set_access_token(
			config['access_token'], config['access_token_secret']
	)

	return tweepy.API(auth)


#twitter = twitter_auth()


content = []
content.append("Stock gaps:\n")
char_count = len(content[0])
for t in df[['symbol', 'Pct Change']].values:
    if t[1] <= -1:
        pass
    elif abs(t[1]) > .03:
        line = f"${t[0]} {t[1]:,.2%}\n"
        content.append(line)
        char_count += len(line)
        if char_count >= 253:
            twitter.update_status("".join(content))
            content.clear()
            char_count = 0
            content.append("Stock gaps:\n")
# twitter.update_status("".join(content))
print("".join(content))


# Breakout alerts
content.clear()
char_count = 0

for t in df[['symbol', 'openPrice', '20 Day High', '50 Day High', '100 Day High', '52WkHigh']].values:
    if t[1] > t[2]:
        if t[1] > t[5]:
            line = f'${t[0]} New 52 Wk high!\n'
        elif t[1] > t[4]:
                line = f'${t[0]} Alert: Open > 100 day high\n'
        elif t[1] > t[3]:
            line = f'${t[0]} Alert: Open > 50 day high\n'
        else:
            line = f'${t[0]} Alert: Open > 20 day high\n'
        # Count characters
        char_count += len(line)
        content.append(line)
        if char_count > 242:
            # twitter.update_status("".join(content))
            print("".join(content))
            content.clear()
            char_count = 0
if content:
    # twitter.update_status("".join(content))
    print("".join(content))
