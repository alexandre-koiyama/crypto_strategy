import pandas as pd
import requests
from datetime import datetime, timedelta

class CryptoData:
    def __init__(self, symbol, interval, start_date, end_date):
        self.symbol = symbol
        self.interval = interval
        self.start_date = start_date
        self.end_date = end_date

    def get_historical_data(self, start_time, end_time):
        url = "https://fapi.binance.com/fapi/v1/klines"
        
        # Convert start and end times to string timestamps in milliseconds
        start_date_str = str(int(start_time.timestamp() * 1000))
        end_date_str = str(int(end_time.timestamp() * 1000))

        params = {
            'symbol': self.symbol,
            'interval': self.interval,
            'startTime': start_date_str,
            'endTime': end_date_str,
            'limit': 1500  # Adjust to Binance's max limit for API requests
        }
        response = requests.get(url, params=params)

        column_names = [
            'Open Time',
            'Open',
            'High',
            'Low',
            'Close',
            'Volume',
            'Close Time',
            'Base Asset Volume',
            'Number of Trades',
            'Taker Buy Volume',
            'Taker Buy Base Asset Volume',
            'Ignore'
        ]

        if response.status_code != 200:
            print(f'Error fetching data: {response.status_code}')
            return None
        else:
            data = response.json()
            df = pd.DataFrame(data, columns=column_names)
            df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')
            df['Close Time'] = pd.to_datetime(df['Close Time'], unit='ms')
            return df

    def get_divisions(self):
        start_date = datetime(self.start_date.year, self.start_date.month, self.start_date.day)
        end_date = datetime(self.end_date.year, self.end_date.month, self.end_date.day)
        date_difference = (end_date - start_date).days

        interval = self.interval
        if interval == '1m':
            divisions = (date_difference * 60 * 24) // 500 + 1
            int_time = 60
        elif interval == '5m':
            divisions = (date_difference * (60 / 5) * 24) // 500 + 1
            int_time = 5 * 60
        elif interval == '15m':
            divisions = (date_difference * (60 / 15) * 24) // 500 + 1
            int_time = 15 * 60
        elif interval == '1h':
            divisions = (date_difference * 24) // 500 + 1
            int_time = 60 * 60
        elif interval == '1d':
            divisions = date_difference // 500 + 1 if date_difference > 500 else 1
            int_time = 24 * 60 * 60
        return int(divisions), int_time

    def get_all_historical_data(self):
        divisions, int_time = self.get_divisions()
        print(divisions)
        data_frames = []
        for num in range(divisions):
            # Calculate the new start and end dates
            new_start_date = self.start_date + timedelta(seconds=500 * num * int_time)
            new_end_date = self.start_date + timedelta(seconds=500 * (num + 1) * int_time)
            
            
            new_df = self.get_historical_data(new_start_date, new_end_date)
            if new_df is not None:
                data_frames.append(new_df)

        # Concatenate all dataframes
        data_hist_pd = pd.concat(data_frames)
        data_hist_pd = data_hist_pd.drop_duplicates(subset=['Open Time'], keep='first')
        data_hist_pd = data_hist_pd.reset_index(drop=True)
        data_hist_pd = data_hist_pd[['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Number of Trades']]
        return data_hist_pd
