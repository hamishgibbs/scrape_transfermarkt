import sys
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

def parse_team_name(td):
    return td.find_all('a')[0].get("title")

def parse_teams_data(fn):

    with open(fn, "r") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    table = soup.find_all(class_="responsive-table")[0]

    teams_rows = table.find_all('tbody')[0].find_all('tr')
    
    team_data = []

    for row in teams_rows:
        row_data = {}

        if row.find_all('th'):
            continue

        td = row.find_all('td')
        
        row_data["name"] = parse_team_name(td[1])
        row_data["url_stub"] = parse_team_url_stub(td[1].find_all('a')[0].get("href").split("/")[1])
        team_data.append(row_data)
    
    df = pd.DataFrame.from_records(team_data)

    return df

if __name__ == "__main__":
    df = parse_teams_data(sys.argv[1])
    df.to_csv(sys.argv[-1], index=False)