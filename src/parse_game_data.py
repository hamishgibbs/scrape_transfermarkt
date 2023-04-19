import sys
import re
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

def parse_date_time(date, time):
    return datetime.strptime(date.split(" ")[-1] + " " + time, 
                      "%d.%m.%y %H:%M")

def parse_score(td):
    return td.find_all('span')[0].text.strip().split(":")

def parse_game_data(fn):

    with open(fn, "r") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    tables_div = soup.find_all(class_="large-8 columns")[0]

    game_tables = tables_div.find_all('tbody')

    game_data = []

    for table in game_tables[1:-1]:

        td = table.find_all('td')

        game_data.append(
            {
                "home_team": td[0].find_all('a')[-1].get("href").split("/")[1],
                "away_team": td[7].find_all('a')[0].get("href").split("/")[1],
                "date": td[9].find_all('a')[0].text.strip(),
                "time": re.findall(r'(\d*:\d* \w*)', td[9].text)[0],
                "attendance": td[10].text.strip().split('\t')[0].replace(".", "")
            }
        )
        
    df = pd.DataFrame.from_records(game_data)

    return df

if __name__ == "__main__":
    df = parse_game_data(sys.argv[1])
    df.to_csv(sys.argv[-1], index=False)

