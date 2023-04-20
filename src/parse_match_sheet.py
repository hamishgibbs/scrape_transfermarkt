import os
import sys
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

def parse_match_sheet(fn):

    with open(fn, "r") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    stadium_p = soup.find_all("p", class_="sb-zusatzinfos")[0]

    stadium_href = stadium_p.find_all('a')[0].get('href')

    stadium = {
        "match_sheet_id": os.path.basename(fn).split("_")[-1].split(".")[0],
        "stadium_name": stadium_p.find_all("a")[0].text.strip(),
        "stadium_url": f"https://www.transfermarkt.co.uk{stadium_href}",
        "association": stadium_href.split("/")[-3],
        "season": stadium_href.split("/")[-1]
    }

    df = pd.DataFrame.from_records([stadium])

    return df

if __name__ == "__main__":
    df = parse_match_sheet(sys.argv[1])
    df.to_csv(sys.argv[-1], index=False)

