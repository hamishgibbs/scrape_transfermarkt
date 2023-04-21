import sys
import re
import os
import pandas as pd
from bs4 import BeautifulSoup

def parse_stadium_data(fn):

    with open(fn, "r") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    table = soup.find_all("div", class_="large-8 columns")[1]

    rows = table.find_all('tr')

    address_table = soup.find_all("div", class_="large-4 columns")[0]

    script = " ".join([x.text for x in soup.find_all("script")])

    coordinates = re.findall(r'koordinaten=\[(.*?)]', script)[0]
    
    stadium_data = {
        "association": os.path.basename(fn).split("_")[-2],
        "season": os.path.basename(fn).split("_")[-1].split(".")[0],
        "name": rows[0].find_all("td")[0].text.strip(),
        "capacity": rows[1].find_all("td")[0].text.strip().replace(".", ""),
        "seats": rows[3].find_all("td")[0].text.strip().replace(".", ""),
        "x": coordinates.split(",")[0].strip(),
        "y": coordinates.split(",")[1].strip()
    }
    
    df = pd.DataFrame.from_records([stadium_data])

    df["capacity"] = pd.to_numeric(df["capacity"], errors="coerce")
    df["seats"] = pd.to_numeric(df["seats"], errors="coerce")
    df["x"] = pd.to_numeric(df["x"], errors="coerce")
    df["y"] = pd.to_numeric(df["y"], errors="coerce")

    return df

if __name__ == "__main__":
    df = parse_stadium_data(sys.argv[1])
    df.to_csv(sys.argv[-1], index=False)

