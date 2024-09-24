from crypto_retrieve import CryptoData
from datetime import datetime
import technical_indicators as ti   


if __name__ == '__main__':
    symbol = 'BTCUSDT'
    interval = '1d'
    start_date = datetime(2021,2, 1)
    end_date = datetime.now()

    crypto_data = CryptoData(symbol, interval, start_date, end_date)
    df = crypto_data.get_all_historical_data()

    indicators = ti.TechnicalIndicators(df)
  
    df['SMA'] = indicators.get_sma(20)
    
    print(df.tail())
    print("---")
    print(df.head(2))


