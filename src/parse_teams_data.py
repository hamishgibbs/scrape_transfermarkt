import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

def parse_teams_data(fn):

    with open(fn, "r") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    

