import pandas as pd
import numpy as np
import datetime
import os

## Rename Columns
for file in os.listdir('.'):
    if file.endswith('.csv'):
        data = pd.read_csv(file)
        print
        data.rename(columns={'Close/Last':'Close',' Volume':'Volume',' Open':'Open',' High':'High',' Low':'Low'}, inplace=True)
        data = data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        data.to_csv(file, index=False)


## Remove Dollar Sign
for file in os.listdir('.'):
    if file.endswith('.csv'):
        data = pd.read_csv(file, parse_dates=[0])
        data[data.columns[1:5]] = data[data.columns[1:5]].replace('[^.0-9]', '', regex=True).astype(float)
        data.to_csv(file, index=False)

## Remove Whitespace in Columns
for file in os.listdir('.'):
    if file.endswith('.csv'):
        data = pd.read_csv(file, parse_dates=[0])
        data['Open'] = data['Open'].astype(str).str.strip()
        data['High'] = data['High'].astype(str).str.strip()
        data['Low'] = data['Low'].astype(str).str.strip()
        data['Close'] = data['Close'].astype(str).str.strip()
        data[data.columns[1:5]] = data[data.columns[1:5]].replace('[^.0-9]', '', regex=True).astype(float)
        data.to_csv(file, index=False)

## Reverse Sort (oldest date on top)
for file in os.listdir('.'):
    if file.endswith('.csv'):
        data = pd.read_csv(file)
        data = data.iloc[::-1]
        data.reset_index(inplace=True, drop=True)
        data.to_csv(file, index=False)

## Fix date (remove timestamp from datetime)
for file in os.listdir('.'):
    if file.endswith('.csv'):
        data = pd.read_csv(file, parse_dates=[0])
        data['Date'] = pd.to_datetime(data['Date'])
        data['Date'] = data['Date'].dt.date
        data.to_csv(file, index=False, date_format='%Y-%m-%d')


##Replace 0 with nan then remove those rows (holidays)
for file in os.listdir('.'):
    if file.endswith('.csv'):
        data = pd.read_csv(file, parse_dates=[0])
        data.replace(0, np.nan, inplace=True)
        data.dropna(how='any', inplace=True)
        data.to_csv(file, index=False, date_format='%Y-%m-%d')
