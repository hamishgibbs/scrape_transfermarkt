import json
import pandas as pd

def test_all_teams_are_in_stadiums():
    
    teams = pd.read_csv("data/teams.csv")

    with open("data/geo/stadiums.geojson", "r") as f:
        stadiums = json.load(f)

    assert set(teams["url_stub"]) - set(x["properties"]["team"] for x in stadiums['features']) == set()
    assert set(x["properties"]["team"] for x in stadiums['features']) - set(teams["url_stub"]) == set()