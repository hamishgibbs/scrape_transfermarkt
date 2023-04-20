import os
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

    tables_div = soup.find_all(class_="responsive-table")[0]
    game_table = tables_div.find_all('tbody')[0]
    game_rows = game_table.find_all('tr')

    game_data = []

    for table in game_rows:

        td = table.find_all('td')

        if len(td) == 1:
            continue

        date = td[1].text.strip().split(" ")[-1]
        time = td[2].text.strip()

        game_data.append(
            {   
                "date_time": datetime.strptime(date + " " + time, "%d.%m.%y %H:%M"),
                "home_team": os.path.basename(fn).split("_")[0],
                "away_team": td[5].find_all('a')[0].get("href").split("/")[1],
                "attendance": td[8].text.strip().replace(".", ""),
                "home_flag": td[3].text.strip(),
                "match_sheet_url": td[9].find_all('a')[0].get("href").split("/")[-1]
            }
        )
        
    df = pd.DataFrame.from_records(game_data)

    df["attendance"] = pd.to_numeric(df["attendance"], errors="coerce")

    return df

if __name__ == "__main__":
    df = parse_game_data(sys.argv[1])
    df.to_csv(sys.argv[-1], index=False)

