import pandas as pd
import geopandas as gpd

import requests
from datetime import datetime, timedelta
import time


class WeatherDim:
    def __init__(self):

        latitude = None
        longitude = None
        time = None
        unit = None
        hourly = None
        lang = None
        stationPressure = None

        self.base_link = f"""
        
        https://api.pirateweather.net/forecast/{self.KEY}/
        {[latitude]},{[longitude]},{[time]}?exclude=[excluded]&units={[unit]}
        &extend={[hourly]}&version=[2]&lang={[lang]}&extraVars={[stationPressure]}
        """
        self.shapemap = gpd.read_file('data/tenzones_ieso.geojson')
        self.shapemap['centroid'] = self.shapemap.geometry.centroid
        

        print(self.shapemap)










if __name__ == "__main__":
    obj = WeatherDim()
    obj.addWeather()
