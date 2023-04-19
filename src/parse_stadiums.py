import sys
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

def parse_stadium_data(fn):

    with open(fn, "r") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    stadium_table = soup.find_all('table', class_='profilheader')[0]
    
    td = stadium_table.find_all('td')

    return pd.DataFrame({
            "name": [td[0].text],
            "total_capacity": [td[1].text.replace(".", "")]
    })

if __name__ == "__main__":
    df = parse_stadium_data(sys.argv[1])
    df.to_csv(sys.argv[-1], index=False)

