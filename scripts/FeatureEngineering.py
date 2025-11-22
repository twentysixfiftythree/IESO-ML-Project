import pandas as pd
import duckdb
import holidays


class CleanedDataset:
    def __init__(self, weather_data, demand_data, price_data):
        #- -- -WEATHER --- 
        self.weather_data = weather_data
        self.weather_data['valid_time'] = pd.to_datetime(self.weather_data['valid_time'])
        columns = list(self.weather_data.columns)
        columns[0] = 'Hour'
        self.weather_data.columns = columns

        # ---- DEMAND ----

        self.demand_data = demand_data
        # add the hour column to the demand data date. the time is split into hour and date in two seperate columns
        self.demand_data['Date'] = pd.to_datetime(self.demand_data['Date'], format= 'mixed').dt.normalize()

        # hours should start from 0 to 23.
        self.demand_data['Date'] += pd.to_timedelta(self.demand_data['Hour'] - 1, unit='h')
        

        ## ---- PRICE ----- 
        self.price_data = price_data
        self.price_data = self.price_data.drop(columns = self.price_data.columns[0], axis = 1)
        self.price_data['price_Date'] = pd.to_datetime(self.price_data['Zones_Date'], format= 'mixed').dt.normalize()
        self.price_data['price_Date'] += pd.to_timedelta(self.price_data['Hour_of_Day'] -1, unit = 'h')

        #start data in 2004
        self.demand_data = self.demand_data[self.demand_data['Date'].dt.year >= 2004]
        self.weather_data = self.weather_data[self.weather_data['valid_time'].dt.year >= 2004]
        self.price_data = self.price_data[self.price_data['price_Date'].dt.year >=2004]
        # ----------------------




    def merge_datasets(self) -> pd.DataFrame:

        con = duckdb.connect(database=':memory:')
        # r4gister DataFrames
        con.register('demand_data', self.demand_data)
        con.register('weather_data', self.weather_data)
        con.register('price_data', self.price_data)

        merge_all = con.execute("""
            SELECT *
            FROM demand_data d
            LEFT JOIN weather_data w
                ON d.Date = w.valid_time
            LEFT JOIN price_data p
                ON d.Date = p.price_Date
        """).df()


        # i could use the pandas stuff, but it has no aura.
        # merged_data = pd.merge(self.demand_data, self.weather_data, left_on='Date', right_on='valid_time', how='inner')
        # merged_data.head()
        # merged_data = pd.merge(merged_data, self.price_data, left_on=['Date'], right_on=['price_Date'], how='inner')
        cols_to_drop = [
        'Hour_1',        
        'valid_time',    
        'Zones_Date',    
        'price_Date'     
    ]

        merged_df = merge_all.drop(columns=cols_to_drop)
        
        return merged_df
    

    
    def add_calendar_features(self, cleaned_data):
        """
        Add calendar and holiday features to the cleaned data.
        """
        # add calendar features
        cleaned_data['Month'] = cleaned_data['Date'].dt.month
        cleaned_data['Day'] = cleaned_data['Date'].dt.day
        cleaned_data['Weekday'] = cleaned_data['Date'].dt.weekday
        cleaned_data['Hour'] = cleaned_data['Date'].dt.hour
        
        # Get Ontario holidays for all years in the dataset
        years = cleaned_data['Date'].dt.year.unique()
        ontario_holidays = holidays.Canada(prov='ON', years=years)
        
        # Create holiday indicator
        cleaned_data['IsHoliday'] = cleaned_data['Date'].dt.date.isin(ontario_holidays).astype(int)
        
        return cleaned_data