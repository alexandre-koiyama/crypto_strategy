import technical_indicators as ti
import crypto_retrieve as cr
import pandas as pd
import numpy as np
from datetime import datetime

class Backtest:
    def __init__(self, symbol, interval, start_date, end_date):
        self.symbol = symbol
        self.interval = interval
        self.start_date = start_date
        self.end_date = end_date
        self.crypto_data = cr.CryptoData(self.symbol, self.interval, self.start_date, self.end_date)
        self.df = self.crypto_data.get_all_historical_data()
        self.indicators = ti.TechnicalIndicators(self.df)
        
    def run_backtest_sma(self, period):
        self.df['SMA'] = self.indicators.get_sma(period)
        self.df['SMA_signal'] = np.where(self.df['SMA'] > self.df['Close'], 1, -1)
        self.df['SMA_cross'] = self.df['SMA_signal'].diff()
        self.df['Strategy'] = self.df['SMA_cross'].where(df['SMA_Signal'] == 2,'BUY')
        self.df['Strategy'] = self.df['Strategy'].where(df['SMA_Signal'] == -2,'SELL')
        self.df['Strategy'] = self.df['Strategy'].fillna('HOLD')
        return self.df
    
    def run_backtest_macd(self, short_period, long_period, signal_period):
        self.df['MACD'], self.df['MACD_S'], self.df['MACD_H'] = self.indicators.get_macd(short_period, long_period, signal_period)
        self.df['MACD_signal'] = np.where(self.df['MACD'] > self.df['Close'], 1, -1)
        self.df['MACD_cross'] = self.df['MACD_signal'].diff()
        self.df['Strategy'] = self.df['MACD_cross'].where(df['MACD_Signal'] == 2,'BUY')
        self.df['Strategy'] = self.df['Strategy'].where(df['MACD_Signal'] == -2,'SELL')
        self.df['Strategy'] = self.df['Strategy'].fillna('HOLD')



