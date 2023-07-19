import requests, csv, datetime
import yfinance as yf
import json


# The following tickers (keys) can only be found on the TD Ameritrade API under the respective (values).
replacements = {'DJI': '$DJI', 'SPX': '$SPX.X', 'VIX': '$VIX.X', 'COMP':'COMP:GIDS'}

# Read stocks to update from file
with open('stocks.txt', newline='') as f:
    lines = f.read().splitlines()
    stocks = list(lines[1:])
    for ticker in stocks:
        if ticker in replacements:
            stocks[stocks.index(ticker)] = replacements[ticker]

# Break into chunks as to not call the function with too many symbols
def chunks(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

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
    }
    
    #return json.dumps(quote_details)
    return quote_details

# Create Close Date Dict
close_data = {}

for chunk in chunks(stocks, 10):
    for ticker in chunk:
        data = get_quote_details(ticker)
        close_data[ticker] = data

#print(json.dumps(close_data, indent=4))

today = datetime.date.today().strftime('%Y-%m-%d')

with open('eod.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Symbol', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    for ticker in close_data:
        if ticker in ['$DJI', '$SPX.X', '$VIX.X', 'COMP:GIDS']:
            writer.writerow([close_data[ticker]['symbol'], today, close_data[ticker]['openPrice'],
                                        close_data[ticker]['highPrice'], close_data[ticker]['lowPrice'],
                                        close_data[ticker]['lastPrice'], '0'])
        else:
            writer.writerow([close_data[ticker]['symbol'], today, close_data[ticker]['openPrice'],
                             close_data[ticker]['highPrice'], close_data[ticker]['lowPrice'],
                             close_data[ticker]['regularMarketLastPrice'], close_data[ticker]['totalVolume']])
