import pandas as pd
import geopandas as gpd
from datetime import datetime, timedelta



class Centroids:
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

    def getCentroids(self):
        centroids = self.shapemap['centroid']
        centroid_list = list()
        for point in centroids:
            centroid_list.append((point.y, point.x))  # (latitude, longitude)
        return centroid_list










if __name__ == "__main__":
    obj = Centroids()
    centroids = obj.getCentroids()
    print(centroids)