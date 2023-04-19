import pandas as pd
from parse_games import parse_game_data

def test_parse_game_data():

    res = parse_game_data("tests/data/game_data.html")

    assert res.shape == (10, 5)
    assert res.iloc[0]["home_team"] == "fc-liverpool"
    assert res.iloc[-1]["away_team"] == "fc-chelsea"
    assert res.iloc[4]["attendance"] == 19784

def test_parse_game_data_removes_sold_out():

    res = parse_game_data("tests/data/game_data_sold_out.html")
    
    assert res.shape == (10, 5)
    assert res.iloc[7]["attendance"] == 11355

def test_parse_game_data_coerces_missing_values():

    res = parse_game_data("tests/data/game_data_attendance_missing.html")
    
    assert res.shape == (10, 5)
    assert pd.isna(res.iloc[0]["attendance"])