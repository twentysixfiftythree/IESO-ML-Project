import requests

class IESODataLoader:
    def __init__(self):
        self.links = []
        self.big_table = None

    def download_csv(self, url, local_filename):
        response = requests.get(url)
        if response.status_code == 200:
            with open(local_filename, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {local_filename}")
        else:
            raise Exception(f"❌ Failed to download file. Status code: {response.status_code}")


if __name__ == "__main__":
    loader = IESODataLoader()
    
    csv_url = "https://reports-public.ieso.ca/public/Demand/PUB_Demand_2002.csv"
    local_file = "ieso_data.csv"

    loader.download_csv(csv_url, local_file)
