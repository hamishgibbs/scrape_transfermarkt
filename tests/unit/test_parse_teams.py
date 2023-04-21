import pandas as pd
from parse_teams import parse_teams_data

def test_parse_teams_data():

    res = parse_teams_data("tests/data/teams_data.html")

    first_row_expected = pd.Series({
        "name": "Manchester City",
        "url_stub": "manchester-city",
        "association": "281"
    }, name=0)
    
    last_row_expected = pd.Series({
        "name": "AFC Bournemouth",
        "url_stub": "afc-bournemouth",
        "association": "989"
    }, name=19)

    assert res.shape == (20, 3)
    pd.testing.assert_series_equal(res.iloc[0, :], first_row_expected)
    pd.testing.assert_series_equal(res.iloc[-1, :], last_row_expected)
    