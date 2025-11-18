from pathlib import Path
import pandas as pd
import numpy as np

def concatCentroidWeather(save = False) -> pd.Dataframe:
    path = Path(r'../data/weather/')  
    files = list(path.glob("*.csv"))

    print("Found CSVs:", files)
    dfs = list()
    for f in files:
        data = pd.read_csv(f)
        # .stem is method for pathlib objects to get the filename w/o the extension
        data['file'] = f.stem
        dfs.append(data)

    df = pd.concat(dfs, ignore_index=True)
    if save == True:
        df.to_csv("../data/consolidated/consolidated_weather_from_centroids.csv")
    return df


if __name__ == "__main__":
    concatCentroidWeather(save = True)