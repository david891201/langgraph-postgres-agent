import yfinance as yf
import pandas as pd

class StockFetcher:
    def __init__(self, ticker: str):
        self.ticker = ticker
    def __call__(self, start: str, end: str):
        stock = yf.Ticker(self.ticker)
        df = stock.history(start=start, end=end)
        df.reset_index(inplace=True)
        df.columns = [col.replace(" ", "_") for col in df.columns] # 列名不能有空格
        df['date'] = df['Date'].dt.strftime("%Y-%m-%d") # 只能儲存str的日期格式
        df.drop(columns=["Date"], inplace=True)
        return df