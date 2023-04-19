import sys
import pandas as pd
import requests
from parse_stadiums import parse_stadium_data
from scrape import headers

def main():

    teams = pd.read_csv(sys.argv[1])['url_stub'].to_list()
    seasons = [2016, 2017, 2018, 2019, 2020]

    stadium_data = []

    for team in teams:
        for season in seasons:
            response = requests.get(
                f"https://www.transfermarkt.co.uk/{team}/stadion/verein/31/saison_id/{season}", 
                headers=headers)
            stadium_data.append(parse_stadium_data(response.text))
    
    pd.concat(stadium_data).to_csv(sys.argv[-1], index=False)

if __name__ == "__main__":
    main()

    