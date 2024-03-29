import pandas as pd
import numpy as np
from parse_games import parse_game_data
from datetime import datetime

def test_parse_game_data():

    res = parse_game_data("tests/data/tottenham-hotspur_game_data.html")

    first_row_expected = pd.Series({
        "date_time": datetime(2019, 8, 10, 17, 30),
        "team_1": "tottenham-hotspur",
        "team_2": "aston-villa",
        "attendance": 60407.0,
        "home_flag": "H",
        "match_sheet_id": "3194823"
    }, name=0)

    last_row_expected = pd.Series({
        "date_time": datetime(2020, 7, 26, 16, 00),
        "team_1": "tottenham-hotspur",
        "team_2": "crystal-palace",
        "attendance": np.nan,
        "home_flag": "A",
        "match_sheet_id": "3219104"
    }, name=51)

    assert res.shape == (52, 6)
    pd.testing.assert_series_equal(res.iloc[0, :], first_row_expected)
    pd.testing.assert_series_equal(res.iloc[-1, :], last_row_expected)
    assert len(res["match_sheet_id"].unique()) == res.shape[0]

