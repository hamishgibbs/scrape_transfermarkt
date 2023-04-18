import pandas as pd
from datetime import datetime
from parse import parse_table, parse_team_name

def parse_team_url_stub(td):
    return td.find_all('a')[0].get("href").split("/")[0]


def parse_teams_data(fn):

    teams_rows = parse_table(fn)
    
    team_data = []

    for row in teams_rows:
        row_data = {}

        if row.find_all('th'):
            continue

        td = row.find_all('td')
        
        print(row)
        row_data["name"] = parse_team_name(td[1])
        row_data["url_stub"] = parse_team_url_stub(td[1])
        team_data.append(row_data)
    
    df = pd.DataFrame.from_records(team_data)

    print(df)



