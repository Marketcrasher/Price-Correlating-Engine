import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup


def fetch_data(ticker1, ticker2, period='4y'):
    """Fetch historical data for two given tickers."""
    data1 = yf.download(ticker1, period=period, auto_adjust=True)['Close']
    data2 = yf.download(ticker2, period=period, auto_adjust=True)['Close']
    data = pd.concat([data1, data2], axis=1)
    data.columns = [ticker1, ticker2]
    return data

def get_average_price_for_given_value(data, ticker_reference, reference_value):
    """Calculate the average price of one ticker when the other has a certain value."""
    filtered_data = data[(data[ticker_reference] >= reference_value - 0.5) & 
                         (data[ticker_reference] <= reference_value + 0.5)]
    other_ticker = [col for col in data.columns if col != ticker_reference][0]
    return filtered_data[other_ticker].mean()

def fetch_sentiment(ticker):
    """Scrape StockTwits for the sentiment of a given stock ticker."""
    url = f"https://stocktwits.com/symbol/{ticker}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # This is a simplified example - you'll need to adjust based on the actual structure of the StockTwits page
    sentiment_data = soup.find('div', {'class': 'sentiment-data-class'})  # Placeholder class
    if sentiment_data:
        sentiment = sentiment_data.text.strip()
    else:
        sentiment = "Sentiment data not found."
    return sentiment

def main():
    print("Welcome to the financial correlation system!")
    
    ticker1 = input("Enter the ticker of the primary asset (AAPL, GC=F, BTC-USD, GOOG, ^GSPC, PA=F, PL=F, HG=F): ")
    ticker2 = input("Enter the ticker of the reference asset (DX-Y.NYB for DXY): ")
    ref_value = float(input(f"Enter the current value for {ticker2}: "))

    data = fetch_data(ticker1, ticker2)
    avg_price = get_average_price_for_given_value(data, ticker2, ref_value)
    sentiment = fetch_sentiment(ticker1)  # Fetch sentiment for the primary asset

    print(f"When {ticker2} was approximately {ref_value}, the average price of {ticker1} was {avg_price:.2f}")
    print(f"Current sentiment for {ticker1} on StockTwits is: {sentiment}")

if __name__ == "__main__":
    main()
