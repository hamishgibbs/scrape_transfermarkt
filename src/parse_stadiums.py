import sys
import pandas as pd
import numpy as np
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
            "city": td[0].find_all("td")[-1].text.strip(),
            "capacity": td[1].text.strip().replace(".", ""),
            "seats": td[3].text.strip().replace(".", "")
        })
    
    df = pd.DataFrame.from_records(stadium_data)

    df["capacity"] = pd.to_numeric(df["capacity"], errors="coerce")
    df["seats"] = pd.to_numeric(df["seats"], errors="coerce")

    return df

if __name__ == "__main__":
    df = parse_stadium_data(sys.argv[1])
    df.to_csv(sys.argv[-1], index=False)

