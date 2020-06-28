import requests as http
import pandas as pd
import json
import keys

file_name = 'pickedStocks.txt'
api_key = keys.api_key

def savePickedStocks(picked_stocks):
    with open(file_name, 'w') as outfile:
        json.dump(picked_stocks, outfile)
    
    print('Saved')

def retrievePickedStocks():
    with open(file_name) as jsonfile:
        data = json.load(jsonfile)
        return data

def getStocks():
    params = {
        'apikey': api_key
    }

    stocks = http.get('https://financialmodelingprep.com/api/v3/stock/list', params)
    return stocks.json()

def pickStocks(allStocks):
    params = {
        'apikey': api_key
    }

    picked_stocks = []
    for stock in allStocks:
        #! check if keys exist
        if 'name' not in stock or 'symbol' not in stock:
            continue

        #? ignore foreign companies (American Deposit Receipts)
        #? ignore foreign companies (contains '.' in name)
        if 'ADR' in stock['name'] or '.' in stock['symbol']:
            continue


        symbol = stock['symbol']

        financial_ratios = http.get(f'https://financialmodelingprep.com/api/v3/ratios/{symbol}', params)
        financial_ratios = financial_ratios.json()
        if len(financial_ratios) <= 0:
            continue
        financial_ratios = financial_ratios[0]  # the service returns ratios per year, this gets latest
        
        #! check if keys exist
        if 'returnOnAssets' not in financial_ratios or 'priceEarningsRatio' not in financial_ratios:
            continue

        roa = financial_ratios['returnOnAssets']
        pe_ratio = financial_ratios['priceEarningsRatio']

        if roa is None or pe_ratio is None:
            continue

        print(f'{symbol}: roa={roa}, p-e ratio={pe_ratio}')

        #TODO: Ignore utilities and financial stocks (mutual funds, banks and insurance companies)
        #TODO: I believe funds are already ignored because pe_ratio would be None

        # return on assets must be at least 25%
        # price to earnings ratio of 5 or less may indicate that the year's data is unusual in some way
        if roa >= 0.25 and pe_ratio > 5:
            picked_stocks.append({
                'symbol': symbol,
                'name': stock['name'],
                'roa': roa,
                'pe_ratio': pe_ratio
            })

    print('Picked')
    return picked_stocks

def pickNewStocks():
    stocks = getStocks()
    picked_stocks = pickStocks(stocks)
    savePickedStocks(picked_stocks)

def evaluatePickedStocks():
    picked_stocks = retrievePickedStocks()

    #TODO: set score based on Joel Greenblatt's book
    #TODO: order picked_stocks by score

    print(picked_stocks)

if __name__ == "__main__":
    pickNewStocks()
    
    # once gone through the picking, making a ton of requests to the API
    # we can evaluate the stocks saved to the txt file:
    # evaluatePickedStocks()
