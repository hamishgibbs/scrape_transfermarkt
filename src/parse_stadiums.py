import sys
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

def parse_stadium_data(fn):

    with open(fn, "r") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    table = soup.find_all(class_="responsive-table")[0]

    rows = table.find_all('tbody')[0].find_all('tr', recursive=False)
    
    stadium_data = []

    for row in rows:

        td = row.find_all('td', recursive=False)
        
        stadium_data.append({
            "team": td[0].find_all('a')[0].get("href").split("/")[1],
            "name": td[0].find_all('a')[1].text,
            "capacity": td[1].text.replace(".", ""),
            "seats": td[3].text.replace(".", "")
        })
    
    return pd.DataFrame.from_records(stadium_data)

if __name__ == "__main__":
    df = parse_stadium_data(sys.argv[1])
    df.to_csv(sys.argv[-1], index=False)

