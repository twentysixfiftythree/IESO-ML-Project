import pandas as pd

class CleanedDataset:
    def __init__(self, weather_data, demand_data):
        self.weather_data = weather_data
        self.demand_data = demand_data
        # add the hour column to the demand data date. the time is split into hour and date in two seperate columns
        

    def merge_datasets(self):
        # ensure datetime columns are in datetime format
        self.weather_data['datetime'] = pd.to_datetime(self.weather_data['datetime'])
        self.demand_data['Date/Time'] = pd.to_datetime(self.demand_data['Date/Time'])

        # merge datasets on datetime
        merged_data = pd.merge(self.demand_data, self.weather_data, left_on='Date/Time', right_on='datetime', how='inner')

        return merged_data