import talib as ta
import pandas as pd

class TechnicalIndicators:
    def __init__(self, df):
        self.df = df
        self.indicators = {
            'SMA': ta.SMA,
            'EMA': ta.EMA,
            'WMA': ta.WMA,
            'MACD': ta.MACD,
            'RSI': ta.RSI,
            'BBANDS': ta.BBANDS,
            'ATR': ta.ATR,
            'TREND': ta.HT_TRENDLINE
        }

    def get_sma(self, period):
        return ta.SMA(self.df['Close'], timeperiod=period)

    def get_ema(self, period):
        return ta.EMA(self.df['Close'], timeperiod=period)

    def get_wma(self, period):
        return ta.WMA(self.df['Close'], timeperiod=period)

    def get_macd(self, short_period, long_period, signal_period):
        return ta.MACD(self.df['Close'], fastperiod=short_period, slowperiod=long_period, signalperiod=signal_period)

    def get_rsi(self, period):
        return ta.RSI(self.df['Close'], timeperiod=period)

    def get_bollinger_bands(self, period, std):   #WORKING - 3 outputs (upper band,  SMA, lower band)
        return ta.BBANDS(self.df['Close'], timeperiod=period, nbdevup=std, nbdevdn=std)

    def get_atr(self, period):
        return ta.ATR(self.df['High'], self.df['Low'], self.df['Close'], timeperiod=period)

    def get_trend(self, period):
        return ta.HT_TRENDLINE(self.df['Close'], timeperiod=period)

