import requests
import pandas as pd
import os

class IESODataLoader:
    def __init__(self, outdir="data"):
        self.outdir = outdir
        os.makedirs(outdir, exist_ok=True)
        self.big_table = pd.DataFrame()
    
    def download_csv(self, url, local_filename):
        response = requests.get(url, timeout=30)
        with open(local_filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {local_filename}")
    
    def _load_csv_with_header_detection(self, filepath):
        with open(filepath, "r") as f:
            lines = f.readlines()
        header_row = next(i for i, line in enumerate(lines) if line.strip().startswith("Date"))
        return pd.read_csv(filepath, skiprows=header_row)
    
    def load_all_years(self, start=2002, end=2025):
        for year in range(start, end + 1):
            url = f"https://reports-public.ieso.ca/public/Demand/PUB_Demand_{year}.csv"
            local_file = os.path.join(self.outdir, f"PUB_Demand_{year}.csv")
            
            if not os.path.exists(local_file):
                self.download_csv(url, local_file)
            
            df = self._load_csv_with_header_detection(local_file)
            df["Year"] = year
            self.big_table = pd.concat([self.big_table, df], ignore_index=True)
            print(f"Loaded {year}")
        
        return self.big_table

if __name__ == "__main__":
    loader = IESODataLoader()
    all_data = loader.load_all_years()
    print("Combined dataset shape:", all_data.shape)
    all_data.to_csv("data/consolidatedIESOdemand.csv", index=False)
