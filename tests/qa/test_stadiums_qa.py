import json
import pandas as pd

def test_all_teams_are_in_stadiums(teams_fn, stadiums_geo_fn):
    
    teams = pd.read_csv(teams_fn)

    with open(stadiums_geo_fn, "r") as f:
        stadiums = json.load(f)

    assert set(teams["url_stub"]) - set(x["properties"]["team"] for x in stadiums['features']) == set()
    assert set(x["properties"]["team"] for x in stadiums['features']) - set(teams["url_stub"]) == set()