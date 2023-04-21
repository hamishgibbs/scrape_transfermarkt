import pandas as pd
from parse_stadiums import parse_stadium_data

def test_parse_stadium_data():

    res = parse_stadium_data("tests/data/stadium_data_3299_2015.html")

    expected = pd.Series({
        "association": "3299",
        "season": "2015",
        "name": "Wembley Stadium",
        "capacity": 90000,
        "seats": 90000,
        "x": -0.2795188,
        "y": 51.5560208
    }, name=0)

    assert res.shape == (1, 7)
    pd.testing.assert_series_equal(res.iloc[0, :], expected)

    res = parse_stadium_data("tests/data/stadium_data_631_2015.html")

    expected = pd.Series({
        "association": "631",
        "season": "2015",
        "name": "Stamford Bridge",
        "capacity": 40853,
        "seats": 40853,
        "x": -0.1909565,
        "y": 51.481663
    }, name=0)

    assert res.shape == (1, 7)
    pd.testing.assert_series_equal(res.iloc[0, :], expected)

