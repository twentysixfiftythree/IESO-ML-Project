import requests
import pandas as pd
from pathlib import Path
from datetime import datetime
import time

class IESOScraper:
    BASE_URL = "https://reports-public.ieso.ca/public/PriceNodal/PUB_PriceNodal_{}.csv"
    
    def __init__(self, output_dir="ieso_data", start_year=2002):
        self.output_dir = Path(output_dir)
        self.start_year = start_year
        self.current_year = datetime.now().year
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def download_year(self, year):
        url = self.BASE_URL.format(year)
        output_file = self.output_dir / f"PUB_PriceNodal_{year}.csv"
        
        if output_file.exists():
            return 'skipped'
        
        try:
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                with open(output_file, 'wb') as f:
                    f.write(response.content)
                
                pd.read_csv(output_file, skiprows=2)
                print(f"Downloaded data for year: {year}")
                return 'success'
            else:
                return 'failed'
                
        except Exception:
            if output_file.exists():
                output_file.unlink()
            return 'failed'
    
    def download_all(self):
        for year in range(self.start_year, self.current_year + 1):
            self.download_year(year)
            
            time.sleep(0.5)
    
    def combine_files(self, output_file="data/combined_nodal_prices.csv"):
        csv_files = sorted(self.output_dir.glob("PUB_PriceNodal_*.csv"))
        
        if not csv_files:
            return None
        
        dfs = []
        for file in csv_files:
            try:
                df = pd.read_csv(file, skiprows=2)
                dfs.append(df)
            except Exception:
                pass
        
        if dfs:
            combined = pd.concat(dfs, ignore_index=True)
            combined.to_csv(output_file, index=False)
            return combined
        
        return None

if __name__ == "__main__":
    scraper = IESOScraper()
    scraper.download_all()
    scraper.combine_files()