import pandas as pd
from datetime import datetime
from parse import parse_table, parse_team_name

def parse_date_time(date, time):
    return datetime.strptime(date.split(" ")[-1] + " " + time, 
                      "%d.%m.%y %H:%M")

def parse_score(td):
    return td.find_all('span')[0].text.strip().split(":")

def parse_game_data(fn):

    game_rows = parse_table(fn)

    game_data = []

    for row in game_rows:
        row_data = {}

        if row.find_all('td', class_="extrarow"):
            continue

        td = row.find_all('td')
        
        row_data["date_time"] = parse_date_time(
            date = td[1].text.strip(),
            time = td[2].text.strip()
        )
        row_data["home_team"] = parse_team_name(td[4])
        row_data["away_team"] = parse_team_name(td[6])
        row_data["attendance"] = td[9].text.strip()
        row_data["home_score"], row_data["away_score"] = parse_score(td[10])
        game_data.append(row_data)
    
    df = pd.DataFrame.from_records(game_data)

    print(df)

